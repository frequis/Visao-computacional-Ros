import sys
import numpy as np
import matplotlib.pyplot as plt
sys.path.insert(0, '.')

from pipeline_visao.processamento import carregar_imagem, converter_escala_cinza, aplicar_blur_gaussiano
from pipeline_visao.detector_bordas import detectar_bordas_sobel, binarizar_bordas
from pipeline_visao.mapeamento import extrair_coordenadas

imagem = sys.argv[1] if len(sys.argv) > 1 else 'imagens/star.png'
print(f"Processando: {imagem}")

img    = carregar_imagem(imagem)
cinza  = converter_escala_cinza(img)
blur   = aplicar_blur_gaussiano(cinza)
bordas = detectar_bordas_sobel(blur)
bin_   = binarizar_bordas(bordas, 100)
pontos = extrair_coordenadas(bin_)

print(f"{len(pontos)} pontos prontos para o Turtlesim.")

xs, ys = zip(*pontos)

fig, axes = plt.subplots(2, 3, figsize=(14, 8))
fig.suptitle(f"Pipeline — {imagem}", fontsize=13)

# BGR -> RGB só para exibição
axes[0, 0].imshow(img[:, :, ::-1])
axes[0, 0].set_title("Original")

axes[0, 1].imshow(cinza, cmap="gray")
axes[0, 1].set_title("Escala de cinza")

axes[0, 2].imshow(blur, cmap="gray")
axes[0, 2].set_title("Blur gaussiano")

axes[1, 0].imshow(bordas, cmap="gray")
axes[1, 0].set_title("Bordas Sobel")

axes[1, 1].imshow(bin_, cmap="gray")
axes[1, 1].set_title(f"Binarização (limiar=100)")

axes[1, 2].scatter(xs, ys, s=0.5, c=range(len(xs)), cmap="plasma")
axes[1, 2].set_title(f"Caminho ({len(pontos)} pts)")
axes[1, 2].set_xlim(0, 11)
axes[1, 2].set_ylim(0, 11)
axes[1, 2].set_aspect("equal")

for ax in axes.flat:
    ax.axis("off")
axes[1, 2].axis("on")

plt.tight_layout()
plt.show()
