"""
MongoDB-backed authentication helpers.

Uses a free MongoDB Atlas cluster (see README for setup). The connection
string is read from Streamlit secrets as `MONGO_URI`. If it is missing,
the app falls back to a local in-memory store so the UI still works in a
sandbox/demo environment.
"""

import hashlib
import hmac
import os
import re
from datetime import datetime, timezone

import streamlit as st

try:
    from pymongo import MongoClient
    from pymongo.errors import PyMongoError
    PYMONGO_AVAILABLE = True
except ImportError:  # pragma: no cover
    PYMONGO_AVAILABLE = False

DB_NAME = "ai_offensive_security"
USERS_COLLECTION = "users"

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


# --------------------------------------------------------------------------
# Connection
# --------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def _get_client():
    """Returns a cached MongoClient, or None if no URI is configured."""
    uri = None
    try:
        uri = st.secrets.get("MONGO_URI")
    except Exception:
        uri = os.environ.get("MONGO_URI")

    print("DEBUG: uri is None?", uri is None)
    print("DEBUG: PYMONGO_AVAILABLE =", PYMONGO_AVAILABLE)
    if uri:
        # Show first 40 chars only, no password leak
        print("DEBUG: uri prefix =", uri[:40])

    if not uri or not PYMONGO_AVAILABLE:
        print("DEBUG: returning None because uri missing or pymongo unavailable")
        return None

    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        print("DEBUG: MongoDB connection SUCCESS")
        return client
    except PyMongoError as e:
        print("DEBUG: MongoDB connection FAILED:", repr(e))
        return None
    except Exception as e:
        print("DEBUG: Unexpected error:", repr(e))
        return None


def _get_users_collection():
    client = _get_client()
    if client is None:
        return None
    return client[DB_NAME][USERS_COLLECTION]


def db_is_connected() -> bool:
    return _get_users_collection() is not None


# --------------------------------------------------------------------------
# Local fallback store (demo mode only — resets on restart)
# --------------------------------------------------------------------------
def _local_store():
    if "local_users" not in st.session_state:
        st.session_state.local_users = {}
    return st.session_state.local_users


# --------------------------------------------------------------------------
# Password hashing (PBKDF2-HMAC-SHA256, stdlib only)
# --------------------------------------------------------------------------
def _hash_password(password: str, salt: bytes | None = None) -> str:
    if salt is None:
        salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000)
    return f"{salt.hex()}${digest.hex()}"


def _verify_password(password: str, stored: str) -> bool:
    try:
        salt_hex, digest_hex = stored.split("$")
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(digest_hex)
    except ValueError:
        return False
    candidate = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000)
    return hmac.compare_digest(candidate, expected)


# --------------------------------------------------------------------------
# Validation
# --------------------------------------------------------------------------
def is_valid_email(email: str) -> bool:
    return bool(EMAIL_RE.match(email or ""))


def password_strength_issues(password: str) -> list[str]:
    issues = []
    if len(password or "") < 8:
        issues.append("at least 8 characters")
    if not re.search(r"[A-Z]", password or ""):
        issues.append("one uppercase letter")
    if not re.search(r"[a-z]", password or ""):
        issues.append("one lowercase letter")
    if not re.search(r"\d", password or ""):
        issues.append("one number")
    return issues


# --------------------------------------------------------------------------
# Public API
# --------------------------------------------------------------------------
def register_user(name: str, email: str, password: str) -> tuple[bool, str]:
    email = email.strip().lower()
    name = name.strip()

    if not name:
        return False, "Please enter your name."
    if not is_valid_email(email):
        return False, "Please enter a valid email address."
    issues = password_strength_issues(password)
    if issues:
        return False, "Password needs: " + ", ".join(issues) + "."

    hashed = _hash_password(password)
    doc = {
        "name": name,
        "email": email,
        "password": hashed,
        "created_at": datetime.now(timezone.utc),
    }

    col = _get_users_collection()
    if col is not None:
        if col.find_one({"email": email}):
            return False, "An account with this email already exists."
        col.insert_one(doc)
        return True, "Account created successfully. You can now log in."

    # local fallback
    store = _local_store()
    if email in store:
        return False, "An account with this email already exists."
    store[email] = doc
    return True, "Account created successfully (demo mode — no database configured). You can now log in."


def authenticate_user(email: str, password: str) -> tuple[bool, str]:
    email = email.strip().lower()
    col = _get_users_collection()

    if col is not None:
        user = col.find_one({"email": email})
    else:
        user = _local_store().get(email)

    if not user:
        return False, "No account found with that email."
    if not _verify_password(password, user["password"]):
        return False, "Incorrect password."

    st.session_state.authenticated = True
    st.session_state.user_name = user["name"]
    st.session_state.user_email = user["email"]
    return True, f"Welcome back, {user['name']}!"


def logout():
    for key in ("authenticated", "user_name", "user_email"):
        st.session_state.pop(key, None)


def is_authenticated() -> bool:
    return bool(st.session_state.get("authenticated"))
