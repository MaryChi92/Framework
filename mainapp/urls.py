from datetime import date
from mainapp.views import IndexView, AboutView, CreateCourseView, CopyCourseView, CoursesListView, CreateCategoryView,\
    CategoriesListView, ExamplesView, ContactsView


def date_today(context):
    context["date"] = date.today()


def hello_friend(context):
    context["hello_friend"] = "Hello Friend!"


fronts = [date_today, hello_friend]

urls = {}
