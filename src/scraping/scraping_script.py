from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

def extract_data_from_page(url, current_date, driver):
    driver.get(url)
    time.sleep(0.5) # Esperar a que cargue la página
    
    # Lógica de extracción de datos (como lo tenías antes)
    # Aquí obtienes los datos de la tabla y creas un DataFrame
    soup = BeautifulSoup(driver.page_source, "html.parser")
    table = soup.find("table", class_="table-scroll")
    
    if table:
        rows = table.find("tbody").find_all("tr")
        data = []
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 10:
                data.append([
                    cols[0].text.strip(),
                    cols[1].text.strip(),
                    cols[2].text.strip(),
                    cols[3].text.strip(),
                    cols[5].text.strip(),
                    cols[6].text.strip(),
                    cols[7].text.strip(),
                    cols[9].text.strip(),
                    cols[10].text.strip()
                ])
        columns = ["Date & Time UTC", "Lat. degrees", "Lon. degrees", "Depth km",
                   "Region", "Type", "A/M", "Magnitude", "Network"]
        df = pd.DataFrame(data, columns=columns)
        return df
    return pd.DataFrame()  # Si no encuentra la tabla, devuelve un DataFrame vacío.


def scrape_data_for_days(start_date, num_days, driver):
    all_data = pd.DataFrame()
    current_date = start_date

    for _ in range(num_days):
        print(f"Scrapeando datos para la fecha: {current_date}")

        # Crear la URL con la fecha
        url = f"https://www.emsc-csem.org/Earthquake_data/index.php?date={current_date}"

        # Extraer los datos
        df = extract_data_from_page(url, current_date, driver)
        all_data = pd.concat([all_data, df], ignore_index=True)

        # Intentar encontrar el botón "Next" para pasar de página
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@class='pag spes spes1']"))
            )
            if next_button.is_displayed():
                next_button.click()
                print("Clic en el botón 'Next'")
                time.sleep(0.5)  # Esperar para que se cargue la siguiente página
            else:
                print("No hay más páginas.")
                break
        except Exception as e:
            print("Error al encontrar el botón 'Next':", e)
            break

        # Restar un día para el próximo ciclo
        current_date = (pd.to_datetime(current_date) - pd.Timedelta(days=1)).strftime('%Y-%m-%d')

    return all_data

import os


def main():
    # Configuración de Selenium
    options = Options()
    options.add_argument("--headless")  # Ejecutar en segundo plano
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Inicializar el driver de Selenium
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Fecha de inicio y número de días
    start_date = '2025-04-01'  # Fecha de inicio
    num_days = 7000  # Número de días a scrapear 7000

    # Llamar a la función para scrapear los datos
    scraped_data = scrape_data_for_days(start_date, num_days, driver)

    # Obtener la ruta absoluta del directorio donde está este script
    project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

    
    # Construir la ruta relativa a la carpeta 'data'
    data_dir = os.path.join(project_dir, "data")

    os.makedirs(data_dir, exist_ok=True)  # Crear la carpeta si no existe

    # Ruta completa del archivo CSV
    csv_path = os.path.join(data_dir, "scraped_earthquakes.csv")
    
    # Guardar el DataFrame en CSV
    scraped_data.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"Datos guardados en: {csv_path}")

    driver.quit()  # Cerrar el navegador al final

if __name__ == "__main__":
    main()

