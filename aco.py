from numpy.random import choice
from scipy import spatial

import matplotlib.pyplot as plt
import random
import math

class Formiga:
  def __init__(self, ponto_atual):
    self.ponto_atual = ponto_atual
    self.rota = [ponto_atual]

  def andar(self, ponto):
    self.ponto_atual = ponto
    self.rota.append(ponto)

class Ponto:
  def __init__(self, x, y):
    self.x = x
    self.y = y

class Caminho:
  def __init__(self, ponto_i, ponto_j):
    self.ponto_i = ponto_i
    self.ponto_j = ponto_j
    self.comprimento = math.sqrt((ponto_i.x - ponto_j.x)**2 + (ponto_i.y - ponto_j.y)**2)
    self.feromonio = 0
    self.formigas_passantes = []

  def contem(self, formiga):
    if self.ponto_i == formiga.ponto_atual:
      return self.ponto_j not in formiga.rota
    elif self.ponto_j == formiga.ponto_atual:
      return self.ponto_i not in formiga.rota
    else:
      return False

  def ponto_adjacente(self, ponto):
    if self.ponto_i == ponto:
      return self.ponto_j
    elif self.ponto_j == ponto:
      return self.ponto_i
    else:
      return None

class Grafo:
  def __init__(self, caminhos):
    self.caminhos = caminhos
    self.melhor_rota = []
    self.comprimento_melhor_rota = 0

  def atualizas_melhor_rota(self, melhor_rota):
    self.melhor_rota = melhor_rota
    self.comprimento_melhor_rota = sum([math.sqrt((i.x - j.x)**2 + (i.y - j.y)**2) for [i, j] in melhor_rota])

  def possiveis_caminhos(self, formiga):
    return [caminho for caminho in self.caminhos if caminho.contem(formiga)]

# Atributos do ACO

n = 3
p = 0.2
alfa = 0.5
beta = 0.7
iteracoes = 10 # quantidade de iterações que irão acontecer até a parada da otimização

# Problema
#Para esse exemplo iremos encontrar a melhor rota (menor distância total) que percorre todos os pontos de um grafo gerado aleatoriamente e completamente conectado (cada ponto tem um #caminho par todos os outros).

qtd_pontos = 6 # quantidade de pontos do grafo que será gerado

# Inicialização do grafo

# criando os pontos
pontos = []

for _ in range(qtd_pontos):
  pontos.append(Ponto(random.uniform(-100, 100), random.uniform(-100, 100)))

# criando os caminhos
caminhos = []

i = 0
while i < qtd_pontos - 1:
  j = i + 1

  while j < qtd_pontos:
    caminhos.append(Caminho(pontos[i], pontos[j]))
    j += 1
  
  i += 1

# criando o grafo
grafo = Grafo(caminhos)

# Grafo criado

for ponto in pontos:
    plt.plot(ponto.x, ponto.y, marker='o', color='r')

x = []
y = []

for caminho in caminhos:
  x_i = caminho.ponto_i.x
  x_j = caminho.ponto_j.x
  y_i = caminho.ponto_i.y
  y_j = caminho.ponto_j.y

  x_texto = (x_i + x_j) / 2
  y_texto = (y_i + y_j) / 2

  plt.text(x_texto, y_texto, "{:.2f}".format(caminho.comprimento))

  x.append(x_i)
  x.append(x_j)
  y.append(y_i)
  y.append(y_j)

plt.plot(x, y, color='c')

plt.show()

# Inicialização da colônia

def inicializar_colonia():
  formigas = []

  for _ in range(n):
    formigas.append(Formiga(random.choice(pontos)))

  return formigas

# Escolha do caminho

def escolher_caminho(possiveis_caminhos):
  denominador = sum([(caminho.feromonio)**alfa * (1 / caminho.comprimento)**beta for caminho in possiveis_caminhos])
  distribuicao_probabilidades = None

  if denominador == 0:
    distribuicao_probabilidades = [1 / len(possiveis_caminhos)  for _ in possiveis_caminhos]
  else:
    distribuicao_probabilidades = [((caminho.feromonio)**alfa * (1 / caminho.comprimento)**beta) / denominador for caminho in possiveis_caminhos]

  return choice(possiveis_caminhos, 1, p=distribuicao_probabilidades)[0]

# Atualização de feromônio

def distancia_rota(rota):
  distancia_rota = 0

  for i in range(0, len(rota) - 1):
    distancia = math.sqrt((rota[i].x - rota[i + 1].x)**2 + (rota[i].y - rota[i + 1].y)**2)
    distancia_rota += distancia

  return distancia_rota

def atualizar_feromonios(caminhos):
  for caminho in caminhos:
    soma_heuristica = sum([1 / distancia_rota(formiga.rota) for formiga in caminho.formigas_passantes])
    caminho.feromonio = (1 - p) * caminho.feromonio + soma_heuristica
    caminho.formigas_passantes = []

# Movimentação da formiga

def movimentar_formiga(formiga, grafo):
  while True:
    possiveis_caminhos = grafo.possiveis_caminhos(formiga)

    if possiveis_caminhos == []:
      break

    caminho_escolhido = escolher_caminho(possiveis_caminhos)
    caminho_escolhido.formigas_passantes.append(formiga)
    formiga.andar(caminho_escolhido.ponto_adjacente(formiga.ponto_atual))

# Otimização

melhor_rota = None
distancia_melhor_rota = 0

for _ in range(iteracoes):
  formigas = inicializar_colonia()

  for formiga in formigas:
    movimentar_formiga(formiga, grafo)

    if melhor_rota is None or distancia_rota(melhor_rota) > distancia_rota(formiga.rota):
      melhor_rota = formiga.rota
      distancia_melhor_rota = distancia_rota(formiga.rota)

  atualizar_feromonios(grafo.caminhos)

  # mostrando a melhor rota a cada iteracao
  for ponto in pontos:
    plt.plot(ponto.x, ponto.y, marker='o', color='r')

  x = []
  y = []

  for caminho in caminhos:
    x_i = caminho.ponto_i.x
    x_j = caminho.ponto_j.x
    y_i = caminho.ponto_i.y
    y_j = caminho.ponto_j.y

    x_texto = (x_i + x_j) / 2
    y_texto = (y_i + y_j) / 2

    plt.text(x_texto, y_texto, "{:.2f}".format(caminho.comprimento))

    x.append(x_i)
    x.append(x_j)
    y.append(y_i)
    y.append(y_j)

  plt.plot(x, y, color='c')

  x = []
  y = []

  for ponto in melhor_rota:
    x.append(ponto.x)
    y.append(ponto.y)

  plt.plot(x, y, color='y')

  plt.show()
  print("{:.2f}".format(distancia_melhor_rota))