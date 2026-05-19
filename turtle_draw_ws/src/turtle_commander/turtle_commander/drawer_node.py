import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import TeleportAbsolute, SetPen
import math
import sys
import os

# TRUQUE DE ARQUITETURA: Adiciona a raiz do projeto ao PATH do Python
# Isso resolve o "Problema 2" que encontrei na sua arquitetura
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
# Sobe na árvore até encontrar a pasta pipeline_visao (funciona via src/ e via install/)
caminho_raiz = diretorio_atual
for _ in range(10):
    if os.path.isdir(os.path.join(caminho_raiz, 'pipeline_visao')):
        break
    caminho_raiz = os.path.dirname(caminho_raiz)
if caminho_raiz not in sys.path:
    sys.path.append(caminho_raiz)

# Agora podemos importar nossos módulos NumPy livremente
from pipeline_visao.processamento import carregar_imagem, converter_escala_cinza, aplicar_blur_gaussiano
from pipeline_visao.detector_bordas import detectar_bordas_sobel, binarizar_bordas
from pipeline_visao.mapeamento import extrair_coordenadas

class DrawerNode(Node):
    # Distância acima da qual é considerado um salto entre contornos (levanta a caneta)
    JUMP_THRESHOLD = 0.5

    def __init__(self):
        super().__init__('drawer_node')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.subscriber_ = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        self._teleport = self.create_client(TeleportAbsolute, '/turtle1/teleport_absolute')
        self._set_pen = self.create_client(SetPen, '/turtle1/set_pen')

        self.pose = Pose()
        self.caminho = self.processar_pipeline_visao()
        self.alvo_atual = 0
        self._caneta_levantada = True  # começa levantada até chegar na primeira posição

        # O Timer define a taxa de atualização do controle (0.05 seg = 20 Hz)
        self.timer = self.create_timer(0.05, self.mover_tartaruga)
        self.get_logger().info(f'Iniciando o Turtle Draw! {len(self.caminho)} pontos no caminho.')

    def _levantar_caneta(self):
        req = SetPen.Request()
        req.off = 1
        self._set_pen.call_async(req)
        self._caneta_levantada = True

    def _baixar_caneta(self):
        req = SetPen.Request()
        req.r, req.g, req.b = 255, 255, 255
        req.width = 2
        req.off = 0
        self._set_pen.call_async(req)
        self._caneta_levantada = False

    def _teleportar(self, x, y):
        req = TeleportAbsolute.Request()
        req.x, req.y, req.theta = float(x), float(y), 0.0
        self._teleport.call_async(req)

    def processar_pipeline_visao(self):
        caminho_img = os.environ.get(
            'IMAGEM_ENTRADA',
            os.path.join(caminho_raiz, 'imagens', 'turtle_teste.png')
        )
        self.get_logger().info(f'Processando imagem em: {caminho_img}')

        img = carregar_imagem(caminho_img)
        cinza = converter_escala_cinza(img)
        blur = aplicar_blur_gaussiano(cinza)
        bordas = detectar_bordas_sobel(blur)
        binaria = binarizar_bordas(bordas, 100)

        return extrair_coordenadas(binaria)

    def pose_callback(self, msg):
        self.pose = msg

    def mover_tartaruga(self):
        if self.alvo_atual >= len(self.caminho):
            self.get_logger().info('Desenho Concluído com Sucesso!')
            self.timer.cancel()
            return

        alvo_x, alvo_y = self.caminho[self.alvo_atual]

        # Matemática para encontrar o destino
        dist_x = alvo_x - self.pose.x
        dist_y = alvo_y - self.pose.y
        distancia = math.sqrt(dist_x**2 + dist_y**2)

        # Salto entre contornos: levanta caneta e teleporta sem desenhar
        if distancia > self.JUMP_THRESHOLD:
            self._levantar_caneta()
            self._teleportar(alvo_x, alvo_y)
            self.alvo_atual += 1
            return

        # Abaixa a caneta assim que estiver num trecho contíguo
        if self._caneta_levantada:
            self._baixar_caneta()

        angulo_alvo = math.atan2(dist_y, dist_x)
        erro_angular = angulo_alvo - self.pose.theta
        # Normaliza o ângulo entre -pi e pi
        erro_angular = math.atan2(math.sin(erro_angular), math.cos(erro_angular))

        cmd = Twist()

        # Lógica de Controle: Gira primeiro, anda depois
        if abs(erro_angular) > 0.15:
            cmd.angular.z = 2.0 * erro_angular
            cmd.linear.x = 0.0
        elif distancia > 0.15:
            cmd.linear.x = 2.0 * distancia
            cmd.angular.z = 0.0
        else:
            # Chegou no alvo, avança para o próximo ponto da lista
            self.alvo_atual += 1

        self.publisher_.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = DrawerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
