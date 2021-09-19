import enum

from app import db

class Gender(enum.Enum):
    # https://docs.sqlalchemy.org/en/14/core/type_basics.html#sqlalchemy.types.Enum
    # Enum names are persisted, not values.
    Other = 1
    Male = 2
    Female = 3

class Student(db.Model):
    id = db.Column(db.CHAR(9), primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    course = db.Column(db.String(10), db.ForeignKey('course.code'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    # https://stackoverflow.com/questions/44343431/flask-sqlalchemy-enum-field-default-value
    # Enums in SQLAlchemy carry the enum when queried, bringing some clunk in the process.
    # Subject to change.
    gender = db.Column(db.Enum(Gender), nullable=False, server_default='Other')

    # https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
    # The __repr__ method tells Python how to print objects of this class
    def __repr__(self):
        return '<Student {}>'.format(self.id)

class Course(db.Model):
    code = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    college = db.Column(db.String(5), nullable=False)
    # backref cannot be the same as a key in the other table :(
    students = db.relationship('Student', backref='course_code', lazy='dynamic')

    def __repr__(self):
        return '<Course {}>'.format(self.code)
