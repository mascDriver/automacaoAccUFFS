import random
from datetime import timedelta

from PyPDF2 import PdfReader
from dateutil.parser import parse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from rpa.browser import Browser

MONTHS = {
    'janeiro': 1, 'fevereiro': 2, 'março': 3, 'abril': 4, 'maio': 5, 'junho': 6, 'julho': 7, 'agosto': 8, 'setembro': 9,
    'outubro': 10, 'novembro': 11, 'dezembro': 12
}

FORMAT_DATE = {'pt-BR': '%d/%m/%Y', 'en-US': '%m/%d/%Y', 'en': '%m/%d/%Y'}


class PdfManager:
    def __init__(self, file):
        self.file = file
        self.reader = PdfReader(file)

    def get_text(self):
        page = self.reader.pages[0]
        text = page.extract_text().replace('\n', ' ')
        return text


def prepare_file(file):
    file_content = file.read()
    file_name = file.name
    temp_file_path = default_storage.save(file_name, ContentFile(file_content))
    file_path = default_storage.path(temp_file_path)
    return file_path


class BotGoogleForm:
    def __init__(self, data, files, xpaths):
        self.browser = Browser()
        self.data = data
        self.files = files
        self.xpaths = xpaths
        self.hours = 0

    def extract_information_alura_normal(self, text, language):
        data_finalizado, curso = text.split('Finalizado em ')[-1].split(' Curso_ ')
        data_finalizado = data_finalizado.split(' de ')
        data_finalizado = parse(f'{data_finalizado[0]}/{MONTHS[data_finalizado[1]]}/{data_finalizado[2]}')
        curso = curso.split(' Em parceria com')[0]
        horas_curso = text.split('carga horária estimada em ')[-1].split(' horas')[0]
        self.data.update({
            'data_inicio': (data_finalizado - timedelta(random.randint(1, 4))).strftime(FORMAT_DATE[language]),
            'data_fim': data_finalizado.strftime(FORMAT_DATE[language]),
            'horas_curso': horas_curso,
            'atividade': curso,
        })

    def extract_information_alura_formal(self, text, language):
        data_inicio, data_fim = text.split('no período de ')[-1].split('. ')[0].split(' a ')
        curso = text.split('o curso online "')[-1].split('" de carga')[0]
        horas_curso = text.split('de carga horária estimada em ')[-1].split(' hora')[0]
        self.hours += int(horas_curso)
        self.data.update({
            'data_inicio': parse(data_inicio).strftime(FORMAT_DATE[language]),
            'data_fim': parse(data_fim).strftime(FORMAT_DATE[language]),
            'horas_curso': horas_curso,
            'atividade': curso,
        })

    def extract_information(self, text):
        language = self.browser.driver.execute_script("return window.navigator.userLanguage || window.navigator.language")
        if self.data.get('empresa') == '0':
            self.extract_information_alura_normal(text, language)
        elif self.data.get('empresa') == '1':
            self.extract_information_alura_formal(text, language)

    def fill_form(self):
        for key, value in self.data.items():
            if key == 'curso':
                self.browser.driver.find_element(By.ID, value).click()
            elif key == 'arquivo':
                continue
            elif key == 'empresa':
                self.browser.driver.find_element(By.XPATH, self.xpaths[f"xpath_{key}"]).send_keys('Alura')
            else:
                self.browser.driver.find_element(By.XPATH, self.xpaths[f"xpath_{key}"]).send_keys(value)

    def fill_file(self, file_path):
        self.browser.driver.find_element(
            By.XPATH,
            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[15]/div/div/div[2]/div/div[2]'
        ).click()
        self.browser.wait_for_element(By.ID, ':0.contentEl')
        div = self.browser.driver.find_element(By.ID, ':0.contentEl')
        WebDriverWait(div, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
        iframe = div.find_element(By.TAG_NAME, 'iframe')
        self.browser.driver.switch_to.frame(iframe)
        self.browser.wait_for_element(element=self.xpaths['xpath_arquivo'])
        self.browser.driver.find_element(By.XPATH, self.xpaths['xpath_arquivo']).send_keys(file_path)

    def insert_data(self):
        link = self.data.pop('url_form')
        self.browser.driver.get(link)
        self.browser.wait_for_element(By.PARTIAL_LINK_TEXT, "estudante.uffs.edu.br")

        for file in self.files.getlist('arquivo'):
            file_path = prepare_file(file)

            pdf = PdfManager(file_path)
            text = pdf.get_text()

            self.extract_information(text)

            self.fill_form()
            self.fill_file(file_path)

            self.browser.wait_for_element(element=self.xpaths['xpath_email'], timeout=600)

            while True:
                if not self.browser.driver.find_element(By.XPATH, self.xpaths['xpath_email']).get_attribute('value'):
                    break
            default_storage.delete(file_path)
        return f"Foram enviados um total de {self.hours} horas de atividades complementares."
