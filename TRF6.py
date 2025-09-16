import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# URL da página com as subseções (exemplo fictício)
url = "https://www.trf6.jus.br/institucional/subsecoes"

# Faz a requisição
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Lista para armazenar os dados
dados = []

# Exemplo de estrutura HTML (ajuste conforme o site real)
tabela = soup.find("table")  # ou soup.find_all("div", class_="subsecao") se for em blocos

for linha in tabela.find_all("tr")[1:]:  # Ignora o cabeçalho
    colunas = linha.find_all("td")
    if len(colunas) >= 4:
        trf = "TRF6"
        subsecao = colunas[0].get_text(strip=True)
        cidade = colunas[1].get_text(strip=True)
        uf = colunas[2].get_text(strip=True)
        dados.append({
            "TRF": trf,
            "Subseção": subsecao,
            "Cidade": cidade,
            "UF": uf
        })

# Cria DataFrame
df = pd.DataFrame(dados)

# Salva em Excel com data de hoje
data_hoje = datetime.today().strftime("%Y-%m-%d")
nome_arquivo = f"subsecoes_TRF6_{data_hoje}.xlsx"
df.to_excel(nome_arquivo, index=False)

print(f"Planilha '{nome_arquivo}' criada com sucesso!")