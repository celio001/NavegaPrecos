from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


class MercadoLivre:
    def __init__(self, pesquisar: str, nomeDoArquivo: str):
        self.produtoParaPesquisar = pesquisar
        self.nomeDoArquivo = nomeDoArquivo

    def pesquisar(self):
        self.driver = self._iniciar_driver()    # iniciamos o navegador
        # entra no site
        self.driver.get('https://www.mercadolivre.com.br/')

        try:
            self._pesquisarMercadoLivre()  # Ok
            self._pega_produtos()  # Em crição

        except Exception as e:
            print("Ocorreu uma exceção:", e)
        finally:
            input("verifica...")
            self.driver.close()  # encerramos o navegador no final de tudo

    def _iniciar_driver(self):  # Concluido
        chrome_options = Options()
        arguments = ['--lang=pt-BR', '--window-size=800,600',
                     '--incognito']
        for argument in arguments:
            chrome_options.add_argument(argument)

        chrome_options.add_experimental_option('prefs', {
            'download.prompt_for_download': False,
            'profile.default_content_setting_values.notifications': 2,
            'profile.default_content_setting_values.automatic_downloads': 1,
        })

        driver = webdriver.Chrome(service=ChromeService(
            ChromeDriverManager().install()), options=chrome_options)
        return driver

    # Pega o elemento DOM da pagina somente quando ele carregar
    def _querySelector(self, id: str, by: By):  # Concluido
        print(id)
        # Definir um tempo máximo de espera o elemento carregar de até 20 segundos
        wait = WebDriverWait(self.driver, 15)
        # Aguardar até que o elemento carregue
        wait.until(EC.presence_of_element_located((by, id)))
        return self.driver.find_element(by, id)

    def _pesquisarMercadoLivre(self):  # Concluido

        os.system('cls')  # limpa o pronpt de comando
        print("Vamos começar a pesquisa...")

        # Limpar a barra de pesquisa antes de inserir um novo termo de pesquisa para evitar erros
        self.driver.execute_script(
            f"document.querySelector('input.nav-search-input').value = ''")

        # Selecionamos o input de pesquisa do mercado livre e escrevermos a opção de pesquisa e inicia a pesquisa
        self._querySelector('input.nav-search-input', By.CSS_SELECTOR).send_keys(
            self.produtoParaPesquisar + Keys.RETURN)

        self._querySelector(
            '.andes-dropdown__standalone-arrow', By.CSS_SELECTOR).click()
        self._querySelector('li[data-key="price_asc"]',
                            By.CSS_SELECTOR).click()
        # data-key:
        # price_asc = Menor preço
        # relevance = Mais relevante
        # price_desc = Maior Preço

        # Seleciona os melhores vendedores
        self._querySelector(
            'a[aria-label="Melhores vendedores"]', By.CSS_SELECTOR).click()

    def _pega_produtos(self):
        # Pega os itens com os dados dos produtos
        itens = self.driver.execute_script(
            "return document.querySelectorAll('.ui-search-layout__item')")


mercado_livre = MercadoLivre("Celular", "Celular")
mercado_livre.pesquisar()
