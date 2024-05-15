from fastapi import APIRouter, HTTPException, status
from app.database.schemas import PasswordReset, db, NewPasssword
from app.autenthication.oauth2 import create_access_token, get_current_user
from app.mail.send_mail import password_reset
from app.autenthication.utils import get_password_hash


router = APIRouter(prefix="/password", tags=["Reset Password"])


@router.post("/request/", response_description="Request to Reset password")
async def reset_request(user_email: PasswordReset):

    user = await db["users"].find_one({"email" : user_email.email})

    if user is not None:

        token = create_access_token({"id" : str(user["_id"])})

        reset_link = f"http://localhost:8000/?token={token}"

        await password_reset("Password Reset", user["email"], 
                             {"title" : "Password Reset",
                             "name" : user["name"],
                             "reset_link" : reset_link})

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid email")
    

@router.put("/reset/", response_description="Reset password")
async def reset (token: str, new_password: NewPasssword):
    #verificar que se ha pasado la new info
    request_data = {k:v for k,v in new_password.dict().items() if v is not None}

    request_data["password"] = get_password_hash(request_data["password"])

    if len(request_data) >= 1:
        user = await get_current_user(token)

        update_result = await db["users"].update_one({"_id" : user["_id"]},
                                                     {"$set" : request_data})
        if update_result.modified_count == 1:
            updated_user = await db["users"].find_one({"_id": user["_id"]})
            updated_user["_id"] = str(updated_user["_id"])
            
            if updated_user is not None:
                return updated_user
            
    existing_user = await db["users"].find_one({"_id": user["_id"]})
    existing_user["_id"] = str(existing_user["_id"])
  
    if existing_user is not None:
        return existing_user
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "User info not found")

