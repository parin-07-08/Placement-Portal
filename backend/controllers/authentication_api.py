from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import utils, auth_token_required, roles_required, hash_password
from controllers.user_datastore import user_datastore
from controllers.models import Student,Company
from controllers.database import db

class LoginAPI(Resource):
    def post(self):
        details = request.get_json()

        if not details:
            result = {
                'status': 'error',
                'message': 'Login Credentials are required'
            }
            return make_response(jsonify(result),400)
        
        email = details.get('email')
        password = details.get('password')

        if not email or not password:
            result = {
                'status':'error',
                'message':'Both Email and Password are Required.'
            }
            return make_response(jsonify(result),400)

        user = user_datastore.find_user(email=email)
        if not user:
            result = {
                'status':'error',
                'message':'User does not exist'
            }
            return make_response(jsonify(result),404)
        
        if user.is_blacklisted:
            result = {
                'status': 'error',
                'message': 'Account is black-listed'
            }
            return make_response(jsonify(result),403)
        
        company = Company.query.filter_by(user_id=user.id).first()
        if (user.user_type == 'company' and company.status != "Approved"):
            result = {
                'status': 'error',
                'message': 'Company not approved by admin'
            }
            return make_response(jsonify(result,403))
        
        if not utils.verify_password(password,user.password):
            result = {
                'status':'error',
                'message':'Password Incorrect'
            }
            return make_response(jsonify(result),401)
        
        auth_token = user.get_auth_token()
        utils.login_user(user)
        response = {
            'message': 'Login successful',
            'user_details': {
                'id': user.id,
                'email': user.email,
                'user_type': user.user_type,
                'roles': [role.name for role in user.roles],
                'auth_token': auth_token
            }
        }
        return make_response(jsonify(response), 200)
    
class LogoutAPI(Resource):
    @auth_token_required
    def post(self):
        utils.logout_user()
        response = {
            'message' : 'Logout successful'
        }
        return make_response(jsonify(response), 200)
    
class StudentRegisterAPI(Resource):
    def post(self):
        details = request.get_json()

        if not details:
            result = {
                'status': 'error',
                'message': 'Registration Details are required'
            }
            return make_response(jsonify(result),400)
        
        email = details.get('email')
        password = details.get('password')
        user_type = 'student'
        name = details.get('name')
        education = details.get('education')
        
        if not all([email, password, name, education]):
            result = {
                'status':'error',
                'message':'All Details are required'
            }
            return make_response(jsonify(result),400)
        
        if user_datastore.find_user(email=email):
            result = {
                'message' : 'User already exsists',
                'status' : 'error'
            }
            return make_response(jsonify(result), 400)
        
        user_role = user_datastore.find_role('student')
        user_datastore.create_user(
            email=email,
            password=hash_password(password),
            user_type=user_type,
            roles=[user_role],
        )
        db.session.commit()
        user = user_datastore.find_user(email=email)
        student = Student(user_id=user.id,name=name,education=education)
        db.session.add(student)
        db.session.commit()
        result = {
            'status': 'success',
            'message': 'Student registered successfully',
            'user_details': {
                'id': user.id,
                'email': user.email,
                'user_type': user.user_type,
                'roles': [role.name for role in user.roles],
                'student_id': student.id}
            }
        return make_response(jsonify(result), 201)

class CompanyRegisterAPI(Resource):

    def post(self):
        details = request.get_json()

        if not details:
            result = {
                'status': 'error',
                'message': 'Registration Details are required'
            }
            return make_response(jsonify(result),400)
        
        email = details.get('email')
        password = details.get('password')
        user_type = 'company'
        name = details.get('name')
        website = details.get('website')
        hr = details.get('hr')
        
        if not all([email, password, name, website, hr]):
            result = {
                'status':'error',
                'message':'All Details are required'
            }
            return make_response(jsonify(result),400)
        
        if user_datastore.find_user(email=email):
            result = {
                'message' : 'User already exsists',
                'status' : 'error'
            }
            return make_response(jsonify(result), 400)
        
        user_role = user_datastore.find_role('company')
        user_datastore.create_user(
            email=email,
            password=hash_password(password),
            user_type=user_type,
            roles=[user_role],
        )
        db.session.commit()
        user = user_datastore.find_user(email=email)
        company = Company(user_id=user.id,name=name,website=website,hr_contact=hr,status="Pending")
        db.session.add(company)
        db.session.commit()
        result = {
            'status': 'success',
            'message': 'Company registered successfully',
            'user_details': {
                'id': user.id,
                'email': user.email,
                'user_type': user.user_type,
                'roles': [role.name for role in user.roles],
                'company_id': company.id}
            }
        return make_response(jsonify(result), 201)