from flask import Flask
from flask_security import Security, hash_password
from flask_restful import Api
from controllers.database import db
from controllers.config import Config
from controllers.user_datastore import user_datastore
from controllers.authentication_api import LoginAPI, LogoutAPI, CompanyRegisterAPI, StudentRegisterAPI
from controllers.crud_api import CompanyAPI, ResumeUploadAPI, StudentAPI, DriveAPI, ApplicationAPI, StudentHistoryCSVAPI,CeleryDemoAPI
from flask_cors import CORS
from flask import send_from_directory

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    security = Security(app, user_datastore)

    api = Api(app, prefix='/api')
    
    with app.app_context():
        db.create_all()

        admin_role = user_datastore.find_or_create_role(name='admin', description='Administrator')
        student_role = user_datastore.find_or_create_role(name='student', description='Student')
        company_role = user_datastore.find_or_create_role(name='company', description='Company')

        if not user_datastore.find_user(email = 'admin@gmail.com'):
            user_datastore.create_user(
                email = 'admin@gmail.com',
                password=hash_password("admin123"),
                user_type = 'admin',
                roles = [admin_role]
            )
        
        db.session.commit()

    return app, api

app, api = create_app()
apply_cors = CORS(app)

@app.route('/')
def index():
    return {
        'message': 'Welcome to the Placement Portal Website'
    }, 200
@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory("uploads",filename)

api.add_resource(LoginAPI, "/login")

api.add_resource(LogoutAPI, "/logout")

api.add_resource(StudentRegisterAPI, "/student/register")

api.add_resource(CompanyRegisterAPI, "/company/register")

api.add_resource(CompanyAPI, "/company", "/company/<int:company_id>")

api.add_resource(StudentAPI, "/student","/student/<int:student_id>")

api.add_resource(DriveAPI, "/drive", "/drive/<int:drive_id>")

api.add_resource(ApplicationAPI, "/application","/application/<int:app_id>")

api.add_resource(StudentHistoryCSVAPI, "/student/history/csv")

api.add_resource(CeleryDemoAPI, "/celery/demo")

api.add_resource(ResumeUploadAPI,"/student/upload_resume")

if __name__ == '__main__':
    app.run(debug=True)
