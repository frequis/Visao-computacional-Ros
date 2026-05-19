import cv2
import numpy as np

def carregar_imagem(caminho_imagem):
    img = cv2.imread(caminho_imagem)
    if img is None:
        raise ValueError(f"Imagem não encontrada em: {caminho_imagem}")
    return img

def converter_escala_cinza(imagem_bgr):
    B, G, R = imagem_bgr[:, :, 0], imagem_bgr[:, :, 1], imagem_bgr[:, :, 2]
    # Fórmula da luminância
    return (0.299 * R + 0.587 * G + 0.114 * B).astype(np.uint8)

def convolucao_2d(imagem, kernel):
    alt_i, larg_i = imagem.shape
    alt_k, larg_k = kernel.shape
    pad_alt, pad_larg = alt_k // 2, larg_k // 2
    
    # Preenchimento com zeros para manter o tamanho
    img_pad = np.pad(imagem, ((pad_alt, pad_alt), (pad_larg, pad_larg)), mode='reflect')
    resultado = np.zeros_like(imagem, dtype=np.float32)
    
    for i in range(alt_i):
        for j in range(larg_i):
            regiao = img_pad[i:i+alt_k, j:j+larg_k]
            resultado[i, j] = np.sum(regiao * kernel)
            
    return resultado

def aplicar_blur_gaussiano(imagem_cinza):
    kernel = np.array([
        [1, 2, 1],
        [2, 4, 2],
        [1, 2, 1]
    ]) / 16.0
    return convolucao_2d(imagem_cinza, kernel)