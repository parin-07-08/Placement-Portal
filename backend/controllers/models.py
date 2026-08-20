from controllers.database import db
from flask_security import UserMixin , RoleMixin

user_roles = db.Table('user_roles',
    db.Column('id', db.Integer(), primary_key=True),                   
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))                 
    )

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(),primary_key=True)
    email = db.Column(db.String(255),unique=True,nullable=False)
    password = db.Column(db.String(255),nullable=False)
    active = db.Column(db.Boolean(),default=True)
    is_blacklisted = db.Column(db.Boolean,default=False)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    fs_token_unquifier = db.Column(db.String(255), unique=True, nullable=True)

    user_type = db.Column(db.String(20), nullable=False)
    roles = db.relationship('Role', secondary=user_roles, backref=db.backref('users', lazy='dynamic'))

class Student(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), unique=True,nullable=False)
    name = db.Column(db.String(25), nullable=False)
    education = db.Column(db.String(100),nullable=False)
    resume_path = db.Column(db.String(255))

    user = db.relationship('User', backref=db.backref('student'), uselist=False)

class Company(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), unique=True,nullable=False)
    name = db.Column(db.String(25), nullable=False)
    website = db.Column(db.String(255))
    hr_contact = db.Column(db.String(20))
    status = db.Column(db.String(20),default='Pending')

    user = db.relationship('User', backref=db.backref('company'), uselist=False)

class Drive(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    company_id = db.Column(db.Integer,db.ForeignKey('company.id'),nullable=False)
    title = db.Column(db.String(40),nullable=False)
    description = db.Column(db.String(300),nullable=False)
    salary = db.Column(db.Integer(),nullable=False)
    location = db.Column(db.String(40),nullable=False)
    eligibility = db.Column(db.String(200),nullable=False)
    deadline = db.Column(db.DateTime)
    status = db.Column(db.String(50),default='Active')

    company = db.relationship('Company', backref=db.backref('drives', lazy=True))

class Application(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    student_id = db.Column(db.Integer,db.ForeignKey('student.id'),nullable=False)
    drive_id = db.Column(db.Integer,db.ForeignKey('drive.id'),nullable=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.String(50),default='Applied')
    __table_args__ = (db.UniqueConstraint('student_id','drive_id',name='unique_student_drive'),)

    drive = db.relationship('Drive', backref=db.backref('applications', lazy=True))
    student = db.relationship('Student', backref=db.backref('applications', lazy=True))