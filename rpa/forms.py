from django import forms
from rpa.bot import BotGoogleForm


XPATHS = {
    'email': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/div[1]/input',
    'nome': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input',
    'cpf': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input',
    'matricula': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[1]/div/div[1]/input',
    'data_inicio': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[11]/div/div/div[2]/div/div/div[2]/div[1]/div/div[1]/input',
    'data_fim': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[12]/div/div/div[2]/div/div/div[2]/div[1]/div/div[1]/input',
    'horas_curso': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[13]/div/div/div[2]/div/div[1]/div/div[1]/input',
    'arquivo': '//input[@type="file"]',
    'atividade': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[8]/div/div/div[2]/div/div[1]/div/div[1]/input',
    'empresa': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[9]/div/div/div[2]/div/div[1]/div/div[1]/input'
}


class AccForm(forms.Form):
    email = forms.CharField(label='Email', max_length=100)
    nome = forms.CharField(label='Nome Completo', max_length=100)
    cpf = forms.CharField(label='CPF', max_length=11, help_text='Informe seu CPF com 11 dígitos sem pontos e traço. Ex.: 12345678900')
    matricula = forms.CharField(label='Matricula', max_length=10, help_text='Informe seu número de matrícula com 10 dígitos sem pontos e traço. Ex.: 1234567890')
    curso = forms.ChoiceField(label='Curso', choices=[('i29', 'Ciência da Computação')])
    empresa = forms.ChoiceField(label='Instituição promotora da atividade', choices=[(0, 'Alura - Certificado Normal'), (1, 'Alura - Certificado Formal')])
    arquivo = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}))
    url_form = forms.URLField(label='URL do Formulário', max_length=200, initial='https://docs.google.com/forms/d/e/1FAIpQLScKx2in_Nnh9b-Gs3jl5CN-H83HHBlVGPQyaQNmWTQMay4CfA/viewform')

    def __init__(self, *args, **kwargs):
        super(AccForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        if '@estudante.uffs.edu.br' not in email:
            email = email + '@estudante.uffs.edu.br'
        return email

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        if len(cpf) != 11:
            raise forms.ValidationError('CPF deve conter 11 dígitos.')
        if not cpf.isnumeric():
            raise forms.ValidationError('O CPF deve conter apenas números.')
        return cpf

    def clean_matricula(self):
        matricula = self.cleaned_data['matricula']
        if len(matricula) != 10:
            raise forms.ValidationError('Matrícula deve conter 10 dígitos.')
        if not matricula.isnumeric():
            raise forms.ValidationError('A matrícula deve conter apenas números.')
        return matricula

    def initialize_rpa(self, xpaths):
        bot = BotGoogleForm(self.cleaned_data, self.files, xpaths)
        msg = bot.insert_data()
        return True, msg


class XpathForm(forms.Form):
    xpath_email = forms.CharField(label='Xpath E-mail', max_length=200, initial=XPATHS['email'])
    xpath_nome = forms.CharField(label='Xpath Nome Completo', max_length=200, initial=XPATHS['nome'])
    xpath_cpf = forms.CharField(label='Xpath CPF', max_length=200, initial=XPATHS['cpf'])
    xpath_matricula = forms.CharField(label='Xpath Matrícula', max_length=200, initial=XPATHS['matricula'])
    xpath_atividade = forms.CharField(label='Xpath Atividade', max_length=200, initial=XPATHS['atividade'])
    xpath_empresa = forms.CharField(label='Xpath Instituição promotora da atividade', max_length=200, initial=XPATHS['empresa'])
    xpath_data_inicio = forms.CharField(label='Xpath Data de início', max_length=200, initial=XPATHS['data_inicio'])
    xpath_data_fim = forms.CharField(label='Xpath Data final', max_length=200, initial=XPATHS['data_fim'])
    xpath_horas_curso = forms.CharField(label='Xpath Carga horária da atividade', max_length=200, initial=XPATHS['horas_curso'])
    xpath_arquivo = forms.CharField(label='Xpath Comprovante', max_length=200, initial=XPATHS['arquivo'])

    def __init__(self, *args, **kwargs):
        super(XpathForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
