#Este é um código super básico que extrai noticias da página principal do NDMais Florianopolis
#Foi feito no Colab

# -*- coding: utf-8 -*-
#"""WebScraping-superBasico.ipynb

#Automatically generated by Colaboratory.

import requests # para requisições http
import json # para gerar JSON a partir de objetos do Python
from bs4 import BeautifulSoup # BeautifulSoup é uma biblioteca Python de extração de dados de arquivos HTML e XML.
from google.colab import files #importei esse pacote para fazer o download do arquivo JSON gerado


requisicaoDePagina = requests.get('https://ndmais.com.br/florianopolis/')

conteudo = requisicaoDePagina.content

#mostra o tipo Pyhton da página
print(type(requisicaoDePagina.content))

#joga para a variável site todo o conteúdo da página passada pelo requests.get()
site = BeautifulSoup(conteudo, 'html.parser')

#imprime o site inteiro, como o original 
print(site)

#joga para a variável noticias todos os elementos "article", que é onde está cada uma das manchetes do site princial 
noticias = site.findAll("article")

#imprime tipo Python de noticias
print(type(noticias))


#cria uma variável do tipo lista para guardar os dados em um JSON
resposta = []
#cria uma variável para numerar as noticias
noticia_nr = 1

#faz um laço na lista noticias (no plural), atribuindo cada item da lista para a variável noticia (no singular)
for noticia in noticias:

  #encontra nas tags do HTMO título, resumo e onde está publicada cada uma das noticias, e joga para as respectivas variáveis
  titulo = noticia.find("h2", {"class" : "title-text"})
  resumo = noticia.find("p", {"class" : "resume"})
  onde = noticia.find("a", {"class" : "hat"})
  
  #joga o texto de cada uma das tags
  tit = titulo.text
  ond = onde.text
  print("Título:", tit)
  print("Onde:", ond)

  #como pode não haver resumo em algumas notícias, é feito um teste.  
  if resumo:
    res = resumo.text
    print("Resumo:", res)
  else:
    res = "Sem resumo"
    print(res)

  #um print para separa as noticias
  print("....")

  # Cria uma espécie de dicionario para depois jogar para o JSON
  dados = {'NUMERO': str(noticia_nr), 'TITULO': tit, 'RESUMO': res, 'ONDE': ond}

  # Pendura o dicionario em uma lista e incrementa a variável que conta o número de noticias
  resposta.append(dados)
  noticia_nr += 1

#final do laço que percorre a lista de notícias

#apenas dois prints para mostrar o tipo da resposta e a resposta transformada em string
print("Tipo da resposta", type(resposta))
print(' '.join(map(str, resposta))) 


# Converte os objetos Pyhton em objeto JSON e exporta para o noticias.json
with open('noticias.json', 'w') as arquivo:
  arquivo.write(str(json.dumps(resposta, indent=4)))
print("Created Json File")

#faz o download usando a boblioteca do Colab
files.download('noticias.json')