import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


driver = webdriver.Chrome()
wait = WebDriverWait(driver, 15)


driver.get("https://rera.odisha.gov.in/projects/project-list")


with open("rera_projects.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)


    writer.writerow(["Project Name", "RERA Regd. No.", "Promoter Name", "Promoter Address", "GST No."])


    project_links = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(text(), 'View Details')]")))
    num_projects = min(6, len(project_links))

    for i in range(num_projects):
        project_links = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[contains(text(), 'View Details')]")))

        driver.execute_script("arguments[0].scrollIntoView(true);", project_links[i])
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", project_links[i])

        wait.until(EC.presence_of_element_located((By.XPATH, "//h5[@id='details-of-the-projects']")))

        try:
            wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='details-project']/strong")))
            project_name = driver.find_element(By.XPATH,
                                               "//div[contains(@class,'details-project')][label[text()='Project Name']]/strong").text.strip()
        except:
            project_name = "N/A"

        try:
            rera_no = driver.find_element(By.XPATH,
                                          "//div[contains(@class,'details-project')][label[text()='RERA Regd. No.']]/strong").text.strip()
        except:
            rera_no = "N/A"


        try:
            promoter_tab = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Promoter Details')]")))
            driver.execute_script("arguments[0].click();", promoter_tab)
            wait.until(EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Company Name')]")))

            try:
                element = driver.find_element(By.XPATH,
                                              "//label[contains(text(), 'Company Name')]/following-sibling::strong")
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(1)
                promoter_name = element.text.strip()
            except:
                promoter_name = "N/A"


            try:
                element = driver.find_element(By.XPATH,
                                              "//label[contains(text(), 'Registered Office Address')]/following-sibling::strong")
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(1)
                promoter_address = element.text.strip()
            except:
                promoter_address = "N/A"

            try:
                element = driver.find_element(By.XPATH,
                                              "//label[contains(text(), 'GST No.')]/following-sibling::strong")
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(1)
                gst_no = element.text.strip()
            except:
                gst_no = "N/A"

        except:
            promoter_name = promoter_address = gst_no = "N/A"

        writer.writerow([project_name, rera_no, promoter_name, promoter_address, gst_no])

        print(f"Project {i + 1}")
        print(f"Project Name     : {project_name}")
        print(f"RERA Regd. No.   : {rera_no}")
        print(f"Promoter Name    : {promoter_name}")
        print(f"Promoter Address : {promoter_address}")
        print(f"GST No.          : {gst_no}")
        print("\n" + "-" * 50 + "\n")

        driver.back()
        time.sleep(2)

driver.quit()

print("Data saved to 'rera_projects.csv'")