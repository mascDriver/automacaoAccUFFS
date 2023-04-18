import random
from datetime import timedelta

from PyPDF2 import PdfReader
from dateutil.parser import parse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

month_dict = {
    'janeiro': 1,
    'fevereiro': 2,
    'março': 3,
    'abril': 4,
    'maio': 5,
    'junho': 6,
    'julho': 7,
    'agosto': 8,
    'setembro': 9,
    'outubro': 10,
    'novembro': 11,
    'dezembro': 12
}

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


class Browser:
    def __init__(self):
        try:
            self.driver = webdriver.Chrome()
        except:
            self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def insert_data(self, data, files):
        self.driver.get(
            'https://docs.google.com/forms/d/e/1FAIpQLScKx2in_Nnh9b-Gs3jl5CN-H83HHBlVGPQyaQNmWTQMay4CfA/viewform')
        while True:
            if WebDriverWait(self.driver, 120).until(
                    EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "estudante.uffs.edu.br"))):
                break
        for file in files.getlist('arquivo'):
            file_content = file.read()
            file_name = file.name
            temp_file_path = default_storage.save(file_name, ContentFile(file_content))
            file_path = default_storage.path(temp_file_path)
            reader = PdfReader(file)
            page = reader.pages[0]
            text = page.extract_text().replace('\n', ' ')
            data_finalizado, curso = text.split('Finalizado em ')[-1].split(' Curso_ ')
            data_finalizado = data_finalizado.split(' de ')
            data_finalizado = parse(f'{data_finalizado[0]}/{month_dict[data_finalizado[1]]}/{data_finalizado[2]}')
            curso = curso.split(' Em parceria com')[0]
            horas_curso = text.split('carga horária estimada em ')[-1].split(' horas')[0]
            data.update({
                'data_inicio': (data_finalizado - timedelta(random.randint(1, 4))).strftime('%d/%m/%Y'),
                'data_fim': data_finalizado.strftime('%d/%m/%Y'),
                'horas_curso': horas_curso,
                'atividade': curso,
            })
            for key, value in data.items():
                if key == 'curso':
                    self.driver.find_element(By.ID, value).click()
                elif key == 'arquivo':
                    continue
                elif key == 'empresa':
                    self.driver.find_element(By.XPATH, XPATHS[key]).send_keys('Alura')
                else:
                    self.driver.find_element(By.XPATH, XPATHS[key]).send_keys(value)
            self.driver.find_element(
                By.XPATH,
                '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[15]/div/div/div[2]/div/div[2]'
            ).click()
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, ':0.contentEl')))
            div = self.driver.find_element(By.ID, ':0.contentEl')
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
            iframe = div.find_element(By.TAG_NAME, 'iframe')
            self.driver.switch_to.frame(iframe)
            self.driver.find_element(By.XPATH, XPATHS['arquivo']).send_keys(file_path)
            while True:
                if WebDriverWait(self.driver, 120).until(
                        EC.presence_of_element_located((By.XPATH, XPATHS['email']))):
                    if not self.driver.find_element(By.XPATH, XPATHS['email']).get_attribute('value'):
                        break
            default_storage.delete(temp_file_path)
        self.driver.quit()
