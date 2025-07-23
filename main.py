import models
from routers import auth,PDC,admin
from database import engine_auth
from fastapi import FastAPI


#models.Base.metadata.create_all(engine_auth)

app= FastAPI()

app.include_router(auth.router)
app.include_router(PDC.router)
app.include_router(admin.router)
