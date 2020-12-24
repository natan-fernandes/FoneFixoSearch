import argparse
import requests
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--nome', help='Nome do dono da linha', nargs='+')
parser.add_argument('-c', '--cidade', help='Cidade', nargs='+')
parser.add_argument('-t', '--telefone', help='Parte do telefone fixo', nargs='+')
args = parser.parse_args()

nome = '&nome='
if args.nome is not None:
    nome += '*+*'.join(args.nome).lower() + '*'

telefone = '&telefone='
if args.telefone is not None:
    telefone += '*' + '*'.join(args.telefone) + '*'

cidade = '&cidade='
if args.cidade is not None:
    cidade += ('*+*'.join(args.cidade)).lower() + '*'

link = f'https://www.telenumeros.com/?dir=pesquisa{nome}{telefone}{cidade}'

print()
req = requests.get(link)
soup = BeautifulSoup(req.content, 'html.parser')
try:
    busca = soup.find_all('td', class_='cerca')
    print(f'Nome: {busca[0].text.strip()}')

    busca = soup.find_all('td', class_='dativ')
    print(f'{busca[0].text.replace("Telefone ", "Telefone: ")}')

    busca = soup.find_all('td', class_='dati')
    print(f'Logradouro: {busca[0].text}')
    print(f'{busca[1].text.replace("Cidade ", "Cidade: ", 1)}')
    print(f'{busca[2].text.replace("Estado (", "Estado: ", 1).replace(")", "", 1)}')

except:
    print('Sem resultados')
