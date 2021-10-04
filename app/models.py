# import enum
from itertools import starmap

from flask import current_app

from app import db

class Base(object):
    _ref = 'base'
    _primary = 'id'

    def add(self):
        pass

    def edit(self):
        pass

    @classmethod
    def count_all(cls):
        cursor = db.connection.cursor()
        cursor.execute(f'SELECT COUNT(*) FROM {cls._ref};')
        result = cursor.fetchone()
        return result[0]

    @classmethod
    def get_one(cls, val):
        pass

    @classmethod
    def to_value_label(cls, value, label):
        return (value, f'{label} ({value})')

    @classmethod
    def get_value_label(cls):
        cursor = db.connection.cursor()
        cursor.execute(f'SELECT code, name FROM {cls._ref} ORDER BY code ASC')
        result = cursor.fetchall()
        return list(starmap(cls.to_value_label, result))

    @classmethod
    def get_paginated(cls, page=1, per_page=50, sort='id', order='asc'):
        pass

    @classmethod
    def count_query(cls):
        pass

    @classmethod
    def delete(cls, val):
        try:
            cursor = db.connection.cursor()
            cursor.execute(f'DELETE FROM {cls._ref} WHERE {cls._primary} = %s', (val,))
            db.connection.commit()
            return True
        except:
            return False

    # https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
    # The __repr__ method tells Python how to print objects of this class
    # def __repr__(self):
    #     return '<Student {}>'.format(self._primary)

class Student(Base):
    def __init__(self, id=None, firstname=None, lastname=None, course=None, year=None, gender=None):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.course = course
        self.year = year
        self.gender = gender

    _ref = 'student'
    _primary = 'id'

    YEARS = ['1', '2', '3', '4', '5']
    GENDERS = ['Other', 'Male', 'Female']

    def add(self):
        cursor = db.connection.cursor()
        cursor.execute(
            f'INSERT INTO {self._ref} (id, firstname, lastname, course, year, gender) \
            VALUES (%s, %s, %s, %s, %s, %s);',
            (self.id, self.firstname, self.lastname, self.course, self.year, self.gender))
        db.connection.commit()

    def edit(self, prev_id):
        cursor = db.connection.cursor()
        cursor.execute(
            f'UPDATE {self._ref} \
            SET \
                id = %s, \
                firstname = %s, \
                lastname = %s, \
                course = %s, \
                year = %s, \
                gender = %s \
            WHERE id = %s;',
            (self.id, self.firstname, self.lastname, self.course, self.year, self.gender, prev_id))
        db.connection.commit()

    @classmethod
    def get_one(cls, val):
        cursor = db.connection.cursor()
        cursor.execute(f'SELECT id, firstname, lastname, course, year, gender \
            FROM {cls._ref} WHERE {cls._primary} = %s LIMIT 1', (val,))
        result = cursor.fetchone()
        if result:
            return cls(*result)
        else:
            return False

    @classmethod
    def get_paginated(cls,
        page=1, per_page=50, sort='id', order='asc',
        id=None, firstname=None, lastname=None, course=None, year=None, gender=None):
        params = []
        query = f'SELECT * FROM {cls._ref} '
        if id or firstname or lastname or course or year or gender:
            query += 'WHERE '
            filters = []
            # Make searches for id, firstname, and lastname partial
            if id:
                filters.append('id LIKE %s ')
                params.append(f'%{id}%')
            if firstname:
                filters.append('firstname LIKE %s ')
                params.append(f'%{firstname}%')
            if lastname:
                filters.append('lastname LIKE %s ')
                params.append(f'%{lastname}%')
            if course:
                filters.append('course IN (%s) ')
                params.append(f'{",".join(course)}')
            if year:
                filters.append('year IN (%s) ')
                params.append(f'{",".join(year)}')
            if gender:
                filters.append('gender IN (%s) ')
                params.append(f'{",".join(gender)}')
            query += 'AND '.join(filters)
        query += f'ORDER BY {sort} {order} LIMIT {(page - 1) * per_page}, {per_page};'
        cursor = db.connection.cursor()
        cursor.execute(query, tuple(params) or None)
        result = cursor.fetchall()
        return starmap(cls, result)

    @classmethod
    def count_query(cls,
        id=None, firstname=None, lastname=None, course=None, year=None, gender=None):
        params = []
        query = f'SELECT COUNT(*) FROM {cls._ref} '
        if id or firstname or lastname or course or year or gender:
            query += 'WHERE '
            filters = []
            # Make searches for id, firstname, and lastname partial
            if id:
                filters.append('id LIKE %s ')
                params.append(f'%{id}%')
            if firstname:
                filters.append('firstname LIKE %s ')
                params.append(f'%{firstname}%')
            if lastname:
                filters.append('lastname LIKE %s ')
                params.append(f'%{lastname}%')
            if course:
                filters.append('course IN (%s) ')
                params.append(f'{",".join(course)}')
            if year:
                filters.append('year IN (%s) ')
                params.append(f'{",".join(year)}')
            if gender:
                filters.append('gender IN (%s) ')
                params.append(f'{",".join(gender)}')
            query += 'AND '.join(filters)
        cursor = db.connection.cursor()
        cursor.execute(query, tuple(params) or None)
        result = cursor.fetchone()
        return result[0]

class Course(Base):
    def __init__(self, code=None, name=None, college=None):
        self.code = code
        self.name = name
        self.college = college

    _ref = 'course'
    _primary = 'code'

    def add(self):
        cursor = db.connection.cursor()
        cursor.execute(
            f'INSERT INTO {self._ref} (code, name, college) VALUES (%s, %s, %s);',
            (self.code, self.name, self.college))
        db.connection.commit()

    def edit(self, prev_id):
        cursor = db.connection.cursor()
        cursor.execute(
            f'UPDATE {self._ref} \
            SET \
                code = %s, \
                name = %s, \
                college = %s \
            WHERE code = %s;',
            (self.code, self.name, self.college, prev_id))
        db.connection.commit()

    @classmethod
    def get_one(cls, val):
        cursor = db.connection.cursor()
        cursor.execute(f'SELECT code, name, college \
            FROM {cls._ref} WHERE {cls._primary} = %s LIMIT 1', (val,))
        result = cursor.fetchone()
        if result:
            return cls(*result)
        else:
            return False

    @classmethod
    def get_paginated(cls,
        page=1, per_page=50, sort='code', order='asc',
        code=None, name=None, college=None):
        params = []
        query = f'SELECT * FROM {cls._ref} '
        if code or name or college:
            query += 'WHERE '
            filters = []
            if code:
                filters.append('code LIKE %s ')
                params.append(f'%{code}%')
            if name:
                filters.append('name LIKE %s ')
                params.append(f'%{name}%')
            if college:
                filters.append('college IN (%s) ')
                params.append(f'{",".join(college)}')
            query += 'AND '.join(filters)
        query += f'ORDER BY {sort} {order} LIMIT {(page - 1) * per_page}, {per_page};'
        cursor = db.connection.cursor()
        cursor.execute(query, tuple(params) or None)
        result = cursor.fetchall()
        return starmap(cls, result)

    @classmethod
    def count_query(cls,
        code=None, name=None, college=None):
        params = []
        query = f'SELECT COUNT(*) FROM {cls._ref} '
        if code or name or college:
            query += 'WHERE '
            filters = []
            if code:
                filters.append('code LIKE %s ')
                params.append(f'%{code}%')
            if name:
                filters.append('name LIKE %s ')
                params.append(f'%{name}%')
            if college:
                filters.append('college IN (%s) ')
                params.append(f'{",".join(college)}')
            query += 'AND '.join(filters)
        cursor = db.connection.cursor()
        cursor.execute(query, tuple(params) or None)
        result = cursor.fetchone()
        return result[0]

class College(Base):
    def __init__(self, code=None, name=None):
        self.code = code
        self.name = name

    _ref = 'college'
    _primary = 'code'

    def add(self):
        cursor = db.connection.cursor()
        cursor.execute(
            f'INSERT INTO {self._ref} (code, name) VALUES (%s, %s);',
            (self.code, self.name))
        db.connection.commit()

    def edit(self, prev_id):
        cursor = db.connection.cursor()
        cursor.execute(
            f'UPDATE {self._ref} \
            SET \
                code = %s, \
                name = %s \
            WHERE code = %s;',
            (self.code, self.name, prev_id))
        db.connection.commit()

    @classmethod
    def get_one(cls, val):
        cursor = db.connection.cursor()
        cursor.execute(f'SELECT code, name \
            FROM {cls._ref} WHERE {cls._primary} = %s LIMIT 1', (val,))
        result = cursor.fetchone()
        if result:
            return cls(*result)
        else:
            return False

    @classmethod
    def get_paginated(cls,
        page=1, per_page=50, sort='code', order='asc',
        code=None, name=None):
        params = []
        query = f'SELECT * FROM {cls._ref} '
        if code or name:
            query += 'WHERE '
            filters = []
            if code:
                filters.append('code LIKE %s ')
                params.append(f'%{code}%')
            if name:
                filters.append('name LIKE %s ')
                params.append(f'%{name}%')
            query += 'AND '.join(filters)
        query += f'ORDER BY {sort} {order} LIMIT {(page - 1) * per_page}, {per_page};'
        cursor = db.connection.cursor()
        cursor.execute(query, tuple(params) or None)
        result = cursor.fetchall()
        return starmap(cls, result)

    @classmethod
    def count_query(cls,
        code=None, name=None, college=None):
        params = []
        query = f'SELECT COUNT(*) FROM {cls._ref} '
        if code or name or college:
            query += 'WHERE '
            filters = []
            if code:
                filters.append('code LIKE %s ')
                params.append(f'%{code}%')
            if name:
                filters.append('name LIKE %s ')
                params.append(f'%{name}%')
            query += 'AND '.join(filters)
        cursor = db.connection.cursor()
        cursor.execute(query, tuple(params) or None)
        result = cursor.fetchone()
        return result[0]

# SQLAlchemy

# class Gender(enum.Enum):
#     # https://docs.sqlalchemy.org/en/14/core/type_basics.html#sqlalchemy.types.Enum
#     # Enum names are persisted, not values.
#     Other = 1
#     Male = 2
#     Female = 3

# class Student(db.Model):
#     id = db.Column(db.CHAR(9), primary_key=True)
#     firstname = db.Column(db.String(50), nullable=False)
#     lastname = db.Column(db.String(50), nullable=False)
#     course = db.Column(db.String(10), db.ForeignKey('course.code', onupdate='CASCADE', ondelete='SET NULL'))
#     year = db.Column(db.Integer, nullable=False)
#     # https://stackoverflow.com/questions/44343431/flask-sqlalchemy-enum-field-default-value
#     # Enums in SQLAlchemy carry the enum when queried, bringing some clunk in the process.
#     # Subject to change.
#     gender = db.Column(db.Enum(Gender), nullable=False, server_default='Other')

#     # https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
#     # The __repr__ method tells Python how to print objects of this class
#     def __repr__(self):
#         return '<Student {}>'.format(self.id)

# class Course(db.Model):
#     code = db.Column(db.String(10), primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     college = db.Column(db.String(5), db.ForeignKey('college.code', onupdate='CASCADE', ondelete='SET NULL'))

#     def __repr__(self):
#         return '<Course {}>'.format(self.code)

#     def to_choice(self):
#         return (self.code, '{} ({})'.format(self.name, self.code))

# class College(db.Model):
#     code = db.Column(db.String(5), primary_key=True)
#     name = db.Column(db.String(50), nullable=False)

#     def __repr__(self):
#         return '<College {}>'.format(self.code)

#     def to_choice(self):
#         return (self.code, '{} ({})'.format(self.name, self.code))
