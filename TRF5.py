from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

# Inicializa o navegador com ChromeDriver automático
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Executa em segundo plano (sem abrir janela)
driver = webdriver.Chrome(service=service, options=options)

# Acessa a página
url = "https://www5.trf5.jus.br/jurisdicao/consulta.php?consulta=&tipoConsulta="
driver.get(url)
time.sleep(5)  # Aguarda o carregamento da página

# Captura o HTML renderizado
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

# Encontra a tabela
table = soup.find("table", {"class": "table"})

# Extrai os dados
data = []
for row in table.find_all("tr")[1:]:  # Ignora o cabeçalho
    cols = row.find_all("td")
    if len(cols) >= 3:
        trf = "TRF5"
        cidade = cols[0].get_text(strip=True)
        subsecao = cols[1].get_text(strip=True)
        uf = cols[2].get_text(strip=True)
        data.append([trf, cidade, subsecao, uf])

# Fecha o navegador
driver.quit()

# Cria o DataFrame
df = pd.DataFrame(data, columns=["TRF", "Cidades", "Subseção", "UF"])

# Salva com a data de hoje
hoje = datetime.today().strftime('%d-%m-%Y')
nome_arquivo = f"TRF5_Subsecoes_{hoje}.xlsx"
df.to_excel(nome_arquivo, index=False)

print(f"✅ Planilha salva como: {nome_arquivo}")