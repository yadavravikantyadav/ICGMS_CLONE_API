from fastapi import APIRouter,Depends,HTTPException,status
from typing import List
from sqlalchemy.orm import Session
from models import  MstrLogin,MstrRole,MstrUser,TokenModel,MotorClaimDetails,MotorClaimFormDetails,MstrCustomer,MstrProduct,WorkFlowStep,MstrInsurense,FormSteps,FormFields,FormDetails,FormFeildValidations,FormFieldOptions
from database import get_db
from hashing import Hash
from schemas import Count_User_Schema,login_response,User_Schema
from oauth2 import get_current_user, user_dependency,oauth2_scheme
import traceback
from datetime import datetime


router=APIRouter(tags=["Superadmin"])

@router.get("/get_all_user", response_model=List[User_Schema])
def get_all_user(user: user_dependency, db: Session = Depends(get_db)):
    try:
        query = db.query(MstrLogin).filter(MstrLogin.is_active != None).all()
        return query
    except Exception as e:
        error_line = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}, Line: {error_line}")  # Line 9


@router.post("/get_count_user", response_model=login_response)
def get_count_user(request: Count_User_Schema, db: Session = Depends(get_db)):
    try:
        user = db.query(MstrLogin).filter(MstrLogin.email == request.email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

        if not Hash.verify_password(request.password, user.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid password")

        role = db.query(MstrRole).filter(MstrRole.id == user.role_id).first()
        no_of_count = db.query(MstrRole).filter(MstrRole.id == user.role_id).count()

        return login_response(role_id=user.role_id, role=role.role_name, no_of_role=no_of_count)
    except Exception as e:
        error_line = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}, Line: {error_line}")  # Line 27


@router.post("/get_MstrUser")
def get_MstrUser(user=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        if not user:
            raise HTTPException(status_code=401, detail="Authentication failed")

        user_details = (
            db.query(
                MstrLogin.id.label("login_id"),
                MstrLogin.email,
                MstrUser.user_type_id,
                MstrUser.ref_id,
                MstrLogin.first_name,
                MstrLogin.last_name,
                MstrLogin.contact_number,
                MstrUser.role_type,
                MstrUser.department_id,
                MstrUser.designation_id,
                MstrRole.role_name
            )
            .join(MstrUser, MstrUser.login_id == MstrLogin.id)
            .join(MstrRole, MstrLogin.role_id == MstrRole.id)
            .filter(MstrLogin.email == user.email)
            .first()
        )
        if not user_details:
            raise HTTPException(status_code=404, detail="User details not found")

        return {
            "login_id": user_details.login_id,
            "email": user_details.email,
            "user_type_id": user_details.user_type_id,
            "ref_id": user_details.ref_id,
            "first_name": user_details.first_name,
            "last_name": user_details.last_name,
            "contact_number": user_details.contact_number,
            "role_type": user_details.role_type,
            "department_id": user_details.department_id,
            "designation_id": user_details.designation_id,
            "role_name": user_details.role_name,
        }
    except Exception as e:
        error_line = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}, Line: {error_line}")  # Line 61


@router.post("/validate_role/{role_id}")
def Validate_Role(role_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        role = db.query(MstrRole).filter(user.role_id == role_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
        elif not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"role {role_id} is not present")
        return role
    except Exception as e:
        error_line = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}, Line: {error_line}")  # Line 78


@router.post("/logout")
def logout(tokens: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        token = tokens.credentials
        db.query(TokenModel).filter(TokenModel.token == token).delete()
        db.commit()
        return {"message": "Logout successfully"}
    except Exception as e:
        error_line = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}, Line: {error_line}")  # Line 90


@router.post("/get_all_claim_list_superadmin")
def Get_all_claim_list_superadmin(db: Session = Depends(get_db)):
    try:
        claim_detail = (
            db.query(
                MotorClaimDetails.id.label("claim_id"),
                MotorClaimDetails.claim_no,
                MotorClaimDetails.product_id,
                MotorClaimDetails.policy_number,
                MotorClaimDetails.customer_mobile_no.label("mobile_no"),
                MotorClaimDetails.insurer_id,
                MotorClaimDetails.status,
                MotorClaimFormDetails.motor_claim_details_id,
                MstrCustomer.name.label('customer_name'),
                MstrProduct.category.label("product_name"),
                WorkFlowStep.workflow_id,
                WorkFlowStep.name.label('workflow_name'),
                WorkFlowStep.route,
                WorkFlowStep.child,
                WorkFlowStep.role_id,
                MstrInsurense.name.label('insurer_name')
            )
            .join(MstrInsurense, MotorClaimDetails.insurer_id == MstrInsurense.id)
            .join(MstrCustomer, MotorClaimDetails.customer_id == MstrCustomer.id)
            .join(MstrProduct, MstrProduct.id == MotorClaimDetails.product_id)
            .join(MotorClaimFormDetails, MotorClaimFormDetails.motor_claim_details_id == MotorClaimDetails.id)
            .join(WorkFlowStep, WorkFlowStep.id == MstrProduct.workflow_id).all()
        )

        result = [{
            "claim_id": detail.claim_id,
            "motor_claim_details_id": detail.motor_claim_details_id,
            "claim_no": detail.claim_no,
            "product_id": detail.product_id,
            "product_name": detail.product_name,
            "policy_number": detail.policy_number,
            "insurer_name": detail.insurer_name,
            "insurer_id": detail.insurer_id,
            "customer_name": detail.customer_name,
            "mobile_no": detail.mobile_no,
            "status": detail.status,
            "workflow_id": detail.workflow_id,
            "route": detail.route,
            "child": detail.child,
            "role_id": detail.role_id,
        } for detail in claim_detail
        ]

        return result
    except Exception as e:
        error_line = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}, Line: {error_line}")  # Line 124



@router.post("/get_dynamic_form/{form_id}")
def Get_dynamic_form(form_id: int, step_id: int, db: Session = Depends(get_db)):
    try:
        # Query to fetch form step data
        form_details = (
            db.query(
                FormDetails.form_render_type.label('form_render_type'),
                FormSteps.id.label('step_id'),
                FormSteps.title.label('step_title'),
                FormFields.label.label('field_label'),
                FormFields.field_name.label('field_name'),
                FormFields.field_type.label('field_type'),
                FormFields.placeholder.label('placeholder'),
                FormFeildValidations.validation_type.label('validation_type'),
                FormFeildValidations.validation_value.label('validation_value'),
                FormFeildValidations.error_message.label('message'),
                FormFieldOptions.option_value.label('option_value'),
                FormFieldOptions.option_label.label('option_label')

            )
            .join(FormSteps, FormSteps.form_id == FormDetails.id)
            .join(FormFields, FormFields.step_id == FormSteps.id)
            .outerjoin(FormFeildValidations, FormFeildValidations.field_id == FormFields.id)
            .outerjoin(FormFieldOptions,FormFieldOptions.field_id==FormFields.id)
            .filter(FormDetails.id == form_id)
            .all()
        )

        if not form_details:
            raise HTTPException(status_code=404, detail="Form not found")

        # Prepare the structured response
        step_data = {
            "form_render_type": form_details[0].form_render_type,
            "step_id": form_details[0].step_id,
            "step_title": form_details[0].step_title,
            "fields": []
        }

        field_map = {}

        for detail in form_details:
            # Create a unique key for each field
            field_key = (detail.field_label, detail.field_name, detail.field_type, detail.placeholder, detail.option_value, detail.option_label)

            if field_key not in field_map:
                field_map[field_key] = {
                    "field_label": detail.field_label,
                    "field_name": detail.field_name,
                    "field_type": detail.field_type,
                    "placeholder": detail.placeholder,
                    "options": [],
                    "validations": []
                }

            # Append validation data
            if detail.validation_type and detail.validation_value and detail.message:
                field_map[field_key]["validations"].append({
                    "validation_type": detail.validation_type,
                    "validation_value": detail.validation_value,
                    "message": detail.message
                })

            
            if detail.option_value and detail.option_label:
                field_map[field_key]["options"].append({
                    "label": detail.option_label,
                    "value": detail.option_value
                })



        # Add fields to step data
        step_data["fields"].extend(field_map.values())

        return step_data

    except Exception as e:
        # Handle exceptions and provide traceback
        error_line = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}, Trace: {error_line}")

@router.post("/server_time")
def Get_server_Time():
    try:
        return{"server_time":datetime.now()}
    except Exception as e:
        error_line=traceback.format_exc()
        print("Error:",str(e),"Line:",error_line)

