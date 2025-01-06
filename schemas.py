from pydantic import BaseModel
from datetime import datetime

class User_Schema(BaseModel):
    id:int
    email:str
    first_name:str
    last_name:str
    is_active:bool

    class Config:
        orm_mode=True


class Count_User_Schema(BaseModel):
    email:str
    password:str
    
    class Config:
        orm_mode=True

class login_response(BaseModel):
    role:str
    role_id:int
    no_of_role:int    

class Login_token(BaseModel):
    email:str
    password:str  

class TokenData(BaseModel):
    email:str=None
    role_id:int=None
    role_name:str=None

    class Config:
        orm_mode=True      

class GetStateSchema(BaseModel):
    country_id:int

class GetCitiySchema(BaseModel):
    state_id:int    

# class UpdateIcgmsSchema(BaseModel):
#     id:int
#     employee_no: str
#     first_name: str
#     last_name: str
#     designation: str
#     department_id: int
#     branch_id: int
#     city_id: int
#     zone_id: int
#     country_id: int
#     servicing_location: str
#     rm_emp_id: int
#     official_email: str
#     official_phone_no: int
#     whatsapp_no: int
#     role_id: int
#     personal_email: str
#     personal_phone_1: int
#     personal_phone_2: int
#     blood_group: str
#     gender: str
#     address: str
#     resident_location: str
#     pincode: int
#     aadhaar_no: int
#     pan_no: str
#     passport_no: str
#     dl_no: str
       
class branch(BaseModel): 
  branch_code: int
  branch_name: str
  city: int
  state: int
  country: int
  zone:int
  pin_code: int
  address: str
  created_by: int
  status: bool
  latitude: int
  longitude: int


class GetBranchShcema(BaseModel):
    record_per_page:int
    page_number:int


class UpdateBranchSchema(BaseModel):
    branch_code: str 
    branch_name: str 
    city_id: int 
    state_id: int 
    country_id: int 
    zone_id: int 
    pincode: int 
    address: str 
    status: bool 

class DeleteBranchSchema(BaseModel):
    delete_id:int

class AddManageUserSchema(BaseModel):
    pass    