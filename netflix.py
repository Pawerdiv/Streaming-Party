#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def netflixApi():
    return 'const videoPlayer = netflix.appContext.state.playerApp.getAPI().videoPlayer; const player = videoPlayer.getVideoPlayerBySessionId(videoPlayer.getAllPlayerSessionIds()[0]); '


def play():
    driver.execute_script('document.getElementsByTagName("video")[0].play();')


def stop():
    driver.execute_script('document.getElementsByTagName("video")[0].pause();')


def goto(time):
    driver.execute_script(netflixApi()+'player.seek('+str(time)+');')


def getCurrent():
    #return driver.execute_script(netflixApi()+'return (player.getCurrentTime());')
    return int(driver.execute_script('return document.getElementsByTagName("video")[0].currentTime')*1000)


def waitLoad():
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'PlayerControlsNeo__button-control-row')))
    except :
        print("Loading took too much time!")


def seek():
    return driver.execute_script('return document.getElementsByTagName("video")[0].seeking;')


def currentUrl():
    return driver.current_url


def startButton():
    try:
        driver.find_element_by_class_name("svg-icon-nfplayerOpticalCenterPlay").click()
    except:
        print("Partito")


def Convert(string):
    li = list(string.split(" "))
    return li


def getPlay():
    ps = 0
    value = driver.execute_script(netflixApi()+'return (player.isPlaying());')
    if value is True:
        ps = 0
    else:
        ps = 1

    return ps


def updateUrl():
    print("STARTED URL")
    status = ['-1', '-1', '0', '0', '0']
    if host == 0:
        if "netflix" not in currentUrl():
            driver.get("https://www.netflix.com/browse")
            status[2] = currentUrl()
            s.send(' '.join([str(elem) for elem in status]).encode())
            s.recv(4096)
        while True:

            status[2] = currentUrl()
            if "/watch/" in status[2]:
                status[3] = '1'
                s.send(' '.join([str(elem) for elem in status]).encode())

                break
            s.send(' '.join([str(elem) for elem in status]).encode())
            s.recv(4096)

    if host == 1:
        driver.get("https://www.netflix.com/browse")
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

            status[0] = getPlay()
            status[1] = getCurrent()

            start = time.perf_counter()
            ret = s.recv(4096)
            s.send('ricevuto'.encode())
            dist = time.perf_counter() - start

            maxp = 2000

            if len(ret) > 0:

                ret = (Convert(ret.decode()))
               # print(ret)
                if ret[3] == '0':
                    break
                if ret[2] != currentUrl():
                    break
                if ret[0] != str(status[0]):
                    if ret[0] == "1":
                        stop()
                    else:
                        play()

                if int(ret[1]) > int(status[1])+maxp or int(status[1]) > int(ret[1])+maxp:

                    goto(str(int(ret[1])+int(dist*1000)))

    print("COMPLETE VIDEO")
    updateUrl()


def init(h, so, d):
    global host, s, driver

    host = h
    s = so
    driver = d

    updateUrl()



