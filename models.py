from database import Base
from sqlalchemy import Column,Integer,String,Boolean,DateTime,BIGINT,ForeignKey,TIMESTAMP, Text, Date
from datetime import datetime

class MstrLogin(Base):
    __tablename__="mstr_login"
    id=Column(Integer,primary_key=True,index=True)
    role_id=Column(Integer,ForeignKey("mstr_role.id"))
    email=Column(String(255))
    first_name=Column(String(255))
    last_name=Column(String(255))
    is_active=Column(Boolean,default=False,nullable=False)
    password=Column(String(255))
    created_at=Column(TIMESTAMP,default=datetime.now())
    contact_number=Column(BIGINT)


class   MstrRole(Base):
    __tablename__="mstr_role"
    id=Column(Integer,primary_key=True,index=True)
    role_name=Column(String(255))
    created_at=Column(TIMESTAMP,default=datetime.now())


class MstrUser(Base):
    __tablename__="mstr_user"
    id=Column(Integer,primary_key=True,index=True)
    login_id=Column(Integer)
    user_type_id=Column(Integer)
    ref_id=Column(Integer)
    role_type=Column(String(255))
    department_id=Column(Integer)
    designation_id=Column(Integer)

class TokenModel(Base):
    __tablename__='mstr_token'
    id=Column(Integer,primary_key=True,index=True)
    token=Column(String(255),unique=True)
    user_id=Column(Integer)
    created_at=Column(DateTime)


class MotorClaimDetails(Base):
    __tablename__ = 'motor_claim_details'
    id = Column(BIGINT, primary_key=True, index=True,nullable=False)
    claim_no = Column(String(255))
    product_id = Column(Integer)
    policy_number = Column(String(255))
    customer_mobile_no = Column(BIGINT)
    status=Column(String(50))
    insurer_id=Column(Integer)
    customer_id=Column(Integer)

class MotorClaimFormDetails(Base):
    __tablename__ = 'motor_claim_form_details'
    id=Column(BIGINT, primary_key=True, index=True,nullable=False)
    motor_claim_details_id=Column(Integer)

class MstrCustomer(Base):
    __tablename__="mstr_customer"
    id=Column(BIGINT, primary_key=True, index=True,nullable=False)
    name=Column(String(255))

class MstrProduct(Base):
    __tablename__="mstr_product"
    id=Column(BIGINT, primary_key=True, index=True,nullable=False)
    category=Column(String(255))
    workflow_id=Column(Integer)

class WorkFlowStep(Base):
    __tablename__="workflow_steps"
    id=Column(BIGINT, primary_key=True, index=True,nullable=False)
    workflow_id=Column(Integer)
    name=Column(String(255))
    route=Column(String(255))
    child=Column(String(255))
    role_id=Column(BIGINT)

class MstrInsurense(Base):
    __tablename__="mstr_insurer"
    id=Column(BIGINT, primary_key=True, index=True,nullable=False)
    name=Column(String(255))

class FormSteps(Base):
    __tablename__="form_steps"
    id=Column(BIGINT,primary_key=True,index=True,nullable=False)
    title=Column(String(255))
    description=Column(String(255))
    form_id=Column(Integer)
    position=Column(Integer)
    created_by=Column(Integer)
    created_at=Column(TIMESTAMP,default=datetime.now())

class FormFields(Base):
    __tablename__="form_fields"
    id=Column(Integer,primary_key=True)
    form_id =Column(Integer)
    field_name=Column(String(255))
    field_type=Column(String(50))
    label =Column(String(255))
    placeholder=Column(String(255))
    position=Column(Integer)
    created_by=Column(Integer)
    created_at=Column(DateTime)
    field_input_type=Column(String(50))
    select_file_type=Column(String(50))
    is_active=Column(Boolean)
    step_id=Column(Integer)
    field_category=Column(String(10))


class FormDetails(Base):
    __tablename__="form_details"
    id=Column(Integer,primary_key=True)
    name=Column(String(255))
    description=Column(Text)
    created_by=Column(Integer)
    created_at=Column(DateTime)
    product_id=Column(Integer)
    insurer=Column(Integer)
    form_render_type=Column(String(100))
    
class FormFeildValidations(Base):
    __tablename__="form_field_validations"
    id=Column(Integer,primary_key=True)
    field_id=Column(Integer)
    validation_type=Column(String(50))
    validation_value=Column(String(255))
    error_message=Column(String(255))
    created_by=Column(Integer)
    created_at=Column(DateTime)

class FormFieldOptions(Base):
    __tablename__="form_field_options"
    id=Column(Integer,primary_key=True)
    field_id=Column(Integer)
    option_value=Column(String(255))
    option_label=Column(String(255))
    created_by=Column(Integer)
    created_at=Column(DateTime)

