from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL='sqlite:///./todosapp.db'


SQLALCHEMY_DATABASE_URL_pdc = "oracle+oracledb://CM_EDWH_D:2022hzu+Zs@rb0orarac35.de.bosch.com:38000/?service_name=AST410_rb0orarac35.de.bosch.com"

engine_auth=create_engine(SQLALCHEMY_DATABASE_URL,connect_args={'check_same_thread':False})
engine_pdc=create_engine(SQLALCHEMY_DATABASE_URL_pdc)

SessionLocal_auth=sessionmaker(autocommit=False,autoflush=False,bind=engine_auth)
SessionLocal_pdc=sessionmaker(autocommit=False,autoflush=False,bind=engine_pdc)

Base=declarative_base()