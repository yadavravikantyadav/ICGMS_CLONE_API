from fastapi import FastAPI
from database import engine,Base
import authentication
from routers import superadmin,user_master,master_branch,manage_user_master
from fastapi.responses import RedirectResponse
# from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="ICGMS DEVELOPMENT API (CLONE)", description="This is a development API for ICGMS", version="1.0.0")
Base.metadata.create_all(bind=engine)

# app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:4200"], 
# allow_credentials=True, 
# allow_methods=["*"], 
#  allow_headers=["*"],)

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

app.include_router(authentication.router)
app.include_router(superadmin.router)
app.include_router(user_master.router)
app.include_router(master_branch.router)
app.include_router(manage_user_master.router)

