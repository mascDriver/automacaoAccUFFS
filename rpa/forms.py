from django import forms

from rpa.browser import Browser


class AccForm(forms.Form):
    email = forms.CharField(label='Email', max_length=100)
    nome = forms.CharField(label='Nome Completo', max_length=100)
    cpf = forms.CharField(label='CPF', max_length=11, help_text='Informe seu CPF com 11 dígitos sem pontos e traço. Ex.: 12345678900')
    matricula = forms.CharField(label='Matricula', max_length=100, help_text='Informe seu número de matrícula com 10 dígitos sem pontos e traço. Ex.: 1234567890')
    curso = forms.ChoiceField(label='Curso', choices=[('i29', 'Ciência da Computação')])
    empresa = forms.ChoiceField(label='Instituição promotora da atividade', choices=[(0, 'Alura - Certificado Normal'), (1, 'Alura - Certificado Formal')])
    arquivo = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}))

    def __init__(self, *args, **kwargs):
        super(AccForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def initialize_rpa(self):
        browser = Browser()
        browser.insert_data(self.cleaned_data, self.files)
