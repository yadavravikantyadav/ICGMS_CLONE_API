from Token import Create_token
from fastapi import APIRouter,HTTPException,status,Depends
from hashing import Hash
from datetime import datetime
from sqlalchemy.orm import Session
from database import get_db 
from models import MstrUser,MstrRole,TokenModel,MstrLogin
from schemas import Login_token


router=APIRouter(tags=['Superadmin'])
@router.post("/token/{user_type_id}")
def Login_for_access_token(request:Login_token,user_type_id:int,db:Session=Depends(get_db)):
    user=db.query(MstrLogin).filter(MstrLogin.email==request.email,MstrLogin.role_id==user_type_id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credentials")
    
    role=db.query(MstrRole).filter(MstrRole.id==user_type_id).first()

    if not Hash.verify_password(request.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Password")

    access_token=Create_token(data={'email':user.email,"role_id":user_type_id,"user_role":role.role_name})
    print("Generated Token:", access_token)
    data=TokenModel(token=access_token,user_id=user.id,created_at=datetime.now())
    db.add(data)
    db.commit()
    return {"access_token":access_token,"bearer":"bearer","role_id":user_type_id,"role":role.role_name}