from mainapp.models import UserFactory, Category, CourseFactory


class Engine:
    def __init__(self):
        self.state = {
            'tutors': [],
            'students': [],
            'categories': [],
            'courses': [],
        }

    def create_user(self, user_type):
        user = UserFactory.create(user_type)
        self.state[user_type].append(user)
        return user

    def create_category(self, name, category=None):
        category = Category(name, category)
        self.state['categories'].append(category)
        return category

    def find_category_by_id(self, id):
        for category in self.state['categories']:
            if category.id == id:
                return category
        raise Exception(f'Category {id} not found')

    def create_course(self, course_type, name, category, **kwargs):
        course = CourseFactory.create(course_type, name, category, **kwargs)
        self.state['courses'].append(course)
        return course

    def get_course_by_name(self, name):
        for course in self.state['courses']:
            if course.name == name:
                return course
        return None
