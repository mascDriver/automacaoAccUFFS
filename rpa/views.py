from django.views.generic.edit import FormView

from rpa.forms import AccForm


class AccFormView(FormView):
    template_name = 'rpa/acc.html'
    form_class = AccForm
    success_url = '/'

    def form_valid(self, form):
        form.initialize_rpa()
        return super().form_valid(form)
