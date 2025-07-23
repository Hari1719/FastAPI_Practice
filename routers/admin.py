from fastapi import APIRouter,HTTPException,Depends
from starlette import status
from database import SessionLocal_pdc,SessionLocal_auth
from typing import Annotated
from sqlalchemy.orm import Session
from .auth import get_current_user
from models import Users,PDCData

router=APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


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

user_dependencies=Annotated[dict,Depends(get_current_user)]

@router.get("/pdc/{pdc_id}",status_code=status.HTTP_200_OK)
async def get_pdcdetail_withID(pdc_id:str,user:user_dependencies,db_pdc:Annotated[Session,Depends(get_db)],db_auth:Annotated[Session,Depends(get_db1)]):
    user_details=db_auth.query(Users).filter(Users.id==user.get("id")).first()
     
    if str(user_details.role).lower() == "admin":
        pdc_data=db_pdc.query(PDCData).filter(PDCData.PDC_ID==pdc_id).first()
     
        if not pdc_data:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Requested PDC id not found")
        return pdc_data
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not authorized to view this PDC")