#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def get_ip_from_file(abspath):
    all_ips = []
    for dir_from_main_dir in os.listdir(abspath):
        if not dir_from_main_dir.startswith('.'):
            for file_from_dirs in os.listdir(abspath + dir_from_main_dir):
                if file_from_dirs == 'UserInformation.txt':
                    with open(abspath + dir_from_main_dir + '/' + file_from_dirs, "r") as f:
                        file_contents = f.readlines()
                        if not file_contents:
                            continue
                        founded_ip = file_contents[12].split()[1]
                        all_ips.append(founded_ip)
    return all_ips


def get_countries_ids(ip_list):
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument('--headless')
    service = Service('/opt/WebDriver/bin/chromedriver')
    driver = webdriver.Chrome(options=options, service=service)
    countries_ids = []
    for ip in ip_list:
        driver.get("https://ipgeolocation.io/ip-location/")
        ip_input_form = driver.find_element(By.XPATH, "//*[@id='inputIPAddress']")
        ip_input_form.clear()
        ip_input_form.send_keys(ip)
        button = driver.find_element(By.ID, "btnSearch")
        button.click()
        country_id = driver.find_element(By.XPATH, "//*[@id='ipInfoTable']/tbody/tr[5]/td[2]")
        countries_ids.append(country_id.text)
    driver.close()
    return countries_ids


def rename_dirs_in_abspath(countries_ids, abspath):
    files_from_abspath = [f for f in os.listdir(abspath) if not f.startswith('.')]
    os.chdir(abspath)
    for file, country_id in zip(files_from_abspath, countries_ids):
        os.rename(file, file.replace("UNKNOWN", country_id))


if __name__ == "__main__":
    abspath = input("Please, enter an absolute path with logs here: ")
    ip_list = get_ip_from_file(abspath)
    countries_ids = get_countries_ids(ip_list)
    rename_dirs_in_abspath(countries_ids, abspath)
