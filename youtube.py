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


def waitLoad():
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'ytp-large-play-button')))
        driver.find_element_by_class_name("ytp-large-play-button").click()
    except :
        print("Loading took too much time!")


def play():
    driver.execute_script('document.getElementsByTagName("video")[0].play();')


def stop():
    driver.execute_script('document.getElementsByTagName("video")[0].pause();')


def getPlay():
    ps = 0
    value = driver.execute_script(' return document.getElementsByTagName("video")[0].paused')
    if value is True:
        ps = 1
    else:
        ps = 0
    return ps


def getCurrent():
    return driver.execute_script('return document.getElementsByTagName("video")[0].getCurrentTime()')


def goto(time):
    driver.execute_script('document.getElementsByTagName("video")[0].currentTime = '+str(time)+'')


def updateUrl():
    print("STARTED URL")
    status = ['-1', '-1', '0', '0', '2']
    if host == 0:
        if "netflix" not in currentUrl():
            driver.get("https://www.youtube.com")
            status[2] = currentUrl()
            s.send(' '.join([str(elem) for elem in status]).encode())
            s.recv(4096)
        while True:

            status[2] = currentUrl()
            if "/watch?" in status[2]:
                status[3] = '1'
                s.send(' '.join([str(elem) for elem in status]).encode())

                break
            s.send(' '.join([str(elem) for elem in status]).encode())
            s.recv(4096)

    if host == 1:
        driver.get("https://www.youtube.com")
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

#<button class="ytp-large-play-button ytp-button" aria-label="Play"><svg height="100%" version="1.1" viewBox="0 0 68 48" width="100%"><path class="ytp-large-play-button-bg" d="M66.52,7.74c-0.78-2.93-2.49-5.41-5.42-6.19C55.79,.13,34,0,34,0S12.21,.13,6.9,1.55 C3.97,2.33,2.27,4.81,1.48,7.74C0.06,13.05,0,24,0,24s0.06,10.95,1.48,16.26c0.78,2.93,2.49,5.41,5.42,6.19 C12.21,47.87,34,48,34,48s21.79-0.13,27.1-1.55c2.93-0.78,4.64-3.26,5.42-6.19C67.94,34.95,68,24,68,24S67.94,13.05,66.52,7.74z" fill="#f00"></path><path d="M 45,24 27,14 27,34" fill="#fff"></path></svg></button>