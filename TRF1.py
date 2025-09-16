from playwright.sync_api import sync_playwright
import pandas as pd
from datetime import datetime

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.trf1.jus.br/trf1/jurisdicao/jurisdicoes-das-varas-federais", wait_until="networkidle")
    page.wait_for_timeout(5000)  # espera 5 segundos

    # Captura todo o texto visível da página
    texto = page.content()
    texto_visivel = page.evaluate("document.body.innerText")
    browser.close()

# Processa o texto
linhas = texto_visivel.split("\n")
dados = []
trf = "TRF1"
jurisdicao_atual = ""

for linha in linhas:
    if "Seção Judiciária" in linha or "Subseção Judiciária" in linha:
        jurisdicao_atual = linha.strip()
    elif linha.strip():
        cidade = linha.strip()
        uf = ""  # Pode ser preenchido com lógica adicional
        dados.append({
            "TRF": trf,
            "Jurisdição": jurisdicao_atual,
            "Cidade": cidade,
            "UF": uf
        })

# Cria planilha
df = pd.DataFrame(dados)
data_hoje = datetime.today().strftime('%Y-%m-%d')
nome_arquivo = f"jurisdicoes_trf1_{data_hoje}.xlsx"
df.to_excel(nome_arquivo, index=False)

print(f"✅ Planilha salva como: {nome_arquivo}")