import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def setup():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver  
    driver.quit()  

def search(driver, query):
    """
    Realiza una búsqueda ingresando el texto en la barra de búsqueda.
    """
    driver.get("http://localhost:8080/")

    wait = WebDriverWait(driver, 10)
    search_bar = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//div[contains(@class, 'input-group')]/input[@class='form-control']")
    ))
    search_bar.send_keys(query)
    search_bar.send_keys(Keys.RETURN)

def test_search(setup):
    driver = setup
    search(driver, "Radiohead")

    assert "Radiohead" in driver.page_source

def test_results_table(setup):
    driver = setup
    search(driver, "Radiohead")

    wait = WebDriverWait(driver, 10)
    results_table = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//div[contains(@class, 'table-responsive')]")
    ))
    assert results_table is not None  

def test_columns_in_table(setup):
    driver = setup
    band_name = "Radiohead"
    search(driver, band_name)
    
    wait = WebDriverWait(driver, 10)
    results_table = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//div[contains(@class, 'table-responsive')]/table")
    ))

    headers = results_table.find_elements(By.XPATH, ".//thead/tr/th")
    header_texts = [header.text.strip() for header in headers]

    expected_columns = ["Nombre canción", "Nombre álbum", "URL preview", "Precio", "Fecha de lanzamiento"]

    for column in expected_columns:
        assert column in header_texts, f"El campo '{column}' no está presente en la tabla. Encabezados encontrados: {header_texts}"


def test_maximum_results(setup):
    driver = setup
    band_name = "Radiohead"
    search(driver, band_name)
    
    wait = WebDriverWait(driver, 10)
    results_table = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//div[contains(@class, 'table-responsive')]/table")
    ))

    rows = results_table.find_elements(By.XPATH, ".//tbody/tr")

    max_results = 25
    assert len(rows) <= max_results, f"La tabla contiene más de {max_results} registros. Total encontrado: {len(rows)}"


