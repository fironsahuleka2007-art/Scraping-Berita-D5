from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def scrape_berita(url, limit):

    options = Options()
    options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(3)

    data = []

    judul = driver.find_elements(By.CSS_SELECTOR, "h3.article__title")

    link = driver.find_elements(By.CSS_SELECTOR, "a.article__link")

    tanggal = driver.find_elements(By.CSS_SELECTOR, ".article__date")

    for i, j in enumerate(judul[:limit]):
        data.append(git commit -m "upload main dan requirements"{
            "judul": j.text,
            "tanggal": tanggal[i].text if i < len(tanggal) else "-",
            "link": link[i].get_attribute("href") if i < len(link) else "-"
        })

    driver.quit()

    return data