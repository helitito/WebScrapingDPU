import requests
from bs4 import BeautifulSoup
import pandas as pd

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

# Busca por todos os elementos <p>
paragrafos = soup.find_all("p")

# Variável para armazenar a subseção atual
subsecao_atual = None

for p in paragrafos:
    texto = p.get_text(strip=True)

    # Se o parágrafo não contém "Cidades atendidas", é provavelmente o nome da subseção
    if "Cidades atendidas:" not in texto and len(texto) > 0:
        subsecao_atual = texto

    # Se contém as cidades, extraí-las e associar à subseção atual
    elif "Cidades atendidas:" in texto and subsecao_atual:
        cidades_texto = texto.split("Cidades atendidas:")[1]
        cidades = [cidade.strip() for cidade in cidades_texto.split(",")]

        for cidade in cidades:
            dados.append({
                "TRF": trf,
                "Cidade": cidade,
                "Jurisdição": subsecao_atual,
                "Estado": estado
            })

# Cria DataFrame
df = pd.DataFrame(dados)

# Exporta para Excel
df.to_excel("jurisdicao_trf2.xlsx", index=False)

print("Arquivo Excel gerado com sucesso!")