from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import FormView

from rpa.forms import AccForm


class AccFormView(SuccessMessageMixin, FormView):
    template_name = 'rpa/acc.html'
    form_class = AccForm
    success_url = '/'
    success_message = 'Certificados processados com sucesso.'

    def form_valid(self, form):
        status, message = form.initialize_rpa()
        if status:
            return super().form_valid(form)
        else:
            messages.error(self.request, message)
            return super().form_invalid(form)
