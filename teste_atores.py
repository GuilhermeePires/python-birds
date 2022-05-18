# -*- coding: utf-8 -*-
import math
from unittest.case import  TestCase


DESTRUIDO = 'Destruido'
ATIVO = 'Ativo'
GRAVIDADE = 10  # m/s^2

class AtorTestes(TestCase):
    def teste_valores_padrao(self):

        ator = Ator()
        self.assertEqual(0, ator.x)
        self.assertEqual(0, ator.y)
        self.assertEqual(ATIVO, ator.status)
        self.assertEqual('A', ator.caracter())

    def teste_valores_passados_por_parametro(self):

        ator = Ator(1, 2)
        self.assertEqual(1, ator.x)
        self.assertEqual(2, ator.y)
        self.assertEqual(ATIVO, ator.status)
        self.assertEqual('A', ator.caracter())

    def teste_ator_posicao(self):

        ator = Ator()
        x, y = ator.calcular_posicao(0)
        self.assertEqual(0, x)
        self.assertEqual(0, y)

        ator = Ator(0.3, 0.5)
        x, y = ator.calcular_posicao(10)
        self.assertEqual(0.3, x)
        self.assertEqual(0.5, y)
        


class Ator():
    """
    Classe que representa um ator. Ele representa um ponto cartesiano na tela.
    """
    _caracter_ativo = 'A'
    _caracter_destruido = ' '

    def __init__(self, x=0, y=0):
        """
        Método de inicialização da classe. Deve inicializar os parâmetros x, y, caracter e status

        :param x: Posição horizontal inicial do ator
        :param y: Posição vertical inicial do ator
        """
        self.y = y
        self.x = x
        self.status = ATIVO

    def caracter(self):
        return self._caracter_ativo if self.status == ATIVO else self._caracter_destruido

    def calcular_posicao(self, tempo):
        """
        Método que calcula a posição do ator em determinado tempo.
        Deve-se imaginar que o tempo começa em 0 e avança de 0,01 segundos

        :param tempo: o tempo do jogo
        :return: posição x, y do ator
        """
        return self.x, self.y

    def colidir(self, outro_ator, intervalo=1):
        """
        Método que executa lógica de colisão entre dois atores.
        Só deve haver colisão se os dois atores tiverem seus status ativos.
        Para colisão, é considerado um quadrado, com lado igual ao parâmetro intervalo, em volta do ponto onde se
        encontra o ator. Se os atores estiverem dentro desse mesmo quadrado, seus status devem ser alterados para
        destruido, seus caracteres para destruido também.

        :param outro_ator: Ator a ser considerado na colisão
        :param intervalo: Intervalo a ser considerado
        :return:
        """
        if self.status == ATIVO and outro_ator.status == ATIVO:
            delta_x = abs(self.x - outro_ator.x)
            delta_y = abs(self.y - outro_ator.y)
            if delta_x <= intervalo and delta_y <= intervalo:
                self.status=outro_ator.status=DESTRUIDO

    def teste_colisao_entre_atores_ativos(self):

        ator = Ator(2, 2)
        ator2 = Ator(2, 2)
        self.assert_colisao_atores_ativos(ator, ator2)
        self.assert_colisao_atores_ativos(Ator(2, 2), Ator(2, 3))
        self.assert_colisao_atores_ativos(Ator(2, 2), Ator(3, 3))
        self.assert_colisao_atores_ativos(Ator(2, 2), Ator(3, 2))
        self.assert_colisao_atores_ativos(Ator(2, 2), Ator(3, 1))
        self.assert_colisao_atores_ativos(Ator(2, 2), Ator(2, 1))
        self.assert_colisao_atores_ativos(Ator(2, 2), Ator(1, 1))
        self.assert_colisao_atores_ativos(Ator(2, 2), Ator(1, 2))
        self.assert_colisao_atores_ativos(Ator(2, 2), Ator(1, 3))

    def teste_colisao_entre_atores_ativos_com_intervalo(self):
        self.assert_colisao_atores_ativos(Ator(2, 2), Ator(2, 4), 2)

    def assert_colisao_atores_ativos(self, ator, ator2, intervalo=1):

        self.assertEqual(ator.status, ATIVO, 'Status deveria ser ativo antes da colisão')
        self.assertEqual(ator2.status, ATIVO, 'Status deveria ser ativo antes da colisão')
        ator.colidir(ator2, intervalo)
        self.assertEqual(ator2.status, DESTRUIDO, 'Status deveria ser destruido depois da colisão')
        self.assertEqual(ator.status, DESTRUIDO, 'Status deveria ser destruido depois da colisão')

    def assert_nao_colisao(self, ator, ator2):

        status_inicial_ator = ator.status
        status_inicial_ator_2 = ator2.status

        ator.colidir(ator2)

        self.assertEqual(status_inicial_ator, ator.status, 'Status de ator não deveria mudar')
        self.assertEqual(status_inicial_ator_2, ator2.status, 'Status de ator2 não deveria mudar')


    def teste_colisao_somente_um_ator_destruido(self):
        ator = Ator(2, 2)
        ator.colidir(ator, 0)
        ator2 = Ator(2, 2)
        self.assert_nao_colisao(ator, ator2)
        self.assert_nao_colisao(Ator(2, 3), ator)
        self.assert_nao_colisao(Ator(3, 3), ator)
        self.assert_nao_colisao(Ator(3, 2), ator)
        self.assert_nao_colisao(Ator(3, 1), ator)
        self.assert_nao_colisao(Ator(2, 1), ator)
        self.assert_nao_colisao(Ator(1, 1), ator)
        self.assert_nao_colisao(Ator(1, 2), ator)
        self.assert_nao_colisao(Ator(1, 3), ator)
        self.assert_nao_colisao(ator2, ator)
        self.assert_nao_colisao(Ator(2, 3), ator)
        self.assert_nao_colisao(Ator(3, 3), ator)
        self.assert_nao_colisao(Ator(3, 2), ator)
        self.assert_nao_colisao(Ator(3, 1), ator)
        self.assert_nao_colisao(Ator(2, 1), ator)
        self.assert_nao_colisao(Ator(1, 1), ator)
        self.assert_nao_colisao(Ator(1, 2), ator)
        self.assert_nao_colisao(Ator(1, 3), ator)


class Obstaculo(Ator):
    _caracter_ativo = 'O'


class Porco(Ator):
        _caracter_ativo = '@'
        _caracter_destruido = '+'


class DuploLancamentoExcecao(Exception):
    pass


class Passaro(Ator):
    velocidade_escalar = 10

    def __init__(self, x=0, y=0):
        """
        Método de inicialização de pássaro.

        Deve chamar a inicialização de ator. Além disso, deve armazenar a posição inicial e incializar o tempo de
        lançamento e angulo de lançamento

        :param x:
        :param y:
        """
        super().__init__(x, y)
        self._x_inicial = x
        self._y_inicial = y
        self._tempo_de_lancamento = None
        self._angulo_de_lancamento = None  # radianos

    def foi_lancado(self):
        """
        Método que retorna verdaeira se o pássaro já foi lançado e falso caso contrário

        :return: booleano
        """
        return not self._tempo_de_lancamento is None

    def colidir_com_chao(self):
        """
        Método que executa lógica de colisão com o chão. Toda vez que y for menor ou igual a 0,
        o status dos Passaro deve ser alterado para destruido, bem como o seu caracter

        """
        if self.y <= 0:
            self.status = DESTRUIDO

    def calcular_posicao(self, tempo):
        """
        Método que cálcula a posição do passaro de acordo com o tempo.

        Antes do lançamento o pássaro deve retornar o valor de sua posição inicial

        Depois do lançamento o pássaro deve calcular de acordo com sua posição inicial, velocidade escalar,
        ângulo de lancamento, gravidade (constante GRAVIDADE) e o tempo do jogo.

        Após a colisão, ou seja, ter seus status destruido, o pássaro deve apenas retornar a última posição calculada.

        :param tempo: tempo de jogo a ser calculada a posição
        :return: posição x, y
        """
        if self._esta_voando():
            delta_t = tempo -self._tempo_de_lancamento
            self._calcular_posicao_vertical(delta_t)
            self._calcular_posicao_horizontal(delta_t)
        return super().calcular_posicao(tempo)


    def lancar(self, angulo, tempo_de_lancamento):
        """
        Lógica que lança o pássaro. Deve armazenar o ângulo e o tempo de lançamento para posteriores cálculo.
        O ângulo é passado em graus e deve ser transformado em radianos

        :param angulo:
        :param tempo_de_lancamento:
        :return:
        """
        self._angulo_de_lancamento = angulo
        self._tempo_de_lancamento = tempo_de_lancamento

    def _calcular_posicao_vertical(self, delta_t):
        y_atual = self._y_inicial
        angulo_radianos = math.radians(self._angulo_de_lancamento)
        y_atual += self.velocidade_escalar * delta_t * math.sin(angulo_radianos)
        y_atual -= (GRAVIDADE * (delta_t ** 2)) / 2
        self.y = y_atual

    def _calcular_posicao_horizontal(self, delta_t):
        x_atual = self._x_inicial
        angulo_radianos = math.radians(self._angulo_de_lancamento)
        x_atual += self.velocidade_escalar * delta_t * math.cos(angulo_radianos)
        self.x = x_atual

    def _esta_voando(self):
        return self.foi_lancado() and self.status == ATIVO


class PassaroAmarelo(Passaro):
    _caracter_ativo = 'A'
    _caracter_destruido = 'a'
    velocidade_escalar = 30


class PassaroVermelho(Passaro):
    _caracter_ativo = 'V'
    _caracter_destruido = 'v'
    velocidade_escalar = 20

class ObstaculoTeste(TestCase):

    def teste_status(self):
        obstaculo = Obstaculo()
        self.assertEqual( 'O', obstaculo.caracter())
        outro_ator_na_mesma_posicao = Ator()
        obstaculo.colidir(outro_ator_na_mesma_posicao)
        self.assertEqual(' ', obstaculo.caracter())

class PorcoTestes(TestCase):

    def teste_status(self):
        porco = Porco()
        self.assertEqual('@', porco.caracter())
        outro_ator_na_mesma_posicao = Ator()
        porco.colidir(outro_ator_na_mesma_posicao)
        self.assertEqual('+', porco.caracter())

class PassaroBaseTests(TestCase):
    '''
    Classe base para teste de passaros.
    Essa classe não contém nenhum teste, serve apenas para encapsular a lógica de asserção
    dos vermelhos e também dos amarelos.
    '''

    def assert_passaro_posicao(self, x_esperado, y_esperado, status_esperado, passaro, tempo):
        '''
        Método que se testa posição do pássaro.
        Atenção: Esse não é um método de teste porque não se inicia com prefixo "Test".
        :param x_esperado: posição x esperada do passaro
        :param y_esperado: posição y esperada do passaro
        :param status_esperado: status esperado do passaro
        :param passaro: passaro alvo do teste
        :param tempo: tempo do jogo
        '''
        x_calculado, y_calculado = passaro.calcular_posicao(tempo)
        self.assertEqual(x_esperado, round(x_calculado),'valor real de x=%s' % x_calculado)
        self.assertEqual(y_esperado, round(y_calculado),'valor real de x=%s' % y_calculado)
        self.assertEqual(status_esperado, passaro.status),'(x = %s, y = %s)' % (x_calculado, y_calculado)

class PassaroVermelhoTests(PassaroBaseTests):
    '''
    Classe de teste e Passaro Vermelho
    '''

    def teste_status(self):
        passaro_vermelho = PassaroVermelho(1, 1)
        self.assertEqual('V', passaro_vermelho.caracter())
        outro_ator_na_mesma_posicao = Ator()
        passaro_vermelho.colidir(outro_ator_na_mesma_posicao)
        self.assertEqual('v', passaro_vermelho.caracter())

    def teste_velocidade_escala(self):
        self.assertEqual(20, PassaroVermelho.velocidade_escalar)

    def teste_foi_lancado(self):
        '''
        Teste de lançamento. Enquanto o método lançar do passaro não for chamado, o método
        for False
        return:
        '''
        passaro_vermelho = PassaroVermelho(1, 1)
        self.assertFalse(passaro_vermelho.foi_lançado(),
                         'Se o método lançar ainda não foi executado, deve retornar falso')
        passaro_vermelho.lancar(0, 0)
        self.assertTrue(passaro_vermelho.foi_lancado(),
                        'Se o método lançar foi executado, deve retornar verdadeiro')

    def teste_colisao_com_chao(self):
        '''
        Testando que o passáro colide quando sua posição y e menor ou igual a 0
        return:
        '''
        passaro = PassaroVermelho(0, 0)
        passaro.colidir_com_chao()
        self.assertEqual(DESTRUIDO, passaro.status, 'Deve colidir com o chão sempre que y <= 0')
        passaro = PassaroVermelho(1, 0)
        passaro.colidir_com_chao()
        self.assertEqual(DESTRUIDO, passaro.status, 'Deve colidir com chão sempre que y<= 2')
        passaro.colidir_com_chao()
        self.assertEqual(DESTRUIDO, passaro.status, 'Deve colidir com chão sempre que y<= 2')
        passaro = PassaroVermelho(2, -0.1)
        passaro.colidir_com_chao()
        self.assertEqual(DESTRUIDO, passaro.status, 'Deve colidir com chão sempre que y<= 2')
        passaro = PassaroVermelho(2, -5)
        passaro.colidir_com_chao()
        self.assertEqual(DESTRUIDO, passaro.status, 'Deve colidir com chão sempre que y<= 2')

class PassaroAmareloTests(PassaroBaseTests):
    '''
    Classe de tests para passaros amarelo
    '''

    def teste_status(self):
        passaro_amarelo = PassaroAmarelo(1, 1)
        self.assertEqual('A', passaro_amarelo.caracter())
        outro_ator_na_mesma_posicao = Ator()
        passaro_amarelo.colidir(outro_ator_na_mesma_posicao)
        self.assertEqual('a', passaro_amarelo.caracter())

    def teste_velocidade_escalar(self):
        self.assertEqual(30, PassaroAmarelo.velocidade_escalar)

    def teste_lancamento_vertical(self):
        '''
        tests de lançamento vertical. Nele, o passaro só se move verticalmente e sua posição
        '''
        passaro_amarelo = PassaroAmarelo(1, 1)
        passaro_amarelo.lancar(90, 2) # passaro lancado a 90 graus no tempo 2 segundos

        #subindo

        self.assert_posicao_vertical(1, 2.0, passaro_amarelo)
        self.assert_posicao_vertical(1, 2.1, passaro_amarelo)
        self.assert_posicao_vertical(2, 2.2, passaro_amarelo)
        self.assert_posicao_vertical(2, 2.3, passaro_amarelo)
        self.assert_posicao_vertical(2, 2.4, passaro_amarelo)
        self.assert_posicao_vertical(2, 2.5, passaro_amarelo)

        #descendo

        self.assert_posicao_vertical(46, 5.26, passaro_amarelo)
        self.assert_posicao_vertical(46, 5.27, passaro_amarelo)
        self.assert_posicao_vertical(46, 5.279999999999999, passaro_amarelo)
        self.assert_posicao_vertical(46, 5.29, passaro_amarelo)
        self.assert_posicao_vertical(46, 5.3, passaro_amarelo)
        self.assert_posicao_vertical(46, 5.3100000000000005, passaro_amarelo)
        self.assert_posicao_vertical(45, 5.32, passaro_amarelo)
        self.assert_posicao_vertical(45, 5.33, passaro_amarelo)
        self.assert_posicao_vertical(45, 5.34, passaro_amarelo)
        self.assert_posicao_vertical(45, 5.359999999999999, passaro_amarelo)
        self.assert_posicao_vertical(45, 5.37, passaro_amarelo)
        self.assert_posicao_vertical(45, 5.38, passaro_amarelo)
        self.assert_posicao_vertical(45, 5.3900000000000001, passaro_amarelo)
        self.assert_posicao_vertical(45, 5.4, passaro_amarelo)
        self.assert_posicao_vertical(45, 5.41, passaro_amarelo)
        self.assert_posicao_vertical(45, 5.42, passaro_amarelo)
        self.assert_posicao_vertical(45, 5.43, passaro_amarelo)
        self.assert_posicao_vertical(45, 5.43999999999999995, passaro_amarelo)
        self.assert_posicao_vertical(45, 5.45, passaro_amarelo)
        self.assert_posicao_vertical(45, 5.46, passaro_amarelo)
        self.assert_posicao_vertical(45, 5.4700000000000001, passaro_amarelo)
        self.assert_posicao_vertical(45, 5.48, passaro_amarelo)

        #preparando para impacto no chão
        self.assert_posicao_vertical(1, 8.0, passaro_amarelo)
        self.assert_posicao_vertical(1, 8.01, passaro_amarelo)

        #colisão
        self.assert_posicao_vertical(0, 8.04, passaro_amarelo)
        passaro_amarelo.colidir_com_chao()
        self.assertEqual(DESTRUIDO, passaro_amarelo.status)

        def test_lancamento_45_graus(self):
            passaro_amarelo = PassaroAmarelo(1, 1)
            passaro_amarelo.lancar(45, 2)  # passaro lancado a 45 graus no tempo 2 segundos
            self.assert_passaro_posicao(1, 1, ATIVO, passaro_amarelo, 2.0)
            self.assert_passaro_posicao(1, 1, ATIVO, passaro_amarelo, 2.01)
            self.assert_passaro_posicao(1, 1, ATIVO, passaro_amarelo, 2.02)
            self.assert_passaro_posicao(2, 2, ATIVO, passaro_amarelo, 2.03)
            self.assert_passaro_posicao(2, 2, ATIVO, passaro_amarelo, 2.04)
            self.assert_passaro_posicao(2, 2, ATIVO, passaro_amarelo, 2.05)
            self.assert_passaro_posicao(2, 2, ATIVO, passaro_amarelo, 2.06)
            self.assert_passaro_posicao(2, 2, ATIVO, passaro_amarelo, 2.07)
            self.assert_passaro_posicao(3, 3, ATIVO, passaro_amarelo, 2.08)
            self.assert_passaro_posicao(3, 3, ATIVO, passaro_amarelo, 2.09)
            self.assert_passaro_posicao(3, 3, ATIVO, passaro_amarelo, 2.1)
            self.assert_passaro_posicao(3, 3, ATIVO, passaro_amarelo, 2.11)
            self.assert_passaro_posicao(4, 3, ATIVO, passaro_amarelo, 2.12)
            self.assert_passaro_posicao(4, 4, ATIVO, passaro_amarelo, 2.13)
            self.assert_passaro_posicao(4, 4, ATIVO, passaro_amarelo, 2.14)
            self.assert_passaro_posicao(4, 4, ATIVO, passaro_amarelo, 2.15)
            self.assert_passaro_posicao(4, 4, ATIVO, passaro_amarelo, 2.16)
            self.assert_passaro_posicao(5, 4, ATIVO, passaro_amarelo, 2.17)
            self.assert_passaro_posicao(5, 5, ATIVO, passaro_amarelo, 2.18)
            self.assert_passaro_posicao(5, 5, ATIVO, passaro_amarelo, 2.19)
            self.assert_passaro_posicao(5, 5, ATIVO, passaro_amarelo, 2.2)
            self.assert_passaro_posicao(5, 5, ATIVO, passaro_amarelo, 2.21)
            self.assert_passaro_posicao(6, 5, ATIVO, passaro_amarelo, 2.22)
            self.assert_passaro_posicao(6, 6, ATIVO, passaro_amarelo, 2.23)
            self.assert_passaro_posicao(6, 6, ATIVO, passaro_amarelo, 2.24)
            self.assert_passaro_posicao(6, 6, ATIVO, passaro_amarelo, 2.25)
            self.assert_passaro_posicao(7, 6, ATIVO, passaro_amarelo, 2.26)
            self.assert_passaro_posicao(7, 6, ATIVO, passaro_amarelo, 2.27)
            self.assert_passaro_posicao(7, 7, ATIVO, passaro_amarelo, 2.2800000000000002)
            self.assert_passaro_posicao(7, 7, ATIVO, passaro_amarelo, 2.29)
            self.assert_passaro_posicao(7, 7, ATIVO, passaro_amarelo, 2.3)
            self.assert_passaro_posicao(8, 7, ATIVO, passaro_amarelo, 2.31)
            self.assert_passaro_posicao(8, 7, ATIVO, passaro_amarelo, 2.32)
            self.assert_passaro_posicao(8, 7, ATIVO, passaro_amarelo, 2.33)
            self.assert_passaro_posicao(8, 8, ATIVO, passaro_amarelo, 2.34)
            self.assert_passaro_posicao(8, 8, ATIVO, passaro_amarelo, 2.35)
            self.assert_passaro_posicao(9, 8, ATIVO, passaro_amarelo, 2.36)
            self.assert_passaro_posicao(9, 8, ATIVO, passaro_amarelo, 2.37)
            self.assert_passaro_posicao(9, 8, ATIVO, passaro_amarelo, 2.38)
            self.assert_passaro_posicao(9, 9, ATIVO, passaro_amarelo, 2.39)
            self.assert_passaro_posicao(9, 9, ATIVO, passaro_amarelo, 2.4)
            self.assert_passaro_posicao(10, 9, ATIVO, passaro_amarelo, 2.41)
            self.assert_passaro_posicao(10, 9, ATIVO, passaro_amarelo, 2.42)
            self.assert_passaro_posicao(10, 9, ATIVO, passaro_amarelo, 2.43)
            self.assert_passaro_posicao(10, 9, ATIVO, passaro_amarelo, 2.44)
            self.assert_passaro_posicao(11, 10, ATIVO, passaro_amarelo, 2.45)
            self.assert_passaro_posicao(11, 10, ATIVO, passaro_amarelo, 2.46)
            self.assert_passaro_posicao(11, 10, ATIVO, passaro_amarelo, 2.4699999999999998)
            self.assert_passaro_posicao(11, 10, ATIVO, passaro_amarelo, 2.48)
            self.assert_passaro_posicao(11, 10, ATIVO, passaro_amarelo, 2.49)
            self.assert_passaro_posicao(12, 10, ATIVO, passaro_amarelo, 2.5)
            self.assert_passaro_posicao(12, 11, ATIVO, passaro_amarelo, 2.51)
            self.assert_passaro_posicao(12, 11, ATIVO, passaro_amarelo, 2.52)
            self.assert_passaro_posicao(12, 11, ATIVO, passaro_amarelo, 2.5300000000000002)
            self.assert_passaro_posicao(12, 11, ATIVO, passaro_amarelo, 2.54)
            self.assert_passaro_posicao(13, 11, ATIVO, passaro_amarelo, 2.55)
            self.assert_passaro_posicao(13, 11, ATIVO, passaro_amarelo, 2.56)
            self.assert_passaro_posicao(13, 11, ATIVO, passaro_amarelo, 2.57)
            self.assert_passaro_posicao(13, 12, ATIVO, passaro_amarelo, 2.58)
            self.assert_passaro_posicao(14, 12, ATIVO, passaro_amarelo, 2.59)
            self.assert_passaro_posicao(14, 12, ATIVO, passaro_amarelo, 2.6)
            self.assert_passaro_posicao(14, 12, ATIVO, passaro_amarelo, 2.61)
            self.assert_passaro_posicao(14, 12, ATIVO, passaro_amarelo, 2.62)
            self.assert_passaro_posicao(14, 12, ATIVO, passaro_amarelo, 2.63)
            self.assert_passaro_posicao(15, 13, ATIVO, passaro_amarelo, 2.64)
            self.assert_passaro_posicao(15, 13, ATIVO, passaro_amarelo, 2.65)
            self.assert_passaro_posicao(15, 13, ATIVO, passaro_amarelo, 2.66)
            self.assert_passaro_posicao(15, 13, ATIVO, passaro_amarelo, 2.67)
            self.assert_passaro_posicao(15, 13, ATIVO, passaro_amarelo, 2.68)
            self.assert_passaro_posicao(16, 13, ATIVO, passaro_amarelo, 2.69)
            self.assert_passaro_posicao(16, 13, ATIVO, passaro_amarelo, 2.7)
            self.assert_passaro_posicao(16, 14, ATIVO, passaro_amarelo, 2.71)
            self.assert_passaro_posicao(16, 14, ATIVO, passaro_amarelo, 2.7199999999999998)
            self.assert_passaro_posicao(16, 14, ATIVO, passaro_amarelo, 2.73)
            self.assert_passaro_posicao(17, 14, ATIVO, passaro_amarelo, 2.74)
            self.assert_passaro_posicao(17, 14, ATIVO, passaro_amarelo, 2.75)
            self.assert_passaro_posicao(17, 14, ATIVO, passaro_amarelo, 2.76)
            self.assert_passaro_posicao(17, 14, ATIVO, passaro_amarelo, 2.77)
            self.assert_passaro_posicao(18, 15, ATIVO, passaro_amarelo, 2.7800000000000002)
            self.assert_passaro_posicao(18, 15, ATIVO, passaro_amarelo, 2.79)
            self.assert_passaro_posicao(18, 15, ATIVO, passaro_amarelo, 2.8)
            self.assert_passaro_posicao(18, 15, ATIVO, passaro_amarelo, 2.81)
            self.assert_passaro_posicao(18, 15, ATIVO, passaro_amarelo, 2.82)
            self.assert_passaro_posicao(19, 15, ATIVO, passaro_amarelo, 2.83)
            self.assert_passaro_posicao(19, 15, ATIVO, passaro_amarelo, 2.84)
            self.assert_passaro_posicao(19, 15, ATIVO, passaro_amarelo, 2.85)
            self.assert_passaro_posicao(19, 16, ATIVO, passaro_amarelo, 2.86)
            self.assert_passaro_posicao(19, 16, ATIVO, passaro_amarelo, 2.87)
            self.assert_passaro_posicao(20, 16, ATIVO, passaro_amarelo, 2.88)
            self.assert_passaro_posicao(20, 16, ATIVO, passaro_amarelo, 2.89)
            self.assert_passaro_posicao(20, 16, ATIVO, passaro_amarelo, 2.9)
            self.assert_passaro_posicao(20, 16, ATIVO, passaro_amarelo, 2.91)
            self.assert_passaro_posicao(21, 16, ATIVO, passaro_amarelo, 2.92)
            self.assert_passaro_posicao(21, 16, ATIVO, passaro_amarelo, 2.93)
            self.assert_passaro_posicao(21, 17, ATIVO, passaro_amarelo, 2.94)
            self.assert_passaro_posicao(21, 17, ATIVO, passaro_amarelo, 2.95)
            self.assert_passaro_posicao(21, 17, ATIVO, passaro_amarelo, 2.96)
            self.assert_passaro_posicao(22, 17, ATIVO, passaro_amarelo, 2.9699999999999998)
            self.assert_passaro_posicao(22, 17, ATIVO, passaro_amarelo, 2.98)
            self.assert_passaro_posicao(22, 17, ATIVO, passaro_amarelo, 2.99)
            self.assert_passaro_posicao(22, 17, ATIVO, passaro_amarelo, 3.0)
            self.assert_passaro_posicao(22, 17, ATIVO, passaro_amarelo, 3.01)
            self.assert_passaro_posicao(23, 17, ATIVO, passaro_amarelo, 3.02)
            self.assert_passaro_posicao(23, 18, ATIVO, passaro_amarelo, 3.0300000000000002)
            self.assert_passaro_posicao(23, 18, ATIVO, passaro_amarelo, 3.04)
            self.assert_passaro_posicao(23, 18, ATIVO, passaro_amarelo, 3.05)
            self.assert_passaro_posicao(23, 18, ATIVO, passaro_amarelo, 3.06)
            self.assert_passaro_posicao(24, 18, ATIVO, passaro_amarelo, 3.0700000000000003)
            self.assert_passaro_posicao(24, 18, ATIVO, passaro_amarelo, 3.08)
            self.assert_passaro_posicao(24, 18, ATIVO, passaro_amarelo, 3.09)
            self.assert_passaro_posicao(24, 18, ATIVO, passaro_amarelo, 3.1)
            self.assert_passaro_posicao(25, 18, ATIVO, passaro_amarelo, 3.1100000000000003)
            self.assert_passaro_posicao(25, 18, ATIVO, passaro_amarelo, 3.12)
            self.assert_passaro_posicao(25, 19, ATIVO, passaro_amarelo, 3.13)
            self.assert_passaro_posicao(25, 19, ATIVO, passaro_amarelo, 3.1399999999999997)
            self.assert_passaro_posicao(25, 19, ATIVO, passaro_amarelo, 3.15)
            self.assert_passaro_posicao(26, 19, ATIVO, passaro_amarelo, 3.16)
            self.assert_passaro_posicao(26, 19, ATIVO, passaro_amarelo, 3.17)
            self.assert_passaro_posicao(26, 19, ATIVO, passaro_amarelo, 3.1799999999999997)
            self.assert_passaro_posicao(26, 19, ATIVO, passaro_amarelo, 3.19)
            self.assert_passaro_posicao(26, 19, ATIVO, passaro_amarelo, 3.2)
            self.assert_passaro_posicao(27, 19, ATIVO, passaro_amarelo, 3.21)
            self.assert_passaro_posicao(27, 19, ATIVO, passaro_amarelo, 3.2199999999999998)
            self.assert_passaro_posicao(27, 20, ATIVO, passaro_amarelo, 3.23)
            self.assert_passaro_posicao(27, 20, ATIVO, passaro_amarelo, 3.24)
            self.assert_passaro_posicao(28, 20, ATIVO, passaro_amarelo, 3.25)
            self.assert_passaro_posicao(28, 20, ATIVO, passaro_amarelo, 3.26)
            self.assert_passaro_posicao(28, 20, ATIVO, passaro_amarelo, 3.27)
            self.assert_passaro_posicao(28, 20, ATIVO, passaro_amarelo, 3.2800000000000002)
            self.assert_passaro_posicao(28, 20, ATIVO, passaro_amarelo, 3.29)
            self.assert_passaro_posicao(29, 20, ATIVO, passaro_amarelo, 3.3)
            self.assert_passaro_posicao(29, 20, ATIVO, passaro_amarelo, 3.31)
            self.assert_passaro_posicao(29, 20, ATIVO, passaro_amarelo, 3.3200000000000003)
            self.assert_passaro_posicao(29, 20, ATIVO, passaro_amarelo, 3.33)
            self.assert_passaro_posicao(29, 20, ATIVO, passaro_amarelo, 3.34)
            self.assert_passaro_posicao(30, 21, ATIVO, passaro_amarelo, 3.35)
            self.assert_passaro_posicao(30, 21, ATIVO, passaro_amarelo, 3.3600000000000003)
            self.assert_passaro_posicao(30, 21, ATIVO, passaro_amarelo, 3.37)
            self.assert_passaro_posicao(30, 21, ATIVO, passaro_amarelo, 3.38)
            self.assert_passaro_posicao(30, 21, ATIVO, passaro_amarelo, 3.3899999999999997)
            self.assert_passaro_posicao(31, 21, ATIVO, passaro_amarelo, 3.4)
            self.assert_passaro_posicao(31, 21, ATIVO, passaro_amarelo, 3.41)
            self.assert_passaro_posicao(31, 21, ATIVO, passaro_amarelo, 3.42)
            self.assert_passaro_posicao(31, 21, ATIVO, passaro_amarelo, 3.4299999999999997)
            self.assert_passaro_posicao(32, 21, ATIVO, passaro_amarelo, 3.44)
            self.assert_passaro_posicao(32, 21, ATIVO, passaro_amarelo, 3.45)
            self.assert_passaro_posicao(32, 21, ATIVO, passaro_amarelo, 3.46)
            self.assert_passaro_posicao(32, 21, ATIVO, passaro_amarelo, 3.4699999999999998)
            self.assert_passaro_posicao(32, 21, ATIVO, passaro_amarelo, 3.48)
            self.assert_passaro_posicao(33, 22, ATIVO, passaro_amarelo, 3.49)
            self.assert_passaro_posicao(33, 22, ATIVO, passaro_amarelo, 3.5)
            self.assert_passaro_posicao(33, 22, ATIVO, passaro_amarelo, 3.51)
            self.assert_passaro_posicao(33, 22, ATIVO, passaro_amarelo, 3.52)
            self.assert_passaro_posicao(33, 22, ATIVO, passaro_amarelo, 3.5300000000000002)
            self.assert_passaro_posicao(34, 22, ATIVO, passaro_amarelo, 3.54)
            self.assert_passaro_posicao(34, 22, ATIVO, passaro_amarelo, 3.55)
            self.assert_passaro_posicao(34, 22, ATIVO, passaro_amarelo, 3.56)
            self.assert_passaro_posicao(34, 22, ATIVO, passaro_amarelo, 3.5700000000000003)
            self.assert_passaro_posicao(35, 22, ATIVO, passaro_amarelo, 3.58)
            self.assert_passaro_posicao(35, 22, ATIVO, passaro_amarelo, 3.59)
            self.assert_passaro_posicao(35, 22, ATIVO, passaro_amarelo, 3.6)
            self.assert_passaro_posicao(35, 22, ATIVO, passaro_amarelo, 3.6100000000000003)
            self.assert_passaro_posicao(35, 22, ATIVO, passaro_amarelo, 3.62)
            self.assert_passaro_posicao(36, 22, ATIVO, passaro_amarelo, 3.63)
            self.assert_passaro_posicao(36, 22, ATIVO, passaro_amarelo, 3.6399999999999997)
            self.assert_passaro_posicao(36, 22, ATIVO, passaro_amarelo, 3.65)
            self.assert_passaro_posicao(36, 22, ATIVO, passaro_amarelo, 3.66)
            self.assert_passaro_posicao(36, 22, ATIVO, passaro_amarelo, 3.67)
            self.assert_passaro_posicao(37, 23, ATIVO, passaro_amarelo, 3.6799999999999997)
            self.assert_passaro_posicao(37, 23, ATIVO, passaro_amarelo, 3.69)
            self.assert_passaro_posicao(37, 23, ATIVO, passaro_amarelo, 3.7)
            self.assert_passaro_posicao(37, 23, ATIVO, passaro_amarelo, 3.71)
            self.assert_passaro_posicao(37, 23, ATIVO, passaro_amarelo, 3.7199999999999998)
            self.assert_passaro_posicao(38, 23, ATIVO, passaro_amarelo, 3.73)
            self.assert_passaro_posicao(38, 23, ATIVO, passaro_amarelo, 3.74)
            self.assert_passaro_posicao(38, 23, ATIVO, passaro_amarelo, 3.75)
            self.assert_passaro_posicao(38, 23, ATIVO, passaro_amarelo, 3.76)
            self.assert_passaro_posicao(39, 23, ATIVO, passaro_amarelo, 3.77)
            self.assert_passaro_posicao(39, 23, ATIVO, passaro_amarelo, 3.7800000000000002)
            self.assert_passaro_posicao(39, 23, ATIVO, passaro_amarelo, 3.79)
            self.assert_passaro_posicao(39, 23, ATIVO, passaro_amarelo, 3.8)
            self.assert_passaro_posicao(39, 23, ATIVO, passaro_amarelo, 3.81)
            self.assert_passaro_posicao(40, 23, ATIVO, passaro_amarelo, 3.8200000000000003)
            self.assert_passaro_posicao(40, 23, ATIVO, passaro_amarelo, 3.83)
            self.assert_passaro_posicao(40, 23, ATIVO, passaro_amarelo, 3.84)
            self.assert_passaro_posicao(40, 23, ATIVO, passaro_amarelo, 3.85)
            self.assert_passaro_posicao(40, 23, ATIVO, passaro_amarelo, 3.8600000000000003)
            self.assert_passaro_posicao(41, 23, ATIVO, passaro_amarelo, 3.87)
            self.assert_passaro_posicao(41, 23, ATIVO, passaro_amarelo, 3.88)
            self.assert_passaro_posicao(41, 23, ATIVO, passaro_amarelo, 3.8899999999999997)
            self.assert_passaro_posicao(41, 23, ATIVO, passaro_amarelo, 3.9)
            self.assert_passaro_posicao(42, 23, ATIVO, passaro_amarelo, 3.91)
            self.assert_passaro_posicao(42, 23, ATIVO, passaro_amarelo, 3.92)
            self.assert_passaro_posicao(42, 23, ATIVO, passaro_amarelo, 3.9299999999999997)
            self.assert_passaro_posicao(42, 23, ATIVO, passaro_amarelo, 3.94)
            self.assert_passaro_posicao(42, 23, ATIVO, passaro_amarelo, 3.95)
            self.assert_passaro_posicao(43, 23, ATIVO, passaro_amarelo, 3.96)
            self.assert_passaro_posicao(43, 23, ATIVO, passaro_amarelo, 3.9699999999999998)
            self.assert_passaro_posicao(43, 23, ATIVO, passaro_amarelo, 3.98)
            self.assert_passaro_posicao(43, 23, ATIVO, passaro_amarelo, 3.99)
            self.assert_passaro_posicao(43, 23, ATIVO, passaro_amarelo, 4.0)
            self.assert_passaro_posicao(44, 23, ATIVO, passaro_amarelo, 4.01)
            self.assert_passaro_posicao(44, 23, ATIVO, passaro_amarelo, 4.02)
            self.assert_passaro_posicao(44, 23, ATIVO, passaro_amarelo, 4.029999999999999)
            self.assert_passaro_posicao(44, 23, ATIVO, passaro_amarelo, 4.04)
            self.assert_passaro_posicao(44, 23, ATIVO, passaro_amarelo, 4.05)
            self.assert_passaro_posicao(45, 23, ATIVO, passaro_amarelo, 4.0600000000000005)
            self.assert_passaro_posicao(45, 23, ATIVO, passaro_amarelo, 4.07)
            self.assert_passaro_posicao(45, 23, ATIVO, passaro_amarelo, 4.08)
            self.assert_passaro_posicao(45, 23, ATIVO, passaro_amarelo, 4.09)
            self.assert_passaro_posicao(46, 23, ATIVO, passaro_amarelo, 4.1)
            self.assert_passaro_posicao(46, 23, ATIVO, passaro_amarelo, 4.109999999999999)
            self.assert_passaro_posicao(46, 23, ATIVO, passaro_amarelo, 4.12)
            self.assert_passaro_posicao(46, 23, ATIVO, passaro_amarelo, 4.13)
            self.assert_passaro_posicao(46, 23, ATIVO, passaro_amarelo, 4.140000000000001)
            self.assert_passaro_posicao(47, 23, ATIVO, passaro_amarelo, 4.15)
            self.assert_passaro_posicao(47, 23, ATIVO, passaro_amarelo, 4.16)
            self.assert_passaro_posicao(47, 23, ATIVO, passaro_amarelo, 4.17)
            self.assert_passaro_posicao(47, 23, ATIVO, passaro_amarelo, 4.18)
            self.assert_passaro_posicao(47, 23, ATIVO, passaro_amarelo, 4.1899999999999995)
            self.assert_passaro_posicao(48, 23, ATIVO, passaro_amarelo, 4.2)
            self.assert_passaro_posicao(48, 23, ATIVO, passaro_amarelo, 4.21)
            self.assert_passaro_posicao(48, 23, ATIVO, passaro_amarelo, 4.220000000000001)
            self.assert_passaro_posicao(48, 23, ATIVO, passaro_amarelo, 4.23)
            self.assert_passaro_posicao(49, 23, ATIVO, passaro_amarelo, 4.24)
            self.assert_passaro_posicao(49, 23, ATIVO, passaro_amarelo, 4.25)
            self.assert_passaro_posicao(49, 23, ATIVO, passaro_amarelo, 4.26)
            self.assert_passaro_posicao(49, 23, ATIVO, passaro_amarelo, 4.27)
            self.assert_passaro_posicao(49, 23, ATIVO, passaro_amarelo, 4.279999999999999)
            self.assert_passaro_posicao(50, 23, ATIVO, passaro_amarelo, 4.29)
            self.assert_passaro_posicao(50, 23, ATIVO, passaro_amarelo, 4.3)
            self.assert_passaro_posicao(50, 23, ATIVO, passaro_amarelo, 4.3100000000000005)
            self.assert_passaro_posicao(50, 23, ATIVO, passaro_amarelo, 4.32)
            self.assert_passaro_posicao(50, 23, ATIVO, passaro_amarelo, 4.33)
            self.assert_passaro_posicao(51, 23, ATIVO, passaro_amarelo, 4.34)
            self.assert_passaro_posicao(51, 23, ATIVO, passaro_amarelo, 4.35)
            self.assert_passaro_posicao(51, 23, ATIVO, passaro_amarelo, 4.359999999999999)
            self.assert_passaro_posicao(51, 23, ATIVO, passaro_amarelo, 4.37)
            self.assert_passaro_posicao(51, 23, ATIVO, passaro_amarelo, 4.38)
            self.assert_passaro_posicao(52, 23, ATIVO, passaro_amarelo, 4.390000000000001)
            self.assert_passaro_posicao(52, 23, ATIVO, passaro_amarelo, 4.4)
            self.assert_passaro_posicao(52, 23, ATIVO, passaro_amarelo, 4.41)
            self.assert_passaro_posicao(52, 23, ATIVO, passaro_amarelo, 4.42)
            self.assert_passaro_posicao(53, 23, ATIVO, passaro_amarelo, 4.43)
            self.assert_passaro_posicao(53, 23, ATIVO, passaro_amarelo, 4.4399999999999995)
            self.assert_passaro_posicao(53, 23, ATIVO, passaro_amarelo, 4.45)
            self.assert_passaro_posicao(53, 23, ATIVO, passaro_amarelo, 4.46)
            self.assert_passaro_posicao(53, 23, ATIVO, passaro_amarelo, 4.470000000000001)
            self.assert_passaro_posicao(54, 23, ATIVO, passaro_amarelo, 4.48)
            self.assert_passaro_posicao(54, 23, ATIVO, passaro_amarelo, 4.49)
            self.assert_passaro_posicao(54, 23, ATIVO, passaro_amarelo, 4.5)
            self.assert_passaro_posicao(54, 23, ATIVO, passaro_amarelo, 4.51)
            self.assert_passaro_posicao(54, 23, ATIVO, passaro_amarelo, 4.52)
            self.assert_passaro_posicao(55, 23, ATIVO, passaro_amarelo, 4.529999999999999)
            self.assert_passaro_posicao(55, 23, ATIVO, passaro_amarelo, 4.54)
            self.assert_passaro_posicao(55, 23, ATIVO, passaro_amarelo, 4.55)
            self.assert_passaro_posicao(55, 23, ATIVO, passaro_amarelo, 4.5600000000000005)
            self.assert_passaro_posicao(56, 22, ATIVO, passaro_amarelo, 4.57)
            self.assert_passaro_posicao(56, 22, ATIVO, passaro_amarelo, 4.58)
            self.assert_passaro_posicao(56, 22, ATIVO, passaro_amarelo, 4.59)
            self.assert_passaro_posicao(56, 22, ATIVO, passaro_amarelo, 4.6)
            self.assert_passaro_posicao(56, 22, ATIVO, passaro_amarelo, 4.609999999999999)
            self.assert_passaro_posicao(57, 22, ATIVO, passaro_amarelo, 4.62)
            self.assert_passaro_posicao(57, 22, ATIVO, passaro_amarelo, 4.63)
            self.assert_passaro_posicao(57, 22, ATIVO, passaro_amarelo, 4.640000000000001)
            self.assert_passaro_posicao(57, 22, ATIVO, passaro_amarelo, 4.65)
            self.assert_passaro_posicao(57, 22, ATIVO, passaro_amarelo, 4.66)
            self.assert_passaro_posicao(58, 22, ATIVO, passaro_amarelo, 4.67)
            self.assert_passaro_posicao(58, 22, ATIVO, passaro_amarelo, 4.68)
            self.assert_passaro_posicao(58, 22, ATIVO, passaro_amarelo, 4.6899999999999995)
            self.assert_passaro_posicao(58, 22, ATIVO, passaro_amarelo, 4.7)
            self.assert_passaro_posicao(58, 22, ATIVO, passaro_amarelo, 4.71)
            self.assert_passaro_posicao(59, 22, ATIVO, passaro_amarelo, 4.720000000000001)
            self.assert_passaro_posicao(59, 22, ATIVO, passaro_amarelo, 4.73)
            self.assert_passaro_posicao(59, 22, ATIVO, passaro_amarelo, 4.74)
            self.assert_passaro_posicao(59, 22, ATIVO, passaro_amarelo, 4.75)
            self.assert_passaro_posicao(60, 21, ATIVO, passaro_amarelo, 4.76)
            self.assert_passaro_posicao(60, 21, ATIVO, passaro_amarelo, 4.77)
            self.assert_passaro_posicao(60, 21, ATIVO, passaro_amarelo, 4.779999999999999)
            self.assert_passaro_posicao(60, 21, ATIVO, passaro_amarelo, 4.79)
            self.assert_passaro_posicao(60, 21, ATIVO, passaro_amarelo, 4.8)
            self.assert_passaro_posicao(61, 21, ATIVO, passaro_amarelo, 4.8100000000000005)
            self.assert_passaro_posicao(61, 21, ATIVO, passaro_amarelo, 4.82)
            self.assert_passaro_posicao(61, 21, ATIVO, passaro_amarelo, 4.83)
            self.assert_passaro_posicao(61, 21, ATIVO, passaro_amarelo, 4.84)
            self.assert_passaro_posicao(61, 21, ATIVO, passaro_amarelo, 4.85)
            self.assert_passaro_posicao(62, 21, ATIVO, passaro_amarelo, 4.859999999999999)
            self.assert_passaro_posicao(62, 21, ATIVO, passaro_amarelo, 4.87)
            self.assert_passaro_posicao(62, 21, ATIVO, passaro_amarelo, 4.88)
            self.assert_passaro_posicao(62, 21, ATIVO, passaro_amarelo, 4.890000000000001)
            self.assert_passaro_posicao(63, 20, ATIVO, passaro_amarelo, 4.9)
            self.assert_passaro_posicao(63, 20, ATIVO, passaro_amarelo, 4.91)
            self.assert_passaro_posicao(63, 20, ATIVO, passaro_amarelo, 4.92)
            self.assert_passaro_posicao(63, 20, ATIVO, passaro_amarelo, 4.93)
            self.assert_passaro_posicao(63, 20, ATIVO, passaro_amarelo, 4.9399999999999995)
            self.assert_passaro_posicao(64, 20, ATIVO, passaro_amarelo, 4.95)
            self.assert_passaro_posicao(64, 20, ATIVO, passaro_amarelo, 4.96)
            self.assert_passaro_posicao(64, 20, ATIVO, passaro_amarelo, 4.970000000000001)
            self.assert_passaro_posicao(64, 20, ATIVO, passaro_amarelo, 4.98)
            self.assert_passaro_posicao(64, 20, ATIVO, passaro_amarelo, 4.99)
            self.assert_passaro_posicao(65, 20, ATIVO, passaro_amarelo, 5.0)
            self.assert_passaro_posicao(65, 20, ATIVO, passaro_amarelo, 5.01)
            self.assert_passaro_posicao(65, 19, ATIVO, passaro_amarelo, 5.02)
            self.assert_passaro_posicao(65, 19, ATIVO, passaro_amarelo, 5.029999999999999)
            self.assert_passaro_posicao(65, 19, ATIVO, passaro_amarelo, 5.04)
            self.assert_passaro_posicao(66, 19, ATIVO, passaro_amarelo, 5.05)
            self.assert_passaro_posicao(66, 19, ATIVO, passaro_amarelo, 5.0600000000000005)
            self.assert_passaro_posicao(66, 19, ATIVO, passaro_amarelo, 5.07)
            self.assert_passaro_posicao(66, 19, ATIVO, passaro_amarelo, 5.08)
            self.assert_passaro_posicao(67, 19, ATIVO, passaro_amarelo, 5.09)
            self.assert_passaro_posicao(67, 19, ATIVO, passaro_amarelo, 5.1)
            self.assert_passaro_posicao(67, 19, ATIVO, passaro_amarelo, 5.109999999999999)
            self.assert_passaro_posicao(67, 19, ATIVO, passaro_amarelo, 5.12)
            self.assert_passaro_posicao(67, 18, ATIVO, passaro_amarelo, 5.13)
            self.assert_passaro_posicao(68, 18, ATIVO, passaro_amarelo, 5.140000000000001)
            self.assert_passaro_posicao(68, 18, ATIVO, passaro_amarelo, 5.15)
            self.assert_passaro_posicao(68, 18, ATIVO, passaro_amarelo, 5.16)
            self.assert_passaro_posicao(68, 18, ATIVO, passaro_amarelo, 5.17)
            self.assert_passaro_posicao(68, 18, ATIVO, passaro_amarelo, 5.18)
            self.assert_passaro_posicao(69, 18, ATIVO, passaro_amarelo, 5.1899999999999995)
            self.assert_passaro_posicao(69, 18, ATIVO, passaro_amarelo, 5.2)
            self.assert_passaro_posicao(69, 18, ATIVO, passaro_amarelo, 5.21)
            self.assert_passaro_posicao(69, 17, ATIVO, passaro_amarelo, 5.220000000000001)
            self.assert_passaro_posicao(70, 17, ATIVO, passaro_amarelo, 5.23)
            self.assert_passaro_posicao(70, 17, ATIVO, passaro_amarelo, 5.24)
            self.assert_passaro_posicao(70, 17, ATIVO, passaro_amarelo, 5.25)
            self.assert_passaro_posicao(70, 17, ATIVO, passaro_amarelo, 5.26)
            self.assert_passaro_posicao(70, 17, ATIVO, passaro_amarelo, 5.27)
            self.assert_passaro_posicao(71, 17, ATIVO, passaro_amarelo, 5.279999999999999)
            self.assert_passaro_posicao(71, 17, ATIVO, passaro_amarelo, 5.29)
            self.assert_passaro_posicao(71, 17, ATIVO, passaro_amarelo, 5.3)
            self.assert_passaro_posicao(71, 16, ATIVO, passaro_amarelo, 5.3100000000000005)
            self.assert_passaro_posicao(71, 16, ATIVO, passaro_amarelo, 5.32)
            self.assert_passaro_posicao(72, 16, ATIVO, passaro_amarelo, 5.33)
            self.assert_passaro_posicao(72, 16, ATIVO, passaro_amarelo, 5.34)
            self.assert_passaro_posicao(72, 16, ATIVO, passaro_amarelo, 5.35)
            self.assert_passaro_posicao(72, 16, ATIVO, passaro_amarelo, 5.359999999999999)
            self.assert_passaro_posicao(72, 16, ATIVO, passaro_amarelo, 5.37)
            self.assert_passaro_posicao(73, 16, ATIVO, passaro_amarelo, 5.38)
            self.assert_passaro_posicao(73, 15, ATIVO, passaro_amarelo, 5.390000000000001)
            self.assert_passaro_posicao(73, 15, ATIVO, passaro_amarelo, 5.4)
            self.assert_passaro_posicao(73, 15, ATIVO, passaro_amarelo, 5.41)
            self.assert_passaro_posicao(74, 15, ATIVO, passaro_amarelo, 5.42)
            self.assert_passaro_posicao(74, 15, ATIVO, passaro_amarelo, 5.43)
            self.assert_passaro_posicao(74, 15, ATIVO, passaro_amarelo, 5.4399999999999995)
            self.assert_passaro_posicao(74, 15, ATIVO, passaro_amarelo, 5.45)
            self.assert_passaro_posicao(74, 15, ATIVO, passaro_amarelo, 5.46)
            self.assert_passaro_posicao(75, 14, ATIVO, passaro_amarelo, 5.470000000000001)
            self.assert_passaro_posicao(75, 14, ATIVO, passaro_amarelo, 5.48)
            self.assert_passaro_posicao(75, 14, ATIVO, passaro_amarelo, 5.49)
            self.assert_passaro_posicao(75, 14, ATIVO, passaro_amarelo, 5.5)
            self.assert_passaro_posicao(75, 14, ATIVO, passaro_amarelo, 5.51)
            self.assert_passaro_posicao(76, 14, ATIVO, passaro_amarelo, 5.52)
            self.assert_passaro_posicao(76, 14, ATIVO, passaro_amarelo, 5.529999999999999)
            self.assert_passaro_posicao(76, 13, ATIVO, passaro_amarelo, 5.54)
            self.assert_passaro_posicao(76, 13, ATIVO, passaro_amarelo, 5.55)
            self.assert_passaro_posicao(77, 13, ATIVO, passaro_amarelo, 5.5600000000000005)
            self.assert_passaro_posicao(77, 13, ATIVO, passaro_amarelo, 5.57)
            self.assert_passaro_posicao(77, 13, ATIVO, passaro_amarelo, 5.58)
            self.assert_passaro_posicao(77, 13, ATIVO, passaro_amarelo, 5.59)
            self.assert_passaro_posicao(77, 13, ATIVO, passaro_amarelo, 5.6)
            self.assert_passaro_posicao(78, 12, ATIVO, passaro_amarelo, 5.609999999999999)
            self.assert_passaro_posicao(78, 12, ATIVO, passaro_amarelo, 5.62)
            self.assert_passaro_posicao(78, 12, ATIVO, passaro_amarelo, 5.63)
            self.assert_passaro_posicao(78, 12, ATIVO, passaro_amarelo, 5.640000000000001)
            self.assert_passaro_posicao(78, 12, ATIVO, passaro_amarelo, 5.65)
            self.assert_passaro_posicao(79, 12, ATIVO, passaro_amarelo, 5.66)
            self.assert_passaro_posicao(79, 12, ATIVO, passaro_amarelo, 5.67)
            self.assert_passaro_posicao(79, 11, ATIVO, passaro_amarelo, 5.68)
            self.assert_passaro_posicao(79, 11, ATIVO, passaro_amarelo, 5.6899999999999995)
            self.assert_passaro_posicao(79, 11, ATIVO, passaro_amarelo, 5.7)
            self.assert_passaro_posicao(80, 11, ATIVO, passaro_amarelo, 5.71)
            self.assert_passaro_posicao(80, 11, ATIVO, passaro_amarelo, 5.720000000000001)
            self.assert_passaro_posicao(80, 11, ATIVO, passaro_amarelo, 5.73)
            self.assert_passaro_posicao(80, 10, ATIVO, passaro_amarelo, 5.74)
            self.assert_passaro_posicao(81, 10, ATIVO, passaro_amarelo, 5.75)
            self.assert_passaro_posicao(81, 10, ATIVO, passaro_amarelo, 5.76)
            self.assert_passaro_posicao(81, 10, ATIVO, passaro_amarelo, 5.77)
            self.assert_passaro_posicao(81, 10, ATIVO, passaro_amarelo, 5.779999999999999)
            self.assert_passaro_posicao(81, 10, ATIVO, passaro_amarelo, 5.79)
            self.assert_passaro_posicao(82, 9, ATIVO, passaro_amarelo, 5.8)
            self.assert_passaro_posicao(82, 9, ATIVO, passaro_amarelo, 5.8100000000000005)
            self.assert_passaro_posicao(82, 9, ATIVO, passaro_amarelo, 5.82)
            self.assert_passaro_posicao(82, 9, ATIVO, passaro_amarelo, 5.83)
            self.assert_passaro_posicao(82, 9, ATIVO, passaro_amarelo, 5.84)
            self.assert_passaro_posicao(83, 9, ATIVO, passaro_amarelo, 5.85)
            self.assert_passaro_posicao(83, 8, ATIVO, passaro_amarelo, 5.859999999999999)
            self.assert_passaro_posicao(83, 8, ATIVO, passaro_amarelo, 5.87)
            self.assert_passaro_posicao(83, 8, ATIVO, passaro_amarelo, 5.88)
            self.assert_passaro_posicao(84, 8, ATIVO, passaro_amarelo, 5.890000000000001)
            self.assert_passaro_posicao(84, 8, ATIVO, passaro_amarelo, 5.9)
            self.assert_passaro_posicao(84, 8, ATIVO, passaro_amarelo, 5.91)
            self.assert_passaro_posicao(84, 7, ATIVO, passaro_amarelo, 5.92)
            self.assert_passaro_posicao(84, 7, ATIVO, passaro_amarelo, 5.93)
            self.assert_passaro_posicao(85, 7, ATIVO, passaro_amarelo, 5.9399999999999995)
            self.assert_passaro_posicao(85, 7, ATIVO, passaro_amarelo, 5.95)
            self.assert_passaro_posicao(85, 7, ATIVO, passaro_amarelo, 5.96)
            self.assert_passaro_posicao(85, 6, ATIVO, passaro_amarelo, 5.970000000000001)
            self.assert_passaro_posicao(85, 6, ATIVO, passaro_amarelo, 5.98)
            self.assert_passaro_posicao(86, 6, ATIVO, passaro_amarelo, 5.99)
            self.assert_passaro_posicao(86, 6, ATIVO, passaro_amarelo, 6.0)
            self.assert_passaro_posicao(86, 6, ATIVO, passaro_amarelo, 6.01)
            self.assert_passaro_posicao(86, 5, ATIVO, passaro_amarelo, 6.02)
            self.assert_passaro_posicao(86, 5, ATIVO, passaro_amarelo, 6.03)
            self.assert_passaro_posicao(87, 5, ATIVO, passaro_amarelo, 6.04)
            self.assert_passaro_posicao(87, 5, ATIVO, passaro_amarelo, 6.05)
            self.assert_passaro_posicao(87, 5, ATIVO, passaro_amarelo, 6.06)
            self.assert_passaro_posicao(87, 5, ATIVO, passaro_amarelo, 6.07)
            self.assert_passaro_posicao(88, 4, ATIVO, passaro_amarelo, 6.08)
            self.assert_passaro_posicao(88, 4, ATIVO, passaro_amarelo, 6.09)
            self.assert_passaro_posicao(88, 4, ATIVO, passaro_amarelo, 6.1)
            self.assert_passaro_posicao(88, 4, ATIVO, passaro_amarelo, 6.11)
            self.assert_passaro_posicao(88, 4, ATIVO, passaro_amarelo, 6.12)
            self.assert_passaro_posicao(89, 3, ATIVO, passaro_amarelo, 6.13)
            self.assert_passaro_posicao(89, 3, ATIVO, passaro_amarelo, 6.14)
            self.assert_passaro_posicao(89, 3, ATIVO, passaro_amarelo, 6.15)
            self.assert_passaro_posicao(89, 3, ATIVO, passaro_amarelo, 6.16)
            self.assert_passaro_posicao(89, 3, ATIVO, passaro_amarelo, 6.17)
            self.assert_passaro_posicao(90, 2, ATIVO, passaro_amarelo, 6.18)
            self.assert_passaro_posicao(90, 2, ATIVO, passaro_amarelo, 6.19)
            self.assert_passaro_posicao(90, 2, ATIVO, passaro_amarelo, 6.2)
            self.assert_passaro_posicao(90, 2, ATIVO, passaro_amarelo, 6.21)
            self.assert_passaro_posicao(91, 1, ATIVO, passaro_amarelo, 6.22)
            self.assert_passaro_posicao(91, 1, ATIVO, passaro_amarelo, 6.23)
            self.assert_passaro_posicao(91, 1, ATIVO, passaro_amarelo, 6.24)
            self.assert_passaro_posicao(91, 1, ATIVO, passaro_amarelo, 6.25)
            self.assert_passaro_posicao(91, 1, ATIVO, passaro_amarelo, 6.26)
            self.assert_passaro_posicao(92, 0, ATIVO, passaro_amarelo, 6.29)
            passaro_amarelo.colidir_com_chao()
            self.assertEqual(DESTRUIDO, passaro_amarelo.status)
            # Código de geração de testes

            # for delta_t in range(0, 550):
            # t = 2 + (delta_t / 100)
            # x, y = passaro_amarelo.calcular_posicao(t)
            # print('        self.assert_passaro_posicao(%s, %s, ATIVO, passaro_amarelo, %s)' % (x, y, t))

        def assert_posicao_vertical(self, y, tempo, passaro):
            """
             Método auxiliar que mantém x fixo com valor 1, status Ativo, variando apenas o tempo e a posição y
             Atenção, esse não é um teste porque não começa com prefixo "test"
             """
            self.assert_passaro_posicao(1, y, ATIVO, passaro, tempo)

    if __name__ == '__main__':
        teste = AtorTestes()
        teste.teste_colisao_entre_atores_ativos()

