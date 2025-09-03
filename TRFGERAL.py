from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from datetime import datetime
import requests

# Configuração do navegador
options = Options()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 20)

dados = []

# Função para obter cidades por UF
def obter_cidades_por_uf(uf_codigo):
    url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf_codigo}/municipios"
    resposta = requests.get(url)
    if resposta.status_code == 200:
        municipios = resposta.json()
        return set(m['nome'] for m in municipios)
    else:
        print(f"❌ Erro ao buscar cidades do UF {uf_codigo}")
        return set()

# Dicionário de cidades por UF
ufs_cidades = {uf: obter_cidades_por_uf(uf) for uf in range(11, 54)}

# Função auxiliar para identificar UF
def identificar_uf(cidade):
    for uf, cidades in ufs_cidades.items():
        if cidade in cidades:
            return uf
    return "Desconhecido"

# TRF1
def extrair_trf1():
    driver.get("https://portal.trf1.jus.br/portaltrf1/varas-federais/enderecos-das-varas-federais.htm")
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//table//tr")))
        linhas = driver.find_elements(By.XPATH, "//table//tr")[1:]
        for linha in linhas:
            colunas = linha.find_elements(By.TAG_NAME, "td")
            if len(colunas) >= 2:
                cidade = colunas[0].text.strip()
                subsecao = colunas[1].text.strip()
                uf = identificar_uf(cidade)
                dados.append({"TRF": "TRF1", "Subseção Judiciária": subsecao, "Cidade": cidade, "UF": uf})
        print(f"✅ TRF1: {len([d for d in dados if d['TRF'] == 'TRF1'])} registros coletados")
    except Exception as e:
        print("❌ Erro ao extrair TRF1:", e)

# TRF2
def extrair_trf2():
    driver.get("https://www10.trf2.jus.br/portal/enderecos-das-varas/")
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//table//tr")))
        linhas = driver.find_elements(By.XPATH, "//table//tr")[1:]
        for linha in linhas:
            colunas = linha.find_elements(By.TAG_NAME, "td")
            if len(colunas) >= 2:
                cidade = colunas[0].text.strip()
                subsecao = colunas[1].text.strip()
                uf = identificar_uf(cidade)
                dados.append({"TRF": "TRF2", "Subseção Judiciária": subsecao, "Cidade": cidade, "UF": uf})
        print(f"✅ TRF2: {len([d for d in dados if d['TRF'] == 'TRF2'])} registros coletados")
    except Exception as e:
        print("❌ Erro ao extrair TRF2:", e)

# TRF3
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
                dados.append({"TRF": "TRF3", "Subseção Judiciária": subsecao, "Cidade": cidade, "UF": uf})
        print(f"✅ TRF3: {len([d for d in dados if d['TRF'] == 'TRF3'])} registros coletados")
    except Exception as e:
        print("❌ Erro ao extrair TRF3:", e)

# TRF4
def extrair_trf4():
    driver.get("https://www.trf4.jus.br/trf4/controlador.php?acao=pagina_visualizar&id_pagina=179")
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//table//tr")))
        linhas = driver.find_elements(By.XPATH, "//table//tr")[1:]
        for linha in linhas:
            colunas = linha.find_elements(By.TAG_NAME, "td")
            if len(colunas) >= 2:
                cidade = colunas[0].text.strip()
                subsecao = colunas[1].text.strip()
                uf = identificar_uf(cidade)
                dados.append({"TRF": "TRF4", "Subseção Judiciária": subsecao, "Cidade": cidade, "UF": uf})
        print(f"✅ TRF4: {len([d for d in dados if d['TRF'] == 'TRF4'])} registros coletados")
    except Exception as e:
        print("❌ Erro ao extrair TRF4:", e)

# TRF5
def extrair_trf5():
    driver.get("https://www.trf5.jus.br/index.php/enderecos-das-varas")
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//table//tr")))
        linhas = driver.find_elements(By.XPATH, "//table//tr")[1:]
        for linha in linhas:
            colunas = linha.find_elements(By.TAG_NAME, "td")
            if len(colunas) >= 2:
                cidade = colunas[0].text.strip()
                subsecao = colunas[1].text.strip()
                uf = identificar_uf(cidade)
                dados.append({"TRF": "TRF5", "Subseção Judiciária": subsecao, "Cidade": cidade, "UF": uf})
        print(f"✅ TRF5: {len([d for d in dados if d['TRF'] == 'TRF5'])} registros coletados")
    except Exception as e:
        print("❌ Erro ao extrair TRF5:", e)

# TRF6
def extrair_trf6():
    driver.get("https://www.trf6.jus.br/enderecos-das-varas/")
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//table//tr")))
        linhas = driver.find_elements(By.XPATH, "//table//tr")[1:]
        for linha in linhas:
            colunas = linha.find_elements(By.TAG_NAME, "td")
            if len(colunas) >= 2:
                cidade = colunas[0].text.strip()
                subsecao = colunas[1].text.strip()
                uf = identificar_uf(cidade)
                dados.append({"TRF": "TRF6", "Subseção Judiciária": subsecao, "Cidade": cidade, "UF": uf})
        print(f"✅ TRF6: {len([d for d in dados if d['TRF'] == 'TRF6'])} registros coletados")
    except Exception as e:
        print("❌ Erro ao extrair TRF6:", e)

# Exporta para Excel
def salvar_em_excel():
    df = pd.DataFrame(dados, columns=["TRF", "Subseção Judiciária", "Cidade", "UF"])
    if df.empty:
        print("❌ Nenhum dado foi extraído.")
    else:
        data_hoje = datetime.today().strftime('%Y-%m-%d')
        nome_arquivo = f"jurisdicoes_trfs_{data_hoje}.xlsx"
        df.to_excel(nome_arquivo, index=False)
        print(f"✅ Arquivo Excel gerado com sucesso: {nome_arquivo}")

# Execução
extrair_trf1()
extrair_trf2()
extrair_trf3()
extrair_trf4()
extrair_trf5()
extrair_trf6()
salvar_em_excel()
driver.quit()