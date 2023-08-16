from http import HTTPStatus

from framework_config.templator import render
from framework_config.utils import AppRoute, debug
from framework_config.views import TemplateView, ListView, CreateView, engine, logger
from framework_config.middleware import SmsNotifier, EmailNotifier, MapperRegistry
from database.main import Session
from mainapp.models import Student, User

sms_notifier = SmsNotifier()
email_notifier = EmailNotifier()
Session.new_current()
Session.get_current().register_mappers(MapperRegistry)


@AppRoute('/')
class IndexView(TemplateView):
    pass


@AppRoute('/about/')
class AboutView(TemplateView):
    template_name = "about.html"


@AppRoute('/courses/create_course/')
class CreateCourseView(CreateView):
    template_name = "create_course.html"

    @debug
    def create_object(self, data):
        category = engine.find_category_by_id(int(data['category_id']), engine.state['categories'])
        try:
            course = engine.create_course(category=category, **data)
        except Exception:
            return f"{HTTPStatus.BAD_REQUEST} BAD REQUEST", render("courses_list.html")
        else:
            course.observers.extend((email_notifier, sms_notifier))


@AppRoute('/courses/copy_course/')
class CopyCourseView(ListView):
    template_name = "courses_list.html"

    def __call__(self, request):
        data = request['params']
        name = data['name']
        course = engine.get_course_by_name(name)
        course.clone()
        return super().__call__(request)


@AppRoute('/courses/')
class CoursesListView(ListView):
    template_name = "courses_list.html"


@AppRoute('/categories/create_category/')
class CreateCategoryView(CreateView):
    template_name = "create_category.html"

    def create_object(self, data):
        name = data['name']
        category_id = data['category_id']
        if category_id:
            category_id = int(category_id)
            category = engine.find_category_by_id(category_id)
        else:
            category = None
        if name:
            engine.create_category(name, category)


@AppRoute('/categories/')
class CategoriesListView(ListView):
    template_name = "categories_list.html"


@AppRoute('/examples/')
class ExamplesView(TemplateView):
    template_name = "examples.html"


@AppRoute('/contacts/')
class ContactsView(TemplateView):
    template_name = "contacts.html"

    def __call__(self, request):
        if request['method'] == 'POST':
            message = request['params']
            logger.log(message)
        return super().__call__(request)


@AppRoute('/students/')
class StudentsListView(ListView):
    template_name = "students_list.html"

    def get_context(self, request):
        students = Session.get_current().get_mapper(Student).all()
        for student in students:
            engine.state['students'][student.id] = student
        request['state'] = engine.state


@AppRoute('/auth/register/')
class RegisterView(CreateView):
    template_name = "register.html"

    @debug
    def create_object(self, data):
        username = data.get('username')
        if username:
            student = engine.create_user(data.get('user_type'), username, data.get('email'), data.get('password'))
            student.create()
            Session.get_current().commit()


@AppRoute('/signup/')
class SignupView(CreateView):
    template_name = 'sign_up_for_course.html'

    def get_context(self, request):
        super().get_context(request)
        students = Session.get_current().get_mapper(Student).all()
        for student in students:
            engine.state['students'][student.id] = student

    def create_object(self, data):
        course_name = data.get('course')
        student_id = data.get('student_id')
        if course_name and student_id:
            course = engine.get_course_by_name(course_name)
            student = engine.state['students'][int(student_id)]
            if student not in course.students:
                course.add_student(student)

    def __call__(self, request):
        if request['method'] == 'POST':
            data = self.get_request_data(request)
            self.create_object(data)
            return f'{HTTPStatus.CREATED} CREATED', render('index.html', context=request)
        request['courses'] = engine.get_courses(engine.state['categories'])
        return super().__call__(request)
