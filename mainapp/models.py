from copy import deepcopy

from framework_config.middleware import Subject
from database.main import Objects
from database.exceptions import IntegrityError
from framework_config.middleware import BaseRegisteredClass


class UserMapper(BaseRegisteredClass):
    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.tablename = 'users'

    def select_all(self):
        sql_statement = f'SELECT * FROM {self.tablename};'
        self.cursor.execute(sql_statement)
        result = []
        for row in self.cursor.fetchall():
            id, usertype, username, email, password = row
            user = UserFactory.create(usertype, username, email, password, id)
            result.append(user)
        return result

    def find_by_id(self, id):
        sql_statement = f'SELECT id, usertype, username, email, password FROM {self.tablename} WHERE id=?'
        self.cursor.execute(sql_statement, (id,))
        result = self.cursor.fetchone()
        if result:
            id, usertype, username, email, password = result
            return UserFactory.create(usertype, username, email, password, id)
        else:
            raise IntegrityError(f'record with id={id} not found')

    def insert(self, user):
        sql_statement = f'INSERT INTO {self.tablename} (id, usertype, username, email, password) VALUES (?, ?, ?, ?, ?)'
        self.cursor.execute(sql_statement, (user.id, 'student', user.username, user.email, user.password))
        try:
            self.connection.commit()
        except Exception as e:
            raise IntegrityError(e.args)

    def update(self, user):
        sql_statement = f'UPDATE {self.tablename} SET username=? WHERE id=?'
        self.cursor.execute(sql_statement, (user.username, user.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise IntegrityError(e.args)

    def delete(self, user):
        sql_statement = f'DELETE FROM {self.tablename} WHERE id=?'
        self.cursor.execute(sql_statement, (user.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise IntegrityError(e.args)


class User(Objects):
    mapper = 'UserMapper'
    auto_id = 0

    def __init__(self, username, email, password, id=None):
        if not id:
            self.id = User.auto_id
            User.auto_id += 1
        else:
            self.id = id
        self.username = username
        self.email = email
        self.password = password


class Tutor(User):
    pass


class Student(User):
    def __init__(self, username, email, password, id=None):
        super().__init__(username, email, password, id)
        self.courses = []


class UserFactory(Objects):
    user_types = {
        'tutor': Tutor,
        'student': Student,
    }

    @classmethod
    def create_obj(cls, user_type, username, email, password):
        return cls.user_types[user_type](username, email, password)


class Course(Subject):
    def __init__(self, name, category):
        super().__init__()
        self.name = name
        self.students = []
        self.category = category
        self.category.courses.append(self)

    def __iter__(self):
        for student in self.students:
            yield student

    def clone(self):
        course = deepcopy(self)
        course.name = f'{self.name}_copy'
        self.category.courses.append(course)
        return course

    def add_student(self, student):
        self.students.append(student)
        self.notify()


class InteractiveCourse(Course):
    def __init__(self, name, category, place=None, **kwargs):
        super().__init__(name, category)
        self.place = place


class RecordedCourse(Course):
    def __init__(self, name, category, place=None, **kwargs):
        super().__init__(name, category)
        self.place = place


class OfflineCourse(Course):
    def __init__(self, name, category, place=None, **kwargs):
        super().__init__(name, category)
        self.place = place


class CourseFactory:
    course_types = {
        'interactive': InteractiveCourse,
        'recorded': RecordedCourse,
        'offline': OfflineCourse,
    }

    @classmethod
    def create(cls, course_type, name, category, **kwargs):
        return cls.course_types[course_type](name, category, **kwargs)


class Category:
    auto_id = 0

    def __init__(self, name):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.categories = {}
        self.courses = []

    def __iter__(self):
        for course in self.courses:
            yield course

    def __repr__(self):
        return f'Category {self.name}'

    def course_count(self):
        result = len(self.courses)
        if self.categories:
            for category in self.categories.values():
                result += category.course_count()
        return result

