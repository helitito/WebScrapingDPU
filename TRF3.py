from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
from datetime import datetime
import requests

# 🚀 Configuração do navegador
options = Options()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 20)

# 📦 Lista para armazenar os dados
dados = []

# 📍 Mapeamento de códigos IBGE para siglas de UF
uf_siglas = {
    11: "RO", 12: "AC", 13: "AM", 14: "RR", 15: "PA", 16: "AP", 17: "TO",
    21: "MA", 22: "PI", 23: "CE", 24: "RN", 25: "PB", 26: "PE", 27: "AL", 28: "SE", 29: "BA",
    31: "MG", 32: "ES", 33: "RJ", 35: "SP",
    41: "PR", 42: "SC", 43: "RS",
    50: "MS", 51: "MT", 52: "GO", 53: "DF"
}

# 🏙️ Função para obter cidades por UF
def obter_cidades_por_uf(uf_codigo):
    url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf_codigo}/municipios"
    resposta = requests.get(url)
    if resposta.status_code == 200:
        municipios = resposta.json()
        return set(m['nome'] for m in municipios)
    else:
        print(f"❌ Erro ao buscar cidades do UF {uf_codigo}")
        return set()

# 🔍 Carrega todas as cidades por UF
ufs_cidades = {uf: obter_cidades_por_uf(uf) for uf in uf_siglas.keys()}

# 🧠 Função para identificar a sigla da UF de uma cidade
def identificar_uf(cidade):
    for uf_codigo, cidades in ufs_cidades.items():
        if cidade in cidades:
            return uf_siglas.get(uf_codigo, "Desconhecido")
    return "Desconhecido"

# ⚖️ TRF3
def extrair_trf3():
    driver.get("https://www.trf3.jus.br/scaj/foruns-e-juizados/jurisdicoes-das-varas-e-jefs/jurisdicoes-por-municipios/")
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//table//tr")))
        linhas = driver.find_elements(By.XPATH, "//table//tr")[1:]

        for linha in linhas:
            colunas = linha.find_elements(By.TAG_NAME, "td")
            if len(colunas) >= 2:
                cidade = colunas[0].text.strip()
                subsecao = colunas[1].text.strip()
                uf = identificar_uf(cidade)

                dados.append({
                    "TRF": "TRF3",
                    "Subseção Judiciária": subsecao,
                    "Cidade": cidade,
                    "UF": uf
                })
        print(f"✅ TRF3: {len(dados)} registros coletados")
    except Exception as e:
        print("❌ Erro ao extrair TRF3:", e)

# 📁 Exporta os dados para Excel
def salvar_em_excel():
    df = pd.DataFrame(dados, columns=["TRF", "Subseção Judiciária", "Cidade", "UF"])
    if df.empty:
        print("❌ Nenhum dado foi extraído. Verifique os seletores ou o carregamento da página.")
    else:
        data_hoje = datetime.today().strftime('%d-%m-%Y')
        nome_arquivo = f"jurisdicoes_trf3_{data_hoje}.xlsx"
        df.to_excel(nome_arquivo, index=False)
        print(f"✅ Arquivo Excel gerado com sucesso: {nome_arquivo}")

# ▶️ Execução
extrair_trf3()
salvar_em_excel()
driver.quit()