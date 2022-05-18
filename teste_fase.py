# -*- coding: utf-8 -*-
from itertools import chain
from teste_atores import ATIVO
from teste_atores import Obstaculo, DESTRUIDO , ATIVO , DuploLancamentoExcecao



VITORIA = 'VITORIA'
DERROTA = 'DERROTA'
EM_ANDAMENTO = 'EM_ANDAMENTO'


class Ator_Fake:
    def __init__(self, x=0, y=0):
        self.y = y
        self.x = x
        self.status = ATIVO
        self.colidir_executado = False
        self.calcular_posição_executado = False
        self.intervalo_colisao = None

    def calcular_posicao(self, tempo):
        self.calcular_posição_executado = True

    def colidir(self, outro_ator, intervalo):
        self.colidir_executado = outro_ator.colidir_executado = True
        self.intervalo_colisao = outro_ator.intervalo_colisao = intervalo

    def caracter(self):
        return ' '


class ObstaculoFake(Ator_Fake):
    pass


class PorcoFake(Ator_Fake):
    pass


class PassaroFake(Ator_Fake):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self._lancado = False
        self.colidir_com_chao_executado = False

    def foi_lancado(self):
        return self._lancado

    def lancar(self, angulo, tempo):
        if self._lancado:
            raise DuploLancamentoExcecao()
        self._lancado = True

    def colidir_com_chao(self):
        self.colidir_com_chao_executado = True

class FaseTestes():
    def teste_adicionar_obstaculo(self):
        fase = Fase()
        self.assertListEqual([], fase._obstaculos)
        obstaculo = ObstaculoFake()
        fase.adicionar_obstaculo(obstaculo)
        self.assertListEqual([obstaculo], fase._obstaculos)

        obstaculo1, obstaculo2 = ObstaculoFake(), ObstaculoFake()
        fase.adicionar_obstaculo(obstaculo1, obstaculo2)
        self.assertListEqual([obstaculo, obstaculo1, obstaculo2],
                             fase._obstaculos)

    def teste_adicionar_porco(self):
        fase = Fase()
        self.assertListEqual([], fase._porcos)
        porco = PorcoFake()
        fase.adicionar_porco(porco)
        self.assertListEqual([porco], fase._porcos)

        porco1, porco2 = PorcoFake(), PorcoFake()
        fase.adicionar_porco(porco1, porco2)
        self.assertListEqual([porco, porco1, porco2], fase._porcos)

    def teste_adicionar_passaro(self):
        fase = Fase()
        self.assertListEqual([], fase._passaros)
        passaro = PassaroFake()
        fase.adicionar_passaro(passaro)
        self.assertListEqual([passaro], fase._passaros)

        passaro1, passaro2 = PassaroFake(), PassaroFake()
        fase.adicionar_passaro(passaro1 ,passaro2)
        self.assertListEqual([passaro, passaro1, passaro2], fase._passaros)

    def teste_acabou_sem_porcos(self):
        fase = Fase()
        self.assertListEqual(VITORIA, fase.status())

    def teste_acabou_com_porcos_e_passaros(self):
        fase = Fase
        porcos = [PorcoFake(1 ,1) for _ in range(2)]
        passaros =[PassaroFake(1 ,1) for _ in range(2)]
        fase.adicionar_porco(*porcos)
        fase.adicionar_passaro(*passaros)

        self.assertEqual(EM_ANDAMENTO, fase.status())

        for ator in porcos + passaros:
            ator.status = DESTRUIDO
        self.assertEqual(VITORIA, fase.status())

        fase.adicionar_obstaculo(ObstaculoFake())
        self.assertEqual(VITORIA, fase.status(),
                         'Obstáculos não interfere no fim do jogo')

        fase.adicionar_porco(PorcoFake())
        self.assertEqual(DERROTA, fase.status(),
                         'Com Porco ativo e sem pássaro para lançar, o jogo'
                         'deveria acabar')

        fase.adicionar_passaro(PassaroFake())
        self.assertEqual(EM_ANDAMENTO, fase.status(),
                         'Com Porco ativo e com pássaro para lançar, o jogo'
                         'nao deveria acabar')
        porcos.status = DESTRUIDO
        self.assertEqual(VITORIA, fase.status(),
                         'Sem porco ativo, o jogo deveria acabar com vitória')

    def testar_lancar_passaro_sem_erro_quando_nao_existe_passaro(self):
        passaro = [PassaroFake(1,1) for _ in range (2)]
        fase = Fase()
        fase.adicionar_passaro(*passaro)
        self.assertFalse(passaro[0].foi_lancado())
        self.assertFalse(passaro[1].foi_lancado())
        fase.lancar(90,1)
        fase.lancar(45,3)
        fase.lancar(31,5)


        self.assertTrue(passaro[0].foi_lancado())
        self.assertTrue(passaro[1].foi_lancado())


class Ponto():
    def __init__(self, x, y, caracter):
        self.caracter = caracter
        self.x = round(x)
        self.y = round(y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.caracter == other.caracter

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def __repr__(self, *args, **kwargs):
        return "Ponto(%s,%s,'%s')" % (self.x, self.y, self.caracter)


class Fase():
    def __init__(self, intervalo_de_colisao=1):
        """
        Método que inicializa uma fase.

        :param intervalo_de_colisao:
        """
        self.intervalo_de_colisao = intervalo_de_colisao
        self._passaros = []
        self._porcos = []
        self._obstaculos = []
    def adicionar_obstaculo(self, *obstaculos):
        """
        Adiciona obstáculos em uma fase

        :param obstaculos:
        """
        self._obstaculos.extend(obstaculos)

    def adicionar_porco(self, *porcos):
        """
        Adiciona porcos em uma fase

        :param porcos:
        """
        self._porcos.extend(porcos)

    def adicionar_passaro(self, *passaros):
        """
        Adiciona pássaros em uma fase

        :param passaros:
        """
        self._passaros.extend(passaros)

    def status(self):
        """
        Método que indica com mensagem o status do jogo

        Se o jogo está em andamento (ainda tem porco ativo e pássaro ativo), retorna essa mensagem.

        Se o jogo acabou com derrota (ainda existe porco ativo), retorna essa mensagem

        Se o jogo acabou com vitória (não existe porco ativo), retorna essa mensagem

        :return:
        """
        if not self._possui_porcos_ativos():
            return VITORIA
        elif self._possui_passaros_ativos():
            return EM_ANDAMENTO
        else:
            return DERROTA

    def teste_intervalo_de_colisao_padrao(self):

        fase = Fase()
        passaro = PassaroFake(1, 1)
        fase.adicionar_passaro(passaro)
        porco = PorcoFake(2,2)
        fase.adicionar_porco(porco)
        fase.calcular_pontos(0)
        self.assertTrue(passaro.colidir_executado)
        self.assertTrue(porco.colidir_executado)
        self.assertTrue(passaro.calcular_posição_executado)
        self.assertTrue(passaro.colidir_com_chao_executado)
        self.assertEqual(1, passaro.intervalo_colisao)
        self.assertEqual(1, porco.intervalo_colisao)

    def teste_intervalo_de_colisao_nao_padrao(self):

        fase = Fase(30)
        passaro = PassaroFake(1, 1)
        fase.adicionar_passaro(passaro)
        porco = PorcoFake(31, 31)
        fase.adicionar_porco(porco)
        fase.calcular_pontos(0)
        self.assertEqual(30, passaro.intervalo_colisao)
        self.assertEqual(30, porco.intervalo_colisao)
        



    def lancar(self, angulo, tempo):
        """
        Método que executa lógica de lançamento.

        Deve escolher o primeiro pássaro não lançado da lista e chamar seu método lançar

        Se não houver esse tipo de pássaro, não deve fazer nada

        :param angulo: ângulo de lançamento
        :param tempo: Tempo de lançamento
        """
        for passaros in self._passaros:
            if not passaros.foi_lancado():
                passaros.lancar(angulo, tempo)
                break

    def calcular_pontos(self, tempo):
        """
        Lógica que retorna os pontos a serem exibidos na tela.

        Cada ator deve ser transformado em um Ponto.

        :param tempo: tempo para o qual devem ser calculados os pontos
        :return: objeto do tipo Ponto
        """
        for passaro in self._passaros:
            passaro.calcular_posicao(tempo)
            for alvo in self._obstaculos + self._porcos:
                passaro.colidir(alvo, self.intervalo_de_colisao)
            passaro.colidir_com_chao()
        pontos = [self._transformar_em_ponto(a) for a in self._passaros + self._obstaculos+ self._porcos]

        return pontos

    def _transformar_em_ponto(self, ator):
        return Ponto(ator.x, ator.y, ator.caracter())

    def _possui_porcos_ativos(self):
        for porco in self._porcos:
            if porco.status == ATIVO:
                return True
        return False

    def _possui_passaros_ativos(self):
        for passaro in self._passaros:
            if passaro.status == ATIVO:
                return True
        return False

