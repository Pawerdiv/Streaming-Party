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


def play():
    driver.execute_script('document.getElementsByTagName("video")[0].play();')


def stop():
    driver.execute_script('document.getElementsByTagName("video")[0].pause()')


def getPlay():
    ps = 0
    value = driver.execute_script(' return document.getElementsByTagName("video")[0].paused')
    if value is True:
        ps = 1
    else:
        ps = 0
    return ps


def getCurrent():
    return driver.execute_script('return document.getElementsByTagName("video")[0].currentTime')


def goto(time):
    driver.execute_script('document.getElementsByTagName("video")[0].currentTime = '+str(time)+'')


def waitLoad():
    while True:
        try:
            WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.CLASS_NAME, 'vjs-big-play-button')))
            driver.find_element_by_class_name("vjs-big-play-button").click()
            break
        except :
            try:
                WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.CLASS_NAME, 'continue__button')))
                driver.find_element_by_class_name("continue__button").click()
                break
            except:
                print("Loading took too much time!")


def updateUrl():
    print("STARTED URL")
    status = ['-1', '-1', '0', '0', '3']
    if host == 0:
        if "lookmovie" not in currentUrl():
            driver.get("https://lookmovie.io/")
            status[2] = currentUrl()
            s.send(' '.join([str(elem) for elem in status]).encode())
            s.recv(4096)
        while True:

            status[2] = currentUrl()
            if "/view/" in status[2]:
                status[3] = '1'
                s.send(' '.join([str(elem) for elem in status]).encode())

                break
            s.send(' '.join([str(elem) for elem in status]).encode())
            s.recv(4096)

    if host == 1:
        driver.get("https://lookmovie.io/")
        current = currentUrl()
        while True:
            currentUrl()
            data = s.recv(4096)
            s.send('ricevuto'.encode())
            if len(data) > 0:
                status = (Convert(data.decode()))
                if status[2] != current:
                    current = status[2]
                    driver.get(status[2])

                if status[3] == '1':
                    break

    print("COMPLETE URL")
    videoUpdate(status)


def videoUpdate(status):
    print("STARTED VIDEO")
    waitLoad()
    diff = ['0', '0', '0', '0', '0']
    while True:

        if host == 0:
            if status[2] != currentUrl():
                status[3] = '0'
                s.send(' '.join([str(elem) for elem in status]).encode())
                break

            status[0] = getPlay()
            status[1] = getCurrent()

            s.send(' '.join([str(elem) for elem in status]).encode())
            s.recv(1000)

        if host == 1:

            diff[0] = getPlay()

            diff[1] = getCurrent()

            start = time.perf_counter()
            ret = s.recv(4096)
            s.send('ricevuto'.encode())
            dist = time.perf_counter() - start

            maxp = float(2)

            if len(ret) > 0:

                ret = (Convert(ret.decode()))
               # print(ret)
                if ret[3] == '0':
                    break
                if ret[2] != currentUrl():
                    break
                if ret[0] != str(diff[0]):
                    if ret[0] == "1":
                        stop()
                    else:
                        play()
                if float(ret[1]) > float(diff[1])+maxp or float(diff[1]) > float(ret[1])+maxp:
                    goto(str(float(ret[1])+float(dist)))

    print("COMPLETE VIDEO")
    updateUrl()


def init(h, so, d):
    global host, s, driver

    host = h
    s = so
    driver = d
    updateUrl()