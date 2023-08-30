from partidos import *

#Função de interagir com o usuario
ano, partidos, threshold = funcao_obter_filtro_usuario()

#Chamando a função normalizacao
funcao_normalizacao(partidos, ano, threshold)