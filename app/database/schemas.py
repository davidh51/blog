from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field, EmailStr
from typing import Optional


load_dotenv()

client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))

db = client.test2

#BSON to JSON
#class PyObjectId(ObjectId):
#    @classmethod
#    def __get_validators__(cls):
#        yield cls.validate

#    @classmethod
#    def validate(cls, v):
#        if not ObjectId.is_valid(v):
#            raise ValueError("Invalid ObjectId")
#        return ObjectId(v)

#    @classmethod
#    def __get_pydantic_json_schema__(
#        cls, core_schema: CoreSchema, handler: GetJsonSchemaHandler
#    ) -> Dict[str, Any]: # type: ignore
#        json_schema = super().__get_pydantic_json_schema__(core_schema, handler)
#        json_schema = handler.resolve_ref_schema(json_schema)
#        json_schema.update(examples='examples')
#        return json_schema

class User (BaseModel):
    id: str = Field(...) #PyObjectId = Field (default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

#    class Config:
#        allowed_population_by_field_name = True
#        arbitrary_types_allowed = True
#        json_encoders = {ObjectId:str}
#        json_schema_extra = {
#            "example":{
#                "name":"dvd hno",
#                "email":"dvd@gmail.com",
#                "password":"123456"
#            }
#        }

class UserResponse (BaseModel):
    #id: ObjectId = Field(alias="_id")#PyObjectId = Field (default_factory=PyObjectId, alias="_id")
    id: str
    name: str = Field(...)
    email: EmailStr = Field(...)

#    class Config:
#        allowed_population_by_field_name = True
#        arbitrary_types_allowed = True
#        json_encoders = {ObjectId:str}
#        json_schema_extra = {
#            "example":{
#                "name":"dvd hno",
#                "email":"dvd@gmail.com"
#            }
#        }

class BlogContent (BaseModel):
    title: str= Field(...)
    body: str= Field(...)


class BlogContentResponse (BaseModel):
    id: str = Field(...)
    title: str= Field(...)
    body: str= Field(...)
    author_name: str= Field(...)
    author_id: str= Field(...)
    created_at: str= Field(...)

class TokenData (BaseModel):
    id: str

class PasswordReset(BaseModel):
    email: EmailStr

class NewPasssword(BaseModel):
    password: str

