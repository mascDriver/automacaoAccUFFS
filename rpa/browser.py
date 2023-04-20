from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class Browser:
    def __init__(self):
        try:
            self.driver = webdriver.Chrome()
        except:
            self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def __del__(self):
        self.driver.quit()

    def wait_for_element(self, by=By.XPATH, element='', timeout=120):
        WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, element)))

