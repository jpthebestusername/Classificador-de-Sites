from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
import re
import time

app = Flask(__name__)
CORS(app)

# Lista de segmentos bloqueados e variações
SEGMENTOS_BLOQUEADOS = [
    "contabilidade", "contábil", "contador", "escritório", "assessoria", "consultoria", "contabil", "contac"
]

@app.route("/")
def index():
    return render_template("index.html")

def verificar_dominio(site):
    dominio = site.lower()
    dominio = re.sub(r"(https?://)?(www\.)?", "", dominio)
    dominio = re.sub(r"\.com(\.br)?|\.br|\.net|\.org", "", dominio)

    for palavra in SEGMENTOS_BLOQUEADOS:
        if palavra in dominio:
            return f"{site} → Segmento bloqueado: {palavra.capitalize()}"
    
    return None

def obter_texto_completo(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    def tentar_requisicao(link):
        try:
            resp = requests.get(link, timeout=6, headers=headers)
            if resp.status_code in [200, 301, 302, 403, 503]:
                return BeautifulSoup(resp.text, "html.parser").get_text(separator=' ', strip=True).lower()
        except requests.exceptions.RequestException:
            pass
        return None

    try:
        texto_total = tentar_requisicao(url)
        if texto_total is None:
            return None

        soup = BeautifulSoup(requests.get(url, timeout=6, headers=headers).text, "html.parser")
        links = [a.get("href") for a in soup.find_all("a", href=True)]
        links_filtrados = []

        for link in links:
            if link.startswith("/") or link.startswith(url):
                full_url = urljoin(url, link)
                if full_url not in links_filtrados:
                    links_filtrados.append(full_url)
            if len(links_filtrados) >= 3:
                break

        for sub_url in links_filtrados:
            texto = tentar_requisicao(sub_url)
            if texto:
                texto_total += " " + texto

        return texto_total

    except Exception:
        return None

def verificar_site_fora_do_ar(url, tentativas=5, delay=5):
    for _ in range(tentativas):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code in [200, 301, 302, 403, 503]:
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(delay)
    return False

def analisar_site(site):
    try:
        url = site if site.startswith("http") else f"https://{site}"

        dominio_resultado = verificar_dominio(site)
        if dominio_resultado:
            return dominio_resultado

        if not verificar_site_fora_do_ar(url):
            return f"{site} → Site fora do ar"

        try:
            soup = BeautifulSoup(requests.get(url, timeout=10).text, "html.parser")
        except:
            return f"{site} → Site fora do ar"

        # Verificação do título
        titulo = soup.title.string.lower() if soup.title and soup.title.string else ""
        for palavra in SEGMENTOS_BLOQUEADOS:
            if palavra in titulo:
                return f"{site} → Segmento bloqueado: {palavra.capitalize()}"

        texto = obter_texto_completo(url)
        if texto is None:
            return f"{site} → Site fora do ar"

        cabecalho = soup.find('header')
        rodape = soup.find('footer')

        for palavra in SEGMENTOS_BLOQUEADOS:
            if cabecalho and palavra in cabecalho.text.lower():
                return f"{site} → Segmento bloqueado: {palavra.capitalize()}"
            if rodape and palavra in rodape.text.lower():
                return f"{site} → Segmento bloqueado: {palavra.capitalize()}"

        palavras_repetidas = {}
        for palavra in SEGMENTOS_BLOQUEADOS:
            ocorrencias = texto.count(palavra)
            if ocorrencias >= 5:
                palavras_repetidas[palavra] = ocorrencias

        if palavras_repetidas:
            segmento = max(palavras_repetidas, key=palavras_repetidas.get)
            return f"{site} → Segmento bloqueado: {segmento.capitalize()} (palavra repetida)"

        return f"{site} → Liberado"

    except Exception:
        return f"{site} → Site fora do ar"

@app.route("/classificar", methods=["POST"])
def classificar():
    data = request.get_json()
    sites = [s.strip() for s in data.get("sites", []) if s.strip()]
    sites = list(set(sites))[:200]

    with ThreadPoolExecutor(max_workers=30) as executor:
        resultados = list(executor.map(analisar_site, sites))

    return jsonify(resultados=resultados)

if __name__ == "__main__":
    app.run(debug=True)
