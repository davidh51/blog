from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.database.schemas import BlogContent, BlogContentResponse, db
from app.database.model import user_schema, users_schema
from app.autenthication.oauth2 import get_current_user
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from typing import List
from bson import ObjectId

router = APIRouter (prefix= "/blog", tags= ["Blog content"])


@router.post("/", response_description= "Create blog content", response_model= BlogContentResponse)
async def create_blog(blog_content: BlogContent, current_user: str= Depends(get_current_user)):
    try:
        blog_content = jsonable_encoder(blog_content)

        blog_content["author_name"] = current_user["name"]
        blog_content["author_id"] = str(current_user["_id"])
        blog_content["created_at"] = str(datetime.utcnow())

        new_blog_content = await db["BlogPosts"].insert_one(blog_content)
        created_blog_post = await (db["BlogPosts"].find_one({"_id": new_blog_content.inserted_id}))
        created_blog_post = user_schema(created_blog_post)

        return created_blog_post

    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail= "Internal server error")

@router.get("/", response_description="Get Blog content", response_model=List[BlogContentResponse])
async def get_blogs( limit: int = 4, orderby: str= "created_at"):
    try:
        blog_posts = await db.BlogPosts.find({"$query":{}, "$orderby":{orderby:-1}}).to_list(limit)
        
        return users_schema(blog_posts)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail= "Internal server error")
    
@router.get("/{id}", response_description="Get one Blog content", response_model=BlogContentResponse)
async def get_blog(id: str):
    try:
        blog_posts = await db["BlogPosts"].find_one({"_id": ObjectId(id)})
        
        if blog_posts is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"Post with id {id} not found")

        return user_schema(blog_posts)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail= "Internal server error")

@router.put("/{id}", response_description="Update one Blog content", response_model=BlogContentResponse)
async def update_blog(id: str, blog_content:BlogContent, current_user=Depends(get_current_user)):

    if blog_post := await db["BlogPosts"].find_one({"_id" : ObjectId(id)}):

        if blog_post["author_id"] == str(current_user["_id"]):

            try: # blog_content=dict(blog_content)
                blog_content={k:v for k,v in blog_content.dict().items() if v is not None}

                if len(blog_content) >= 1:
                    update_result = await db["BlogPosts"].update_one({"_id" : ObjectId(id)},
                                                                     {"$set" : blog_content})
                    if update_result.modified_count == 1:
                        if (updated_post := await db["BlogPosts"].find_one({"_id": ObjectId(id)})) is not None:
                            return user_schema(updated_post)      

                    if (existing_post := await db["BlogPosts"].find_one({"_id": ObjectId(id)})) is not None:  
                        return user_schema(existing_post)
                    
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Post not found")                                                                                                 

            except Exception as e:
                print(e)
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail= "Internal error")
        else: 
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Not authprized")
    else: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Post not found") 
 
@router.delete("/{id}", response_description="Delete Blog Post")
async def delete_post (id: str, current_user=Depends(get_current_user)):

    if blog_post := await db["BlogPosts"].find_one({"_id" : ObjectId(id)}):

        if blog_post["author_id"] == str(current_user["_id"]):

            try:
                delete_result = await db["BlogPosts"].delete_one({"_id": ObjectId(id)})

                if delete_result.deleted_count == 1:
                    
                    return Response(status_code=status.HTTP_204_NO_CONTENT)
                else:
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal error")                                                                                                
            
            except Exception as e:
                print (e)
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal error")                                                                                                 
        else: 
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Not authorized")
    else: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Post not found") 

