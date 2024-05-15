from fastapi import FastAPI
from app.routers import users, auth, reset_password, blog_content


app= FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(reset_password.router)
app.include_router(blog_content.router)


@app.get('/')
def get_main():
    return{'Hello':'world'}
