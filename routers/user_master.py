from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.orm import Session
from database import get_db
from models import GetCountry,GetState,GetCity,GetDocument,GetZone,GetDepartment,MstrRole,MstrDesignation
from schemas import GetStateSchema,GetCitiySchema

router=APIRouter(tags=['User Master'])

@router.post("/get_countries")
def Get_countries(db:Session=Depends(get_db)):
    qury=db.query(GetCountry).all()
    return qury

@router.post("/get_states")
def Get_states(state:GetStateSchema,db:Session=Depends(get_db)):
    query=db.query(GetState).filter(GetState.country_id==state.country_id).all()
    return query

@router.post("/get_cities")
def Get_cities(city:GetCitiySchema,db:Session=Depends(get_db)):
    query=db.query(GetCity).filter(GetCity.state_id==city.state_id).all()
    return query

@router.post('/get_document')
def Get_document(db:Session=Depends(get_db)):
    query=db.query(GetDocument).all()
    return query

@router.post('/get_zone')
def Get_Zone(db:Session=Depends(get_db)):
    query=db.query(GetZone).all()
    return query

@router.post('/get_department')
def Get_department(db:Session=Depends(get_db)):
    query=db.query(GetDepartment).all()
    return query

@router.post('/get_roles')
def Get_Role_List(db:Session=Depends(get_db)):
    query=db.query(MstrRole).all()
    return query

@router.post('/get_designation')
def Get_designation(db:Session=Depends(get_db)):
    query=db.query(MstrDesignation).all()
    return query

# @router.post('/update_icgms_user',response_model=List[UpdateIcgmsSchema])
# def Update_Icgms_User(request:UpdateIcgmsSchema,db:Session=Depends(get_db)):
#     query=UpdateIcgmsUser(id=request.id,employee_no=request.employee_no,first_name=request.first_name,last_name=request.last_name,designation=request.designation,department_id=request.department_id,branch_id=request.branch_id,city_id=request.city_id,zone_id=request.zone_id,country_id=request.country_id,official_phone_no=request.official_phone_no)
#     db.add(query)
#     db.commit()
#     db.refresh(query)


