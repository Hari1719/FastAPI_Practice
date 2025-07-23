from database import Base
from sqlalchemy import Column,Integer,String,TIMESTAMP


class Users(Base):
    
    __tablename__ = "users"
    
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String(2000))
    hashed_password=Column(String(2000))
    role=Column(String(100))

class PDCData(Base):
    __tablename__ = "PDC"  # Replace with actual table name

    PDC_ID=Column(String(100),primary_key=True)
    SUMMARY = Column(String(2010))
    DESCRIPTION = Column(String(2000))
    PROJECT_ID = Column(String(100))
    TEMPLATE_ID = Column(String(100))
    CREATED_BY = Column(String(100))
    CREATED_ON = Column(TIMESTAMP)
    STATUS_ID = Column(String(100))
    REVIEWED_BY = Column(String(100))
    REVIEWED_ON = Column(TIMESTAMP)
    REVIEWER_COMMENT = Column(String(2000))
    PDCGROUPS_ID = Column(String(255))
    WORK_ITEM_ID = Column(String(255))
    WORK_ITEM_TYPE = Column(String(255))
    SCRIPT_EXECUTION = Column(String(20))
    ARCHIVED = Column(String(20))
    SCRIPTERROR_REASON = Column(String(100))
    CREATED_BY_NAME = Column(String(200))
    REVIEWED_BY_NAME = Column(String(200))
    COMPONENT_NAME = Column(String(200))
    WORKITEM_COUNT = Column(Integer)
    
class PDC_USERS(Base):
    __tablename__="PDC_USERS"
    
    NT_ID= Column(String(100),primary_key=True)
    ROLE= Column(String(100))