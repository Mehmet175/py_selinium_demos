from selenium import webdriver

import time

from selenium.webdriver.common.by import By

from eksi_settings_data import SettingsData


def write_to_file(content_list, setting: SettingsData):
    with open(setting.file_name, "w", encoding="utf-8") as file:
        file.write("Title : " + setting.file_title + "\n")
        file.write("Item Count : " + str(len(content_list)) + "\n")
        file.write("**********\n")
        for content in content_list:
            file.write(content + "\n")


def get_contents(setting: SettingsData):
    driver = webdriver.Chrome()
    driver.get(setting.url)
    time.sleep(2)

    # Maks sayfa sayısını al.
    max_page = setting.max_page

    try:
        # Web sayfasındaki sayfa sayısını al.
        page_count = driver.find_element(By.XPATH, '//*[@id="topic"]/div[1]/div[2]').find_element(By.CLASS_NAME, 'last')

        print("**********")
        print(page_count.text)

        # Eğer web sayfasındaki sayfa sayısı, maksimum sayfa sayısından büyükse, maksimum sayfa sayısını güncelle.
        web_page_count = int(page_count.text)
        if max_page > web_page_count:
            max_page = web_page_count
    except Exception as e:
        max_page = 1
        print("Sayfa sayısı alınamadı.")

    time.sleep(2)

    commands = []

    # Sayfalı link
    page_url = setting.url + "?p="
    for i in range(1, max_page + 1):
        driver.get(page_url + str(i))
        time.sleep(2)
        for item in driver.find_elements(By.CLASS_NAME, 'content'):
            commands.append(item.text)

    return commands


settings = SettingsData("https://eksisozluk.com/tanzim-kuyrugundaki-insanlarla-dalga-gecen-laik--5937852", 10000,
                        "contents.txt", "tanzim kuyruğundaki insanlarla dalga geçen laik")

contents = get_contents(settings)
write_to_file(contents, settings)
