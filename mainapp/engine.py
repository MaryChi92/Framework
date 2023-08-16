from mainapp.models import UserFactory, Category, CourseFactory


class Engine:
    def __init__(self):
        self.state = {
            'tutors': {},
            'students': {},
            'categories': {},
            'courses': [],
        }

    def create_user(self, user_type, username, email, password):
        user = UserFactory.create_obj(user_type, username, email, password)
        self.state[f'{user_type}s'][user.id] = user
        return user

    def create_category(self, name, category=None):
        new_category = Category(name)
        if category:
            category.categories[new_category.id] = new_category
        else:
            self.state['categories'][new_category.id] = new_category
        return category

    def find_category_by_id(self, category_id, categories):
        for key, category in categories.items():
            required_category = None
            if category.id == category_id:
                return category
            if category.categories:
                try:
                    required_category = self.find_category_by_id(category_id, category.categories)
                except Exception:
                    pass
            if required_category:
                return required_category
        else:
            raise Exception(f'Category {category_id} not found')

    def create_course(self, course_type, name, category, **kwargs):
        course = CourseFactory.create(course_type, name, category, **kwargs)
        self.state['courses'].append(course)
        return course

    def get_course_by_name(self, name):
        for course in self.state['courses']:
            if course.name == name:
                return course
        return None

    def get_courses(self, categories):
        courses_list = []
        for category in categories.values():
            courses_list.extend(category.courses)
            if category.categories:
                courses_list.extend(self.get_courses(category.categories))
        return courses_list
