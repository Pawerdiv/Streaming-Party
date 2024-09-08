#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def currentUrl():
    return driver.current_url


def Convert(string):
    li = list(string.split(" "))
    return li


def waitCopy():

    try:
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'EY0L4G')))
    finally:

        link = driver.find_element_by_class_name("EY0L4G").text

    return link


def updateUrl():
    print("STARTED URL")
    status = ['0', '0', '0', '1']

    if host == 0:

        if "primevideo" not in currentUrl():

            driver.get("https://www.primevideo.com/")
            status[0] = currentUrl()
            s.send(' '.join([str(elem) for elem in status]).encode())
            s.recv(4096)

        while True:

            status[0] = currentUrl()
            if "/watchparty/amzn" in status[0]:
                status[1] = waitCopy()
                if status[1] == '':
                    status[2] = '0'
                else:
                    status[2] = '1'
            else:
                status[2] = '0'

            s.send(' '.join([str(elem) for elem in status]).encode())
            s.recv(4096)

    if host == 1:

        driver.get("https://www.primevideo.com/")
        currentlink = 'other'
        current = currentUrl()

        while True:
            currentUrl()
            data = s.recv(4096)
            s.send('ricevuto'.encode())
            if len(data) > 0:
                status = (Convert(data.decode()))
                if status[2] == '1' and status[1] != '':
                    if status[1] != currentlink:
                        currentlink = status[1]
                        driver.get(status[1])
                else:
                    if status[0] != current:
                        current = status[0]
                        driver.get(status[0])

    print("COMPLETE URL")


def init(h, so, d):
    global host, s, driver

    host = h
    s = so
    driver = d

    updateUrl()