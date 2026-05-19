import numpy as np
from .processamento import convolucao_2d

def detectar_bordas_sobel(imagem_suavizada):
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    sobel_y = np.array([[-1, -2, -1], [ 0,  0,  0], [ 1,  2,  1]])
    
    grad_x = convolucao_2d(imagem_suavizada, sobel_x)
    grad_y = convolucao_2d(imagem_suavizada, sobel_y)
    
    magnitude = np.sqrt(grad_x**2 + grad_y**2)
    magnitude = (magnitude / magnitude.max()) * 255
    return magnitude.astype(np.uint8)

def binarizar_bordas(imagem_bordas, limiar=100):
    # Tudo que for maior que o limiar vira borda (255)
    return np.where(imagem_bordas > limiar, 255, 0).astype(np.uint8)