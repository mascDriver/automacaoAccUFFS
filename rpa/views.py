from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import FormView

from rpa.forms import AccForm, XpathForm


class AccFormView(SuccessMessageMixin, FormView):
    template_name = 'rpa/acc.html'
    form_class = AccForm
    form_class_aux = XpathForm
    success_url = '/'
    success_message = 'Certificados processados com sucesso.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form2'] = self.form_class_aux()
        return context

    def form_valid(self, form):
        form2 = self.form_class_aux(self.request.POST)
        if form2.is_valid():
            status, message = form.initialize_rpa(form2.cleaned_data)
            if status:
                return super().form_valid(form)
            else:
                messages.error(self.request, message)
                return super().form_invalid(form)
