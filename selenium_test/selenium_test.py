import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

base_dir = os.path.dirname(os.path.abspath(__file__))

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.bcmitsubishiofsaltillo.com/new-vehicles/")

with open("{}/selenium_test.txt".format(base_dir), "w", encoding="utf-8") as ff:
    ff.write(driver.page_source)

driver.quit()
