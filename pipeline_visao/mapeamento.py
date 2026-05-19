import numpy as np

def extrair_coordenadas(imagem_binaria, escala_max=10.0):
    # Encontra os índices dos pixels brancos (borda)
    # np.where retorna (linhas, colunas) = (Y, X)
    pontos_y, pontos_x = np.where(imagem_binaria == 255)
    
    if len(pontos_x) == 0:
        return []

    # O Turtlesim tem origem (0,0) no canto inferior esquerdo.
    # As imagens têm origem no canto superior esquerdo. Invertemos o Y.
    alt, larg = imagem_binaria.shape
    pontos_y = alt - pontos_y
    
    # Normaliza para a escala do Turtlesim (0 a 11, mas usamos 10 pra dar margem)
    pontos_x = (pontos_x / larg) * escala_max + 0.5
    pontos_y = (pontos_y / alt) * escala_max + 0.5
    
    coordenadas = list(zip(pontos_x, pontos_y))
    
    # Subamostragem: Pega 1 ponto a cada 3 para a tartaruga não demorar horas!
    coordenadas = coordenadas[::3] 
    
    # Rastreio de Contorno (Vizinho Mais Próximo)
    caminho_ordenado = [coordenadas.pop(0)]
    while coordenadas:
        ultimo = caminho_ordenado[-1]
        # Distância Euclidiana para todos os pontos restantes
        distancias = [((p[0]-ultimo[0])**2 + (p[1]-ultimo[1])**2) for p in coordenadas]
        idx_mais_proximo = np.argmin(distancias)
        caminho_ordenado.append(coordenadas.pop(idx_mais_proximo))
        
    return caminho_ordenado