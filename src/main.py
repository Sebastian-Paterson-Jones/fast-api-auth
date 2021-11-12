from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication

from database.models import User, UserCreate, UserUpdate, UserDB
from database.user_manager import get_user_manager
from database.db import database

SECRET = "SECRET"

jwt_authentication = JWTAuthentication(secret=SECRET, lifetime_seconds=3600)

fastapi_users = FastAPIUsers(
    get_user_manager,
    [jwt_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

app = FastAPI()

# establish db connection
@app.on_event("startup")
async def startup():
    await database.connect()

# close db connection
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# router for user login and logout
app.include_router(
    fastapi_users.get_auth_router(jwt_authentication),
    prefix="/auth",
    tags=["auth"],
)

# router for user register
app.include_router(
    fastapi_users.get_register_router(),
    prefix="/auth",
    tags=["auth"],
)

# router for reset user password
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

# router to get, delete, or update user
app.include_router(
    fastapi_users.get_users_router(),
    prefix="/users",
    tags=["users"],
)
