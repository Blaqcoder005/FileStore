import time
from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse

from dependencies import hash_password, verify_password
from config import db

router = APIRouter(tags=["auth"], prefix="/auth")

#------------------Session-Checker-------------- 
@router.get("/me") 
def auth_me(request: Request):
    user_id = request.session.get("user_id")
    email = request.session.get("email")
    if not user_id:
        return {"authenticated": False}

    result = db.table("users") \
             .select("username") \
             .eq("id", user_id) \
             .eq("email", email) \
             .single() \
             .execute()

    if not result.data:
        return {"authenticated": False}

    return {
        "authenticated": True,
        "user_id": user_id,
        "username": result.data["username"],
        "email": email
    }


#-------------------Pages----------------
@router.post("/register")
async def register(request: Request):
    data = await request.form()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    #check existing email
    existing = db.table("users").select("id").eq("email", email).execute()
    if existing.data:
       return HTMLResponse("Email already exist", status_code=400)

    # store hash password
    pw_hash = hash_password(password)
    db.table("users").insert({
        "username": username,
        "email": email,
        "password_hash": pw_hash

    }).execute()

    return {"success": True}

@router.post("/login")
async def login(request: Request):
    data = await request.form()
    print(data)
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    print (username, email, password)

    resp = db.table("users").select("id,username,email,password_hash").eq("email", email).execute()
    print(resp.data)

    if not resp.data:
        return HTMLResponse("Invalid credentials", status_code=401)

    user = resp.data[0]
    if not verify_password(password, user["password_hash"]):
        return HTMLResponse("Invalid credentials", status_code=401)

    # SUCCESS - set session
    request.session["user_id"] = str(user["id"])
    request.session["email"] = user["email"]
    request.session["username"] = str(user["username"])

    return {"success": True,
            "user": {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"]
        }
    }

@router.post("/logout")
async def logout():
    request.session.clear()
    return {"success": True}

