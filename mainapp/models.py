from copy import deepcopy

from framework_config.middleware import Subject


class User:
    auto_id = 0

    def __init__(self, username, email, password):
        self.id = User.auto_id
        User.auto_id += 1
        self.username = username
        self.email = email
        self.password = password


class Tutor(User):
    pass


class Student(User):
    def __init__(self, username, email, password):
        super().__init__(username, email, password)
        self.courses = []


class UserFactory:
    user_types = {
        'tutor': Tutor,
        'student': Student,
    }

    @classmethod
    def create(cls, user_type, username, email, password):
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

