from jose import JWTError, jwt 
from datetime import datetime, timedelta 
from dotenv import load_dotenv
import os
from typing import Dict
from app.database.schemas import TokenData, db
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from bson import ObjectId

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login/')

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
SECRET_KEY = os.getenv("SECRET_KEY") 
ALGORITHM = os.getenv ("ALGORITHM")

def create_access_token (payload: Dict):
    to_encode = payload.copy()

    expiration_time =  datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expiration_time})

    jw_token = jwt.encode (to_encode, SECRET_KEY, algorithm= ALGORITHM)

    return jw_token

def verify_access_token (token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        id: str= payload.get("id")

        if id is None:
            raise credentials_exception
        
        token_data = TokenData(id=id)

    except JWTError:
        raise credentials_exception
    
    return token_data

async def get_current_user(token: str = Depends(oauth2_scheme)):

    credentials_exception= HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="Token could not verify credentails", 
                                         headers= {"WWW-Authenticate":"Bearer"})
    
    current_user_id= verify_access_token(token, credentials_exception).id
    
    current_user= await db["users"].find_one({"_id": ObjectId(current_user_id)})

    return current_user







