# Turtle Draw — Visão Computacional com ROS 2

Pipeline completa de visão computacional implementada do zero (NumPy puro) que extrai contornos de uma imagem e comanda a tartaruga do Turtlesim para desenhá-los.

## Resultado

Teste com `dog.jpg` (1280×720 px) — 2304 pontos de contorno mapeados para o espaço do Turtlesim:

![Resultado dog.jpg](docs/resultado_dog.png)

A tartaruga percorre somente as bordas detectadas pelo operador de Sobel. Saltos entre contornos desconexos são feitos com a caneta levantada (sem riscar), garantindo que apenas o contorno real da imagem seja desenhado.

## Estrutura

```
Visao-computacional-Ros/
├── pipeline_visao/              ← pipeline de visão (NumPy + cv2 só para carregar)
│   ├── __init__.py
│   ├── processamento.py         # escala de cinza + blur gaussiano
│   ├── detector_bordas.py       # operador de Sobel + binarização
│   └── mapeamento.py            # mapeamento de pixels → coordenadas Turtlesim
├── turtle_draw_ws/
│   └── src/
│       └── turtle_commander/    ← pacote ROS 2
│           ├── package.xml
│           ├── setup.py
│           ├── resource/
│           │   └── turtle_commander
│           ├── scripts/
│           │   └── drawer_node  # entry-point ros2 run
│           └── turtle_commander/
│               ├── __init__.py
│               └── drawer_node.py
├── imagens/
│   ├── dog.jpg                  ← cachorro (1280×720 px)
│   └── star.png                 ← estrela (imagem padrão, usada sem IMAGEM_ENTRADA)
└── README.md
```

## Dependências

- Python 3.10+
- NumPy
- OpenCV (`cv2`) — apenas para carregar a imagem
- ROS 2 Jazzy
- pacote `turtlesim`

```bash
pip install numpy opencv-python
```

## Como executar

### 1. Compilar o pacote ROS 2

```bash
cd turtle_draw_ws
source /opt/ros/jazzy/setup.bash
colcon build --packages-select turtle_commander
source install/setup.bash
```

### 2. Iniciar o Turtlesim (Terminal 1)

```bash
source /opt/ros/jazzy/setup.bash
ros2 run turtlesim turtlesim_node
```

### 3. Executar o nó desenhador (Terminal 2)

```bash
cd turtle_draw_ws
source /opt/ros/jazzy/setup.bash && source install/setup.bash
ros2 run turtle_commander drawer_node
```

Para escolher a imagem via variável de ambiente:

```bash
# cachorro
IMAGEM_ENTRADA=/home/frequis/ros/Visao-computacional-Ros/imagens/dog.jpg ros2 run turtle_commander drawer_node

# estrela (padrão)
IMAGEM_ENTRADA=/home/frequis/ros/Visao-computacional-Ros/imagens/star.png ros2 run turtle_commander drawer_node
```

### 4. Testar a pipeline isoladamente (sem ROS)

```python
import sys
sys.path.insert(0, '.')   # executar da raiz do repositório

from pipeline_visao.processamento import carregar_imagem, converter_escala_cinza, aplicar_blur_gaussiano
from pipeline_visao.detector_bordas import detectar_bordas_sobel, binarizar_bordas
from pipeline_visao.mapeamento import extrair_coordenadas

img    = carregar_imagem('imagens/star.png')   # ou dog.jpg
cinza  = converter_escala_cinza(img)
blur   = aplicar_blur_gaussiano(cinza)
bordas = detectar_bordas_sobel(blur)
bin_   = binarizar_bordas(bordas, 100)
pontos = extrair_coordenadas(bin_)
print(f'{len(pontos)} pontos mapeados para o Turtlesim')
```

## Resultados dos Testes

### dog.jpg — 1280 × 720 px

![Resultado dog.jpg](docs/resultado_dog.png)

### star.png — 736 × 386 px

![Resultado star.png](docs/resultado_star.png)