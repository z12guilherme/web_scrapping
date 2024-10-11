import requests
from bs4 import BeautifulSoup
import json

def coletar_informacoes(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a página: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    informações = {}

    informações['título'] = soup.title.string if soup.title else None
    informações['descricao'] = soup.meta.get('description') if soup.meta else None
    informações['palavras_chave'] = soup.meta.get('keywords') if soup.meta else None

    elementos = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span', 'div', 'img', 'a'])
    for elemento in elementos:
        if elemento.text:
            if elemento.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                informações.setdefault(f'título_{elemento.name}', []).append(elemento.text)
            elif elemento.name == 'p':
                informações.setdefault('parágrafo', []).append(elemento.text)
            elif elemento.name == 'img':
                informações.setdefault('imagem', []).append(elemento.get('src'))
            elif elemento.name == 'a':
                informações.setdefault('link', []).append(elemento.get('href'))
            elif elemento.name in ['span', 'div']:
                informações.setdefault(elemento.text, []).append(elemento.text)

    tabelas = soup.find_all('table')
    for tabela in tabelas:
        informações.setdefault(f'tabela_{tabela.get("id")}', []).append([])
        for linha in tabela.find_all('tr'):
            informações[f'tabela_{tabela.get("id")}'][-1].append([celula.text for celula in linha.find_all('td')])

    listas = soup.find_all(['ul', 'ol'])
    for lista in listas:
        informações.setdefault(f'lista_{lista.get("id")}', []).append([item.text for item in lista.find_all('li')])

    return informações

def exportar_informacoes_para_txt(informações, arquivo_saida):
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        for chave, valor in informações.items():
            f.write(f"{chave}: {valor}\n\n")

def main():
    url = input("Insira a URL do site que você deseja coletar informações --> ")
    informações = coletar_informacoes(url)
    if informações:
        arquivo_saida = "informacoes.txt"
        exportar_informacoes_para_txt(informações, arquivo_saida)
        print(f"Informações exportadas para {arquivo_saida}")

if __name__ == "__main__":
    main()