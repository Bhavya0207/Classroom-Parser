from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time


def main():
    head = input("Enter subject name:")
    PATH = Service("C:\Program Files (x86)\chromedriver.exe")
    driver = webdriver.Chrome(service=PATH)
    driver.get("https://classroom.google.com/u/1/w/MzExOTQzMDkxMjA1/t/all")
    driver.maximize_window()

    # Login email
    input1 = driver.find_element(By.XPATH, '//*[@id="identifierId"]')
    input1.send_keys("emailHere")
    next1 = driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button/span')
    next1.click()
    time.sleep(5)

    # login password
    input2 = driver.find_element(
        By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input'
    )
    input2.send_keys("password here")
    next2 = driver.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button/span')
    next2.click()
    time.sleep(7)

    # parse to find subject
    soup = bs(driver.page_source, "html.parser")
    headings = soup.find_all("a", class_="onkcGd YVvGBb IMvYId P3W0Dd-Ysl7Fe zFfAHb")
    label = None
    for h in headings:
        if h.get("aria-label") == head:
            label = h.get("aria-label")

    # click on the heading
    xpath = f'//a[@aria-label="{label}"][@class="YVvGBb xUYklb VnOHwf-Tvm9db B7SYid"]'
    link = driver.find_element(By.XPATH, xpath)
    actions = ActionChains(driver)
    actions.move_to_element(link)
    actions.perform()
    time.sleep(1.5)
    link.click()
    time.sleep(5)

    # parse the files
    soup = bs(driver.page_source, "html.parser")
    fname = soup.find_all("div", class_="A6dC2c QDKOcc VBEdtc-Wvd9Cc zZN2Lb-Wvd9Cc")
    flink = soup.find_all("a", "vwNuXe JkIgWb QRiHXd MymH0d maXJsd")
    fnamel = []
    flinkl = []

    # make a data set
    for i in range(0, len(flink)):
        x = flink[i].get("href")
        x = x[:-1]
        x += "1"
        flinkl.append(x)
        fnamel.append(fname[i].get_text())
    driver.quit()

    d = {"File Name": fnamel, "File link": flinkl}
    # print(d)
    df = pd.DataFrame(d)
    pd.set_option("display.max_colwidth", None)
    print(df)

    ch = input("Would you like to continue? (y/n):").lower()
    ch.strip()
    if ch == "y":
        main()
    else:
        print("Goodbye!")
        input()


if __name__ == "__main__":
    main()
