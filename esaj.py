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

        self.dict = {
            "data_process": {},
            "parts_process": {},
            "movements": {},
            "incidents": {},
            "various_petitions": {},
            "audiences": {}
        }


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

    
    def process_tables_html(self):

        self.table_data_process = self.driver.find_element(By.XPATH, "/html/body/table[4]/tbody/tr/td/table[2]").get_attribute("innerHTML")
        self.table_parts_process = self.driver.find_element(By.ID, "tablePartesPrincipais").get_attribute("innerHTML")
        self.table_movements = self.driver.find_element(By.ID, "tabelaTodasMovimentacoes").get_attribute("innerHTML")
        self.table_incidents = self.driver.find_element(By.XPATH, "/html/body/table[4]/tbody/tr/td/table[8]").get_attribute("innerHTML")
        self.table_various_petitions = self.driver.find_element(By.XPATH, "/html/body/table[4]/tbody/tr/td/table[11]").get_attribute("innerHTML")
        self.table_audiences = self.driver.find_element(By.XPATH, "/html/body/table[4]/tbody/tr/td/table[12]").get_attribute("innerHTML")

        self.get_data_process()
        self.get_parts_process()
        self.get_movements()
        self.get_incidents()
        self.get_various_petitions()
        self.get_audiences()

    
    def clean_data(self, text):
        text = text.replace("\n", "")
        text = text.replace("\t", "")
        text = text.replace("<br>", "").strip()
        return " ".join(text.split())


    def get_data_process(self):
        dict_data_process = {}

        exp_process = '<tr>.*?<div .*?>Processo:</div>.*?</td>.*?<td .*?>.*?<table .*?>.*?<td>(.*?)</td>.*?</table>.*?</td>.*?</tr>'
        result_process = re.findall(exp_process, self.table_data_process, re.DOTALL)
        exp_process_span = '<span class="">(.*?)</span>.*?<span class="">(.*?)</span>.*?<span .*?>(.*?)</span>'
        result_process_span = re.findall(exp_process_span, result_process[0], re.DOTALL)
        dict_data_process["process"] = self.clean_data(result_process_span[0][0]) + " " + self.clean_data(result_process_span[0][1]) + " " + self.clean_data(result_process_span[0][2])
        
        exp_class = '<tr>.*?<div .*?>Classe:</div>.*?</td>.*?<td .*?>.*?<table .*?>.*?<td>(.*?)</td>.*?</table>.*?</td>.*?</tr>'
        result_class = re.findall(exp_class, self.table_data_process, re.DOTALL)
        exp_class_span = '<span id="">.*?<span id="">(.*?)</span>'
        result_class_span = re.findall(exp_class_span, result_class[0], re.DOTALL)
        dict_data_process["class"] = result_class_span[0]
        
        exp_area = '<tr>.*?<td .*?>.*?</td>.*?</td>.*?<td .*?>.*?<table .*?>.*?<td>.*?<span class="labelClass">Área:</span>(.*?)</td>.*?</table>.*?</td>.*?</tr>'
        result_area = re.findall(exp_area, self.table_data_process, re.DOTALL)
        dict_data_process["area"] = self.clean_data(result_area[0])

        exp_subject = '<tr>.*?<div .*?>Assunto:</div>.*?</td>.*?<td .*?>.*?<span id="">(.*?)</span>.*?</td>.*?</tr>'
        result_subject = re.findall(exp_subject, self.table_data_process, re.DOTALL)
        dict_data_process["subject"] = result_subject[0]

        exp_location = '<tr>.*?<div .*?>Local Físico:</div>.*?</td>.*?<td .*?>.*?<span id="">(.*?)</span>.*?</td>.*?</tr>'
        result_location = re.findall(exp_location, self.table_data_process, re.DOTALL)
        dict_data_process["location"] = result_location[0]

        exp_distribution = '<tr>.*?<div .*?>Distribuição:</div>.*?</td>.*?<td .*?>.*?<span id="">(.*?)</span>.*?</td>.*?</tr>'
        result_distribution = re.findall(exp_distribution, self.table_data_process, re.DOTALL)
        dict_data_process["distribution"] = result_distribution[0]

        exp_action = '<tr>.*?<div .*?>Valor da ação:</div>.*?</td>.*?<td .*?>.*?<span id="">(.*?)</span>.*?</td>.*?</tr>'
        result_action = re.findall(exp_action, self.table_data_process, re.DOTALL)
        dict_data_process["action"] = result_action[0]

        self.dict["data_process"]["description"] = dict_data_process
        

    def get_parts_process(self):
        print(self.dict)


    def get_movements(self):
        print(self.dict)


    def get_incidents(self):
        exp = '<td .*?>(.*)</td>'
        result = re.findall(exp, self.table_incidents, re.DOTALL)

        self.dict["incidents"]["description"] = self.clean_data(result[0])


    def get_various_petitions(self):
        exp = '<tbody>(.*?)</tbody>'
        result = re.findall(exp, self.table_various_petitions, re.DOTALL)
        result = result[0].split("</tr>")

        exp_date_type = '<td width="140" .*?>(.*?)</td>.*?<td .*?>(.*?)</td>'
        list_petitions = []

        for petition in result:
            result_date_type = re.findall(exp_date_type, petition, re.DOTALL)
            if result_date_type:
                elements = {
                    "date": self.clean_data(result_date_type[0][0]),
                    "type": self.clean_data(result_date_type[0][1])
                }
                list_petitions.append(elements)

        
        self.dict["various_petitions"]["description"] = list_petitions


    def get_audiences(self):
        exp = '<td .*?>(.*)</td>'
        result = re.findall(exp, self.table_audiences, re.DOTALL)

        self.dict["audiences"]["description"] = self.clean_data(result[0])
    


webdriver = webdriver.Chrome(executable_path="webdriver/chromedriver")
esaj = Esaj(webdriver)
esaj.access()
esaj.search_process("0033765492008", "0001")
esaj.process_tables_html()
webdriver.quit()