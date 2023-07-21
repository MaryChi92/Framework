from framework_config.templator import render


class TemplateView:
    template_name = "index.html"

    def __call__(self, request):
        if request["method"] == "GET":
            return "200 OK", render(self.template_name, context=request)
        elif request["method"] == "POST":
            message = request["params"]
            print(message)
            return "200 OK", render(self.template_name, context=request)


class IndexView(TemplateView):
    pass


class PageView(TemplateView):
    template_name = "page.html"


class AnotherPageView(TemplateView):
    template_name = "another_page.html"


class ExamplesView(TemplateView):
    template_name = "examples.html"


class ContactsView(TemplateView):
    template_name = "contacts.html"
