from copy import deepcopy


class User:
    def __init__(self, username):
        self.username = username


class Tutor(User):
    pass


class Student(User):
    pass


class UserFactory:
    user_types = {
        'tutor': Tutor,
        'student': Student,
    }

    @classmethod
    def create(cls, user_type):
        return cls.user_types[user_type]


class Course:
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)

    def clone(self):
        course = deepcopy(self)
        course.name = f'{self.name}_copy'
        self.category.courses.append(course)
        return course


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

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result

