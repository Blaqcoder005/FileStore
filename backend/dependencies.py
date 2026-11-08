from fastapi import Request, HTTPException, status, Depends
from config import db
import hashlib, secrets

#................endpoint_security................
def require_session_user(request: Request):
    if not request.session.get("user_id"):
        raise HTTPException(status_code=401)

    return {
        "id": request.session["user_id"],
        "email": request.session["email"],
        "username": request.session["username"],
    }

def rate_limiter(user=Depends(require_session_user)):
    user_id = user
    if not db.rate_limit(key=f"upload:{user}", limit=10, window=60)["allowed"]:
        raise HTTPException(429, "Too many uploads")

def allowed_filename(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {"png", "jpg", "pdf", "docx", "gif", "jpeg"}

#=======================Password-Hasher===========================
def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}${hashed}"

def verify_password(password: str, stored: str) -> bool:
    try:
        salt, hashed = stored.split("$")
    except ValueError:
        return False
    return hashlib.sha256((salt + password).encode()).hexdigest() == hashed

#==============Supabase Wrapper====================
def _row_to_dict(self, columns, row):
    result = {}
    for col, val in zip(columns, row):
        # Convert UUID to string
        if hasattr(val, 'hex') and hasattr(val, 'int'):  # UUID check
            result[col] = str(val)
        else:
            result[col] = val
    return result

#========================Upload-Security=====================
async def secure_filename(filename):
    try:
        result = db.table("files").insert(filename).execute()
        if result.data == "success":
            return True
    except:
        raise HTTPException(status_code=400)
    return result

async def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {"png", "jpg", "jpeg", "gif", "pdf", "py"}
