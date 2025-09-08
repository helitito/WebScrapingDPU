from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from datetime import datetime

# 🚀 Inicializa o Chrome automaticamente
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 🌐 URLs das subseções por estado
urls = {
    'RS': 'https://www.jfrs.jus.br/institucional/subsecoes/',
    'SC': 'https://www.jfsc.jus.br/institucional/subsecoes/',
    'PR': 'https://www.jfpr.jus.br/institucional/subsecoes/'
}

# 📋 Lista para armazenar os dados
dados = []

# 🔁 Loop pelos estados e extração dos dados
for uf, url in urls.items():
    driver.get(url)
    time.sleep(3)

    blocos = driver.find_elements(By.CSS_SELECTOR, '.subsecao')

    for bloco in blocos:
        try:
            cidade = bloco.find_element(By.CLASS_NAME, 'cidade').text
            nome = bloco.find_element(By.CLASS_NAME, 'nome').text
            dados.append(['TRF4', cidade, nome, uf])
        except Exception as e:
            print(f"⚠️ Erro ao extrair bloco: {e}")
            continue

driver.quit()

# 🗓️ Data atual
data_hoje = datetime.today().strftime('%d-%m-%Y')
nome_arquivo = f'subsecoes_trf4_{data_hoje}.xlsx'

# 🧾 Salva no Excel
df = pd.DataFrame(dados, columns=['TRF', 'Cidade', 'Subseção', 'UF'])
df.to_excel(nome_arquivo, index=False)

print(f"✅ Planilha gerada com sucesso: {nome_arquivo}")