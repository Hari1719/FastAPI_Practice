from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL='sqlite:///./todosapp.db'



engine_auth=create_engine(SQLALCHEMY_DATABASE_URL,connect_args={'check_same_thread':False})
engine_pdc=create_engine(SQLALCHEMY_DATABASE_URL_pdc)

SessionLocal_auth=sessionmaker(autocommit=False,autoflush=False,bind=engine_auth)
SessionLocal_pdc=sessionmaker(autocommit=False,autoflush=False,bind=engine_pdc)

Base=declarative_base()