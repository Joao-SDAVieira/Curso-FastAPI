import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import urllib

contatos_df = pd.read_excel("Contatos.xlsx")
print(contatos_df)
"""aqui eu utilizo uma planilha, mas é possível utilizar um dicionário e convertelo para dataframe,ou passar a variável diretamente"""
navegador = webdriver.Firefox()
print("Abrindo Navegador!")
navegador.get("https://web.whatsapp.com/")

print("Navegador aberto")

while len(navegador.find_elements(By.ID,'side')) < 1:
    time.sleep(1)
    
for i in range (10):
    for i, mensagem in enumerate(contatos_df['Mensagem']):
        pessoa = contatos_df.loc[i, "Pessoa"]
        numero = contatos_df.loc[i, "Número"]
        
        texto = urllib.parse.quote(f"Oi {pessoa}! {mensagem}")
        link = f"https://web.whatsapp.com/send?phone={numero}&text={texto}"
        navegador.get(link)
        while len(navegador.find_elements(By.ID, 'side')) < 1:
            time.sleep(1)
        # navegador.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span/div/div[2]/div[1]/div/div/p/span').send_keys(Keys.ENTER)
        navegador.find_element('xpath', '/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span/div/div[2]/div[1]/div/div/p/span').click()
        time.sleep(1)
