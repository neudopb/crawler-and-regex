from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import os
import json
import time
from pathlib import Path

class Esaj:

    def __init__(self, driver):
        self.driver = driver
        self.url = "http://esaj.tjrn.jus.br/cpo/pg/open.do"
        self.id_input_number_process = "numeroDigitoAnoUnificado"
        self.id_input_number_foro = "foroNumeroUnificado"
        self.id_button_search = "botaoPesaquisar"
        self.id_link_parts = "linkpartes"
        self.id_link_moviments = "linkmovimentacoes"


    def access(self):
        self.driver.get(self.url)

    def search_process(self, number_process, number_foro):
        input_number_process = self.driver.find_element(By.ID, self.id_input_number_process)
        input_number_process.send_keys(number_process)

        input_number_foro = self.driver.find_element(By.ID, self.id_input_number_foro)
        input_number_foro.send_keys(number_foro)
        time.sleep(1)
        
        self.driver.find_element(By.ID, self.id_button_search).click()

        self.driver.find_element(By.ID, self.id_link_parts).click()
        self.driver.find_element(By.ID, self.id_link_moviments).click()



webdriver = webdriver.Chrome(executable_path="webdriver/chromedriver")
esaj = Esaj(webdriver)
esaj.access()
esaj.search_process("0033765492008", "0001")
# webdriver.quit()