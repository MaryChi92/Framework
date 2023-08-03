from datetime import date
from mainapp.views import IndexView, AboutView, CreateCourseView, CopyCourseView, CoursesListView, CreateCategoryView,\
    CategoriesListView, ExamplesView, ContactsView


def date_today(context):
    context["date"] = date.today()


def hello_friend(context):
    context["hello_friend"] = "Hello Friend!"


fronts = [date_today, hello_friend]

urls = {
    # '/': IndexView(),
    # '/about/': AboutView(),
    # '/courses/': CoursesListView(),
    # '/courses/create_course/': CreateCourseView(),
    # '/courses/copy_course/': CopyCourseView(),
    # '/categories/': CategoriesListView(),
    # '/categories/create_category/': CreateCategoryView(),
    # '/examples/': ExamplesView(),
    # '/contacts/': ContactsView(),
}
