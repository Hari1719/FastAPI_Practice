from starlette import status
from typing import Annotated
from fastapi import APIRouter,HTTPException,Depends
from passlib.context import CryptContext
from database import SessionLocal_auth,SessionLocal_pdc
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import Users,PDC_USERS
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt,JWTError
from datetime import datetime, timedelta, timezone

router=APIRouter(
    prefix="/auth",
    tags=["auth"]
)

bcrypt_context=CryptContext(schemes=["bcrypt"],deprecated='auto')

SECRET_KEY="18638583fd8f923b8d0c73d95b97ba5197339ec2547836d503701bd0475a817d"
ALGORITHM="HS256"

oauth_bearer=OAuth2PasswordBearer(tokenUrl='auth/token')
class User_Detail(BaseModel):
    username:str
    password:str
    role:str

class Token(BaseModel):
    access_token:str
    token_type:str
def get_db():
    db=SessionLocal_pdc()
    try:
        yield db
    finally:
        db.close()

def get_db1():
    db=SessionLocal_auth()
    try:
        yield db
    finally:
        db.close()
def authenticate_user(username:str,password:str,db):
    user=db.query(Users).filter(Users.username==username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password,user.hashed_password):
        return False
    return user

def create_access_token(username:str,user_id:int,role:str,expires_delta:timedelta):
    encode={"sub":username,"id":user_id,"role":role,"exp":datetime.now(timezone.utc)+expires_delta}
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

def get_current_user(token:Annotated[str,Depends(oauth_bearer)]):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str=payload.get("sub")
        user_id:str=payload.get("id")
        user_role:str=payload.get("role")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate a user")
        return {"username":username,"id":user_id,"role":user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate a user")
@router.post("/createpdc_user",status_code=status.HTTP_201_CREATED)
async def create_USerAccount(db:Annotated[Session,Depends(get_db1)],create_user:User_Detail):
    create_user_model=Users(
        username=create_user.username,
        hashed_password= bcrypt_context.hash(create_user.password),
        role=create_user.role
    )
    db.add(create_user_model)
    db.commit()
    return {"message":"User Created Successfully"}

@router.post("/token", response_model=Token,status_code=status.HTTP_200_OK)
async def create_token(formdata:Annotated[OAuth2PasswordRequestForm,Depends()],db:Annotated[Session,Depends(get_db1)]):
    user= authenticate_user(formdata.username,formdata.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not authorized")
    token=create_access_token(user.username,user.id,user.role,timedelta(minutes=60))
    return {"access_token":token,"token_type":"bearer"}

# @router.get("/user_detail",status_code=status.HTTP_200_OK)
# async def current_user_detail(db_pdc:Annotated[Session,Depends(get_db)],db_auth:Annotated[Session,Depends(get_db1)],user:Annotated[dict,Depends(get_current_user)]):
#     user_details=db_auth.query(Users).filter(Users.id==user.get("id")).first()
#     if user_details.role=="-":
#         PDC_role= db_pdc.query(PDC_USERS).filter(PDC_USERS.NT_ID==user.get("username")).first()
#         if not PDC_role:
#             return user_details
#         user_details.role=PDC_role.ROLE
#         db_auth.add(user_details)
#         db_auth.commit()
    
#     return user_details    
    