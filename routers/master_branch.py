from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.orm import Session
from database import get_db
from models import AddMasterBranch
from oauth2 import get_current_user,user_dependency
from schemas import branch, GetBranchShcema,UpdateBranchSchema,DeleteBranchSchema

router=APIRouter(tags=["Master Branch"])

@router.post("/add-master-branch")
def add_master_branch(request: branch, db: Session = Depends(get_db)):
    master_branch= AddMasterBranch(branch_code = request.branch_code,
                            branch_name = request.branch_name,
                            city_id = request.city,
                            state_id= request.state,
                            country_id= request.country,
                            zone_id= request.zone,
                            pincode= request.pin_code,
                            address= request.address,
                            created_by= request.created_by,
                            status= request.status,
                            latitude= request.latitude,
                            longitude= request.longitude
                            )
    db.add(master_branch)
    db.commit()
    db.refresh(master_branch)
    return {
          "status": master_branch.status,
          "msg":" branch added successfully"
       
    }

@router.post("/get_master_branch")
def Get_Master_Branch(request:GetBranchShcema,db:Session=Depends(get_db)):
    if request.record_per_page<=0:
        return {"error":"record_per_page must be greater than 0"}
    offset=((request.page_number )-1) * request.record_per_page
    if request.page_number<=0:
        return {"error":'page_number must be greater than 0'}
    branches=db.query(AddMasterBranch).offset(offset).limit(request.record_per_page).all()
    return{"branches":branches}

    
@router.post('/update_master_branch/{id}')    
def update_branch(id: int, request: UpdateBranchSchema, db: Session = Depends(get_db)):
    # Fetch the branch by ID
    branch = db.query(AddMasterBranch).filter(AddMasterBranch.id == id).first()
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")

    # Update branch fields with request data
    branch.branch_code = request.branch_code
    branch.branch_name = request.branch_name
    branch.city_id = request.city_id
    branch.state_id = request.state_id
    branch.country_id = request.country_id
    branch.zone_id = request.zone_id
    branch.pincode = request.pincode
    branch.address = request.address
    branch.status = request.status

    # Commit the changes to the database
    db.commit()
    db.refresh(branch)
    return {"message": "Branch updated successfully", "branch": branch}    


@router.post('/get_branch_by_id/{id}')
def Get_Branch_Data(id:int,db:Session=Depends(get_db)):
    query=db.query(AddMasterBranch).filter(AddMasterBranch.id==id).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"query with {id} is not found")
    return query
    
@router.post('/delete_branch')
def Delete_Branch_Data(request:DeleteBranchSchema,db:Session=Depends(get_db)):
    query=db.query(AddMasterBranch).filter(AddMasterBranch.id==request.delete_id).delete()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'query with {id} is not found')
    db.commit()
    return 'done' 
