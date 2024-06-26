from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.database.schemas import db
from app.autenthication import utils, oauth2


router = APIRouter(prefix="/login", tags=["Authentication"])


@router.post("/", status_code=status.HTTP_200_OK)
async def login (user_credentials: OAuth2PasswordRequestForm = Depends()):

      user = await db["users"].find_one({"name" : user_credentials.username}) 

      if user and utils.verify_password(user_credentials.password, user["password"]):
            
            access_token = oauth2.create_access_token ({"id" : str(user["_id"])})

            return {"access_token": access_token, "token_type": "bearer"}
      
      else:
            raise HTTPException (status_code=status.HTTP_403_FORBIDDEN,
                                 detail= "Invalide user credentials")