class GetCountry(Base):
    __tablename__="mstr_country"
    id=Column(Integer,primary_key=True,index=True)
    country_name=Column(String(255))
    created_by=Column(Integer)
    created_at=Column(TIMESTAMP,default=datetime.now())    

class GetState(Base):
    __tablename__="mstr_state"
    id=Column(Integer,primary_key=True,index=True,nullable=False)
    state_name=Column(String(255))
    country_id=Column(Integer,ForeignKey("mstr_country.id"))
    created_by=Column(Integer)
    created_at=Column(TIMESTAMP,default=datetime.now())

class GetCity(Base):
    __tablename__="mstr_city"
    id=Column(Integer,primary_key=True,index=True,nullable=False)
    city_name=Column(String(255))
    state_id=Column(Integer,ForeignKey("mstr_state.id"))
    created_by=Column(Integer)
    created_at=Column(TIMESTAMP,default=datetime.now())   

class GetDocument(Base):
    __tablename__="mstr_document"
    id=Column(Integer,primary_key=True,index=True,nullable=False)
    file_name=Column(String(255))
    path=Column(String(255))
    is_verified=Column(Boolean)
    module_name=Column(String(255))     
    created_by=Column(Integer)
    created_at=Column(TIMESTAMP,default=datetime.now())   

class GetZone(Base):
    __tablename__="mstr_zone"
    id=Column(Integer,primary_key=True,index=True,nullable=False)
    name=Column(String(255))
    created_by=Column(Integer)
    created_at=Column(TIMESTAMP,default=datetime.now())

class GetDepartment(Base):
    __tablename__="mstr_department"
    id=Column(Integer,primary_key=True,index=True,nullable=False)
    name=Column(String(255))
    created_by=Column(Integer)
    created_at=Column(TIMESTAMP,default=datetime.now())

# class GetRole(Base):
#     __tablename__='mstr_role'
#     id=Column(Integer,primary_key=True,index=True,nullable=False)
#     role_name=Column(String(255))
#     created_at=Column(TIMESTAMP,default=datetime.now())    

class MstrDesignation(Base):
    __tablename__='mstr_designation'
    id=Column(Integer,primary_key=True,index=True,nullable=False)
    designation_name=Column(String(255))
    created_by=Column(Integer)
    created_at=Column(TIMESTAMP,default=datetime.now())

# class UpdateIcgmsUser(Base):
#     __tablename__="mstr_icgms_users"
#     id=Column(BIGINT,primary_key=True,nullable=False)
#     employee_no=Column(String(255))
#     first_name=Column(String(255))
#     last_name=Column(String(255))
#     designation=Column(String(255))
#     department_id=Column(Integer)
#     branch_id=Column(Integer)
#     city_id=Column(Integer)
#     zone_id=Column(Integer)
#     country_id=Column(Integer)
#     servicing_location=Column(String(255))
#     rm_emp_id=Column(Integer)
#     official_email=Column(String(255))
#     official_phone_no=Column(BIGINT)
#     whatsapp_no=Column(BIGINT)
#     role_id=Column(Integer)
#     personal_email=Column(String(255)) 
#     personal_phone_1=Column(Integer) 
#     personal_phone_2=Column(Integer)  
#     blood_group=Column(String(255))  
#     gender=Column(String(255))   
#     address= Column(String(255))   
#     resident_location=Column(String(255)) 
#     pincode=Column(Integer)
#     aadhaar_no= Column(Integer) 
#     pan_no=Column(String(255)) 
#     passport_no=Column(String(255)) 
#     dl_no=Column(String(255)) 
#     created_at=Column(TIMESTAMP,default=datetime.now())

class AddMasterBranch(Base):
    __tablename__="mstr_branch"
    id= Column(Integer, primary_key=True)
    created_by= Column(Integer, nullable= False)
    created_at= Column(TIMESTAMP,default=datetime.now())
    branch_code= Column(Integer, nullable= False)
    branch_name= Column(String(255), nullable= False)
    country_id = Column(Integer,ForeignKey("mstr_country.id"), nullable= False)
    city_id= Column(Integer,ForeignKey("mstr_city.id"), nullable= False)
    state_id= Column(Integer,ForeignKey("mstr_state.id"), nullable= False)
    zone_id= Column(Integer, ForeignKey("mstr_zone.id"), nullable= False)
    pincode= Column(Integer, nullable= False)
    latitude= Column(Integer, nullable= False,default=1)
    longitude= Column(Integer, nullable= False,default=111)
    status= Column(Boolean, nullable= False)
    address= Column(String(255), nullable= False)

class MstrUserType(Base):
    __tablename__='mstr_user_type'
    id=Column(Integer,primary_key=True,index=True)
    user_type=Column(String(255))
    created_by=Column(Integer,nullable=False)
    created_at=Column(TIMESTAMP,default=datetime.now())




