from tasks import daily_reminder
from flask_restful import Resource
from flask import request, jsonify, make_response, Response
from flask_security import utils, auth_token_required, roles_required, roles_accepted, current_user
from controllers.user_datastore import user_datastore
from controllers.models import User, Company, Student, Drive, Application
from controllers.database import db
from datetime import datetime
import io
import csv
import os
from werkzeug.utils import secure_filename
import os


class CompanyAPI(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        companies = Company.query.all()
        company_list = []
        for company in companies:
            company_list.append({'id': company.id,'name': company.name,'website': company.website,'hr_contact': company.hr_contact,'status': company.status,'is_blacklisted': company.user.is_blacklisted,'email': company.user.email})

        result = {
            'status': 'success',
            'data': company_list
        }

        return make_response(jsonify(result), 200)

    @auth_token_required
    @roles_required('admin')
    def put(self, company_id):
        company = Company.query.get(company_id)

        if not company:
            result = {
                'status': 'error',
                'message': 'Company does not exist'
            }
            return make_response(jsonify(result), 404)

        data = request.get_json()

        if not data:
            result = {
                'status': 'error',
                'message': 'Data required'
            }
            return make_response(jsonify(result), 400)

        action = data.get('action')

        if action not in ['approve', 'reject', 'blacklist', 'unblacklist']:
            result = {
                'status': 'error',
                'message': 'Invalid action'
            }
            return make_response(jsonify(result), 400)

        if action == 'approve':
            company.status = 'Approved'

        elif action == 'reject':
            company.status = 'Rejected'

        elif action == 'blacklist':
            company.user.is_blacklisted = True

        elif action == 'unblacklist':
            company.user.is_blacklisted = False

        db.session.commit()

        result = {
            'status': 'success',
            'message': f'Company {action} successfully'
        }

        return make_response(jsonify(result), 200)
    
class StudentAPI(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        students = Student.query.all()

        student_list = []
        for student in students:
            student_list.append({'id': student.id,'name': student.name,'education': student.education,'resume_path': student.resume_path,'is_blacklisted': student.user.is_blacklisted,'email': student.user.email})

        result = {
            'status': 'success',
            'data': student_list
        }

        return make_response(jsonify(result), 200)

    @auth_token_required
    @roles_required('student')
    def put(self, student_id):
        student = Student.query.get(student_id)

        if not student:
            result = {
                'status': 'error',
                'message': 'Student profile not found'
            }
            return make_response(jsonify(result), 404)

        if student.user_id != current_user.id:
            result = {
                'status': 'error',
                'message': 'Unauthorized'
            }
            return make_response(jsonify(result), 403)

        data = request.get_json()

        if not data:
            result = {
                'status': 'error',
                'message': 'Data required'
            }
            return make_response(jsonify(result), 400)

        student.name = data.get('name', student.name)
        student.education = data.get('education', student.education)
        student.resume_path = data.get('resume_path', student.resume_path)

        db.session.commit()

        result = {
            'status': 'success',
            'message': 'Profile updated successfully'
        }

        return make_response(jsonify(result), 200)
    
class DriveAPI(Resource):
    @auth_token_required
    @roles_accepted('admin', 'company', 'student')
    def get(self, drive_id=None):
        if drive_id:
            drive = Drive.query.get(drive_id)

            if not drive:
                result = {
                    'status': 'error',
                    'message': 'Drive not found'
                }
                return make_response(jsonify(result), 404)

            result = {
                'status': 'success',
                'data': {'id': drive.id,'company_name': drive.company.name,'company_id': drive.company.id,'title': drive.title,'description': drive.description,'salary': drive.salary,'location': drive.location,'eligibility': drive.eligibility,'deadline': drive.deadline.isoformat() if drive.deadline else None,'status': drive.status}
            }

            return make_response(jsonify(result), 200)

        if current_user.user_type == "student":
            drives = Drive.query.filter_by(status="Active").all()
        else:
            drives = Drive.query.all()

        drive_list = []

        for drive in drives:
            drive_list.append({'id': drive.id,'company_name': drive.company.name,'company_id': drive.company_id,'title': drive.title,'salary': drive.salary,'location': drive.location,'status': drive.status,'deadline': drive.deadline.isoformat() if drive.deadline else None})

        result = {
            'status': 'success',
            'data': drive_list
        }

        return make_response(jsonify(result), 200)

    @auth_token_required
    @roles_required('company')
    def post(self):
        data = request.get_json()

        if not data:
            result = {
                'status': 'error',
                'message': 'Data required'
            }
            return make_response(jsonify(result), 400)

        company = Company.query.filter_by(user_id=current_user.id).first()

        if not company:
            result = {
                'status': 'error',
                'message': 'Company not found'
            }
            return make_response(jsonify(result), 404)

        if company.status != "Approved":
            result = {
                'status': 'error',
                'message': 'Company is not approved'
            }
            return make_response(jsonify(result), 403)

        deadline = None
        if data.get('deadline'):
            deadline = datetime.fromisoformat(data.get('deadline'))

        drive = Drive(company_id=company.id,title=data.get('title'),description=data.get('description'),salary=data.get('salary'),location=data.get('location'),eligibility=data.get('eligibility'),deadline=deadline)

        db.session.add(drive)
        db.session.commit()

        result = {
            'status': 'success',
            'message': 'Drive created successfully'
        }

        return make_response(jsonify(result), 201)

    @auth_token_required
    @roles_required('company')
    def put(self, drive_id):
        drive = Drive.query.get(drive_id)

        if not drive:
            result = {
                'status': 'error',
                'message': 'Drive not found'
            }
            return make_response(jsonify(result), 404)

        company = Company.query.filter_by(user_id=current_user.id).first()

        if drive.company_id != company.id:
            result = {
                'status': 'error',
                'message': 'Unauthorized'
            }
            return make_response(jsonify(result), 403)

        data = request.get_json()

        if not data:
            result = {
                'status': 'error',
                'message': 'Data required'
            }
            return make_response(jsonify(result), 400)

        action = data.get('action')

        if action == "complete":

            if drive.status == "Completed":
                result = {
                    'status': 'error',
                    'message': 'Drive already completed'
                }
                return make_response(jsonify(result), 400)

            drive.status = "Completed"

        else:
            result = {
                'status': 'error',
                'message': 'Invalid action'
            }
            return make_response(jsonify(result), 400)

        db.session.commit()

        result = {
            'status': 'success',
            'message': 'Drive marked as completed'
        }

        return make_response(jsonify(result), 200)
        
class ApplicationAPI(Resource):
    @auth_token_required
    @roles_accepted('admin', 'company', 'student')
    def get(self, app_id=None):
        if app_id:
            application = Application.query.get(app_id)

            if not application:
                result = {
                    'status': 'error',
                    'message': 'Application not found'
                }
                return make_response(jsonify(result), 404)

            if current_user.user_type == "student":
                student = Student.query.filter_by(user_id=current_user.id).first()

                if not student or application.student_id != student.id:
                    result = {
                        'status': 'error',
                        'message': 'Unauthorized'
                    }
                    return make_response(jsonify(result), 403)

            elif current_user.user_type == "company":
                company = Company.query.filter_by(user_id=current_user.id).first()

                if not company or application.drive.company_id != company.id:
                    result = {
                        'status': 'error',
                        'message': 'Unauthorized'
                    }
                    return make_response(jsonify(result), 403)

            result = {
                'status': 'success',
                'data': {'id': application.id,'student_name': application.student.name,'education': application.student.education,'resume':f'http://127.0.0.1:5000/uploads/{os.path.basename(application.student.resume_path)}' if application.student.resume_path else None,'drive_title': application.drive.title,'company_name': application.drive.company.name,'date': application.date.isoformat() if application.date else None,'status': application.status}
            }

            return make_response(jsonify(result), 200)

        if current_user.user_type == "student":
            student = Student.query.filter_by(user_id=current_user.id).first()

            if not student:
                result = {
                    'status': 'error',
                    'message': 'Student not found'
                }
                return make_response(jsonify(result), 404)

            applications = Application.query.filter_by(student_id=student.id).all()

        elif current_user.user_type == "company":
            company = Company.query.filter_by(user_id=current_user.id).first()

            if not company:
                result = {
                    'status': 'error',
                    'message': 'Company not found'
                }
                return make_response(jsonify(result), 404)

            applications = Application.query.join(Drive).filter(
                Drive.company_id == company.id
            ).all()

        else:
            applications = Application.query.all()

        application_list = []

        for application in applications:
            application_list.append({'id': application.id,'student_name': application.student.name,'education': application.student.education,'resume': application.student.resume_path,'drive_title': application.drive.title,'drive_id': application.drive.id,'company_name': application.drive.company.name,'date': application.date.isoformat() if application.date else None,'status': application.status})

        result = {
            'status': 'success',
            'data': application_list
        }

        return make_response(jsonify(result), 200)

    @auth_token_required
    @roles_required('student')
    def post(self):
        data = request.get_json()

        if not data:
            result = {
                'status': 'error',
                'message': 'Data required'
            }
            return make_response(jsonify(result), 400)

        drive_id = data.get('drive_id')

        if not drive_id:
            result = {
                'status': 'error',
                'message': 'Drive ID required'
            }
            return make_response(jsonify(result), 400)

        student = Student.query.filter_by(user_id=current_user.id).first()

        if not student:
            result = {
                'status': 'error',
                'message': 'Student not found'
            }
            return make_response(jsonify(result), 404)

        drive = Drive.query.get(drive_id)

        if not drive:
            result = {
                'status': 'error',
                'message': 'Drive not found'
            }
            return make_response(jsonify(result), 404)

        if drive.status != "Active":
            result = {
                'status': 'error',
                'message': 'Drive is not active'
            }
            return make_response(jsonify(result), 400)

        existing_application = Application.query.filter_by(student_id=student.id,drive_id=drive.id).first()

        if existing_application:
            result = {
                'status': 'error',
                'message': 'You have already applied for this drive'
            }
            return make_response(jsonify(result), 400)

        application = Application(student_id=student.id,drive_id=drive.id)

        db.session.add(application)
        db.session.commit()

        result = {
            'status': 'success',
            'message': 'Applied to drive successfully'
        }

        return make_response(jsonify(result), 201)

    @auth_token_required
    @roles_required('company')
    def put(self, app_id):
        application = Application.query.get(app_id)

        if not application:
            result = {
                'status': 'error',
                'message': 'Application not found'
            }
            return make_response(jsonify(result), 404)

        company = Company.query.filter_by(user_id=current_user.id).first()

        if not company:
            result = {
                'status': 'error',
                'message': 'Company not found'
            }
            return make_response(jsonify(result), 404)

        if application.drive.company_id != company.id:
            result = {
                'status': 'error',
                'message': 'Unauthorized'
            }
            return make_response(jsonify(result), 403)

        data = request.get_json()

        if not data:
            result = {
                'status': 'error',
                'message': 'Data required'
            }
            return make_response(jsonify(result), 400)

        action = data.get('action')

        if action not in ["Shortlist", "Reject", "Select"]:
            result = {
                'status': 'error',
                'message': 'Invalid application status'
            }
            return make_response(jsonify(result), 400)

        application.status = action

        db.session.commit()

        result = {
            'status': 'success',
            'message': f'Application status updated to {action}'
        }

        return make_response(jsonify(result), 200)
    
class StudentHistoryCSVAPI(Resource):

    @auth_token_required
    @roles_required('student')
    def get(self):

        student = Student.query.filter_by(user_id=current_user.id).first()

        if not student:
            result = {
                'status': 'error',
                'message': 'Student not found'
            }
            return make_response(jsonify(result), 404)

        applications = Application.query.filter_by(student_id=student.id).all()

        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow([
            'Drive',
            'Company',
            'Status',
            'Applied On'
        ])

        for application in applications:
            writer.writerow([
                application.drive.title,
                application.drive.company.name,
                application.status,
                application.date.isoformat() if application.date else ''
            ])

        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={
                'Content-Disposition': 'attachment; filename=ApplicationHistory.csv'
            }
        )

class CeleryDemoAPI(Resource):

    @auth_token_required
    @roles_required('admin')
    def post(self):

        daily_reminder.delay()

        result = {
            "status": "success",
            "message": "Background task started"
        }

        return make_response(jsonify(result), 202)

class ResumeUploadAPI(Resource):

    @auth_token_required
    @roles_required("student")
    def post(self):

        if "resume" not in request.files:

            result = {
                "status": "error",
                "message": "No file uploaded"
            }

            return make_response(jsonify(result),400)

        file = request.files["resume"]

        if file.filename == "":

            result = {
                "status":"error",
                "message":"No file selected"
            }

            return make_response(jsonify(result),400)

        filename = secure_filename(file.filename)

        path = os.path.join("uploads",filename)

        file.save(path)

        student = Student.query.filter_by(user_id=current_user.id).first()

        student.resume_path = path

        db.session.commit()

        result = {
            "status":"success",
            "message":"Resume uploaded successfully"
        }

        return make_response(jsonify(result),200)