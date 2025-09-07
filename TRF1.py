# 📦 Imports
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
# options.add_argument('--headless')  # opcional: executa sem abrir janela
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 20)

# 📍 Lista para armazenar os dados
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

# ⚖️ Função específica para o TRF
def extrair_trf1():
    driver.get("https://www.trf1.jus.br/trf1/jurisdicao/jurisdicoes-das-varas-federais")

    try:
        # Aguarda qualquer <h3> aparecer — são os títulos de UF
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))

        # Captura todos os elementos <h3> e <p> na ordem
        elementos = driver.find_elements(By.XPATH, "//div[contains(@class, 'conteudo')]/*")

        uf_atual = ""
        for el in elementos:
            tag = el.tag_name.lower()
            texto = el.text.strip()

            if tag == "h3" and texto:
                uf_atual = texto

            elif tag == "p" and "Subseção Judiciária de" in texto and ":" in texto:
                partes = texto.split(":")
                if len(partes) == 2:
                    subsecao = partes[0].replace("Subseção Judiciária de", "").strip()
                    cidades = [c.strip() for c in partes[1].split(",")]
                    for cidade in cidades:
                        uf = identificar_uf(cidade)
                        dados.append({
                            "TRF": "TRF1",
                            "Subseção Judiciária": subsecao,
                            "Cidade": cidade,
                            "UF": uf
                        })
        print(f"✅ TRF1: {len([d for d in dados if d['TRF'] == 'TRF1'])} registros coletados")
    except Exception as e:
        print(f"❌ Erro ao extrair TRF1: {type(e).__name__} - {e}")

# 📁 Exporta os dados para Excel
def salvar_em_excel():
    df = pd.DataFrame(dados, columns=["TRF", "Subseção Judiciária", "Cidade", "UF"])
    if df.empty:
        print("❌ Nenhum dado foi extraído.")
    else:
        data_hoje = datetime.today().strftime('%Y-%m-%d')
        nome_arquivo = f"jurisdicoes_trf1_{data_hoje}.xlsx"
        df.to_excel(nome_arquivo, index=False)
        print(f"✅ Arquivo Excel gerado com sucesso: {nome_arquivo}")

# ▶️ Execução
extrair_trf1()
salvar_em_excel()
driver.quit()