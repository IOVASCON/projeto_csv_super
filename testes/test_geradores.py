# testes/test_geradores.py
import unittest
from datetime import datetime
from faker import Faker
from geradores import gerar_data_aleatoria, gerar_dados_empresa  # Ajuste o caminho se necessário


class TestGeradores(unittest.TestCase):

    def setUp(self):
        """Configuração para os testes."""
        self.fake = Faker("pt_BR")
        self.data_inicio = datetime(2023, 1, 1)
        self.data_fim = datetime(2023, 12, 31)

    def test_gerar_data_aleatoria(self):
        """Testa se a data gerada está dentro do intervalo."""
        data = gerar_data_aleatoria(self.data_inicio, self.data_fim)
        self.assertIsInstance(data, datetime)
        self.assertTrue(self.data_inicio <= data <= self.data_fim)

    def test_gerar_dados_empresa_sem_autocorrelacao(self):
      """Teste para geração inicial."""
      dados = gerar_dados_empresa(self.fake, "TI", datetime(2024, 1, 15))
      self.assertEqual(len(dados), 19) #Confere o número de colunas.
      self.assertIsInstance(dados[0], str) #Confere se a data é string
      self.assertIsInstance(dados[7], int)  # numero_clientes é inteiro

    def test_gerar_dados_empresa_com_autocorrelacao(self):
      """Teste com dados anteriores."""
      dados_anteriores = [
        '2024-01-15', 2024, 1, 15, 'TI', 'Empresa A', 'Cidade X', 100,
        50.00, 5000.00, 4000.00, 1000.00, 8.0, 75.00, 10.00, 500.00, 2000.00,
        5500.00, 4400.00, 50.00, 1.01, 500.00]
      dados = gerar_dados_empresa(self.fake, "TI", datetime(2024,1,16), dados_anteriores)

      #Verificações (exemplos - adicione mais conforme necessário)
      self.assertNotEqual(dados[7], dados_anteriores[7]) #Num clientes deve mudar.
      self.assertTrue(dados[9] > 0)  # Receita deve ser positiva.



if __name__ == "__main__":
    unittest.main()