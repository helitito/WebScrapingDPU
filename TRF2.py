import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


# URL do site
url = "https://www.trf2.jus.br/jfes/institucional/jurisdicao"

# Requisição da página
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Dados fixos
trf = "TRF2"
estado = "ES"

# Lista para armazenar os dados
dados = []

# Inicializa subseção atual
subsecao_atual = None

# Percorre todos os elementos da área principal
for tag in soup.find_all(["h4", "p"]):
    texto = tag.get_text(strip=True)

    # Se for um título de subseção (geralmente em <strong>)
    if texto and "Cidades atendidas:" not in texto and len(texto) < 100:
        subsecao_atual = texto

    # Se for um parágrafo com cidades
    elif "Cidades atendidas:" in texto and subsecao_atual:
        cidades_texto = texto.split("Cidades atendidas:")[1]
        cidades = [cidade.strip() for cidade in cidades_texto.split(",")]

        for cidade in cidades:
            dados.append({
                "TRF": trf,
                "Cidade": cidade,
                "Subseção": subsecao_atual,
                "Estado": estado
            })

#Data de hoje
data_hoje = datetime.today().strftime('%Y-%m-%d')  # Formato: 2025-09-08
nome_arquivo = f"jurisdicao_trf2_{data_hoje}.xlsx"

# Cria DataFrame
df = pd.DataFrame(dados)

# Exporta para Excel
df.to_excel(nome_arquivo, index=False)

print("Arquivo Excel gerado com sucesso!")