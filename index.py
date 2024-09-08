#!/usr/bin/python3.9
#coding: utf-8


import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages')
import platform
import subprocess
import selenium
from selenium import webdriver
import socket
import os
import getpass
import threading
import wx
import time
import youtube
import lookmovie
import netflix
import prime

host = 2
s = socket.socket()
driver = webdriver
player = ''


def conn_sub_server(indirizzo_server):
    global link
    try:

        s.connect(indirizzo_server)
        print(indirizzo_server)
    except socket.error as errore:
        print("Qualcosa è andato storto, sto uscendo... \n{errore}")
        sys.exit()
    waitConn()
    getHost()
    link = indirizzo_server
    return s


def getHost():
    global host
    s.send("host".encode())
    data = s.recv(4096)
    host = int(data.decode())


def waitConn():
    while True:
        r = s.recv(4096)
        if r.decode() == "ok":
            break


def sistem():

    sistems = platform.system()
    user = getpass.getuser()
    options = webdriver.ChromeOptions()

    if sistems == "Darwin":
        os.system("pkill Google Chrome")

        try:
            os.mkdir("/Users/"+str(user)+"/Documents/Party")
            os.mkdir("/Users/"+str(user)+"/Documents/Party/Profile2")
        except:
            options.add_argument("user-data-dir=/Users/"+str(user)+"/Documents/Party/Profile2/")
        finally:
            options.add_argument("user-data-dir=/Users/"+str(user)+"/Documents/Party/Profile2/")

    if sistems == "Windows":
        subprocess.call("TASKKILL /f  /IM  CHROME.EXE", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        options.add_argument("user-data-dir=C:\\Users\\"+str(user)+"\\AppData\\Local\\Google\\Chrome\\User Data\\")

    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    return options


def Convert(string):
    li = list(string.split(" "))
    return li


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Party')
        panel = wx.Panel(self)
        my_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.text_ctrl = wx.TextCtrl(panel)
        my_sizer.Add(self.text_ctrl, 0, wx.ALL | wx.CENTER, 5)
        my_btn = wx.Button(panel, label='Connettiti')
        my_btn.Bind(wx.EVT_BUTTON, self.on_press)
        my_sizer.Add(my_btn, 0, wx.ALL | wx.CENTER, 5)
        panel.SetSizer(my_sizer)
        self.SetSize(220, 100)
        self.SetBackgroundColour(wx.Colour(35, 35, 35))
        self.Show()

    def on_press(self, event):
        value = self.text_ctrl.GetValue()
        if not value:
            print("Empty")
        else:
            self.Close(True)
            port = value.split(":")
           # conn_sub_server((port[0]+".tcp.ngrok.io", int(port[1])))
            print("Connessi entrambi")

            processHost = threading.Thread(target=conn_sub_server, args=((port[0]+".tcp.ngrok.io", int(port[1])),))
            processHost.start()


class choiceFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Choice')
        panel = wx.Panel(self)
        my_sizer = wx.BoxSizer(wx.VERTICAL)

        net = wx.Button(panel, label='Netflix', name='Netflix')
        net.Bind(wx.EVT_BUTTON, self.on_press)
        my_sizer.Add(net, 5, wx.ALL | wx.CENTER, 5)

        pri = wx.Button(panel, label='Prime', name='Prime')
        pri.Bind(wx.EVT_BUTTON, self.on_press)
        my_sizer.Add(pri, 5, wx.ALL | wx.CENTER, 5)

        you = wx.Button(panel, label='Youtube', name='Youtube')
        you.Bind(wx.EVT_BUTTON, self.on_press)
        my_sizer.Add(you, 5, wx.ALL | wx.CENTER, 5)

        look = wx.Button(panel, label='Lookmovie', name='Lookmovie')
        look.Bind(wx.EVT_BUTTON, self.on_press)
        my_sizer.Add(look, 5, wx.ALL | wx.CENTER, 5)

        panel.SetSizer(my_sizer)
        self.SetSize(220, 300)
        self.SetBackgroundColour(wx.Colour(35, 35, 35))
        self.Show()

    def on_press(self, event):
        global player
        ob = event.GetEventObject()
        player = ob.GetLabel()
        ob.Disable()
        process = threading.Thread(target=hostThread, args=(ob,))
        process.start()


def hostThread(ob):
    global driver, s, player

    while True:
        try:
            driver = webdriver.Chrome(options=sistem())#, executable_path="/usr/local/bin/chromedriver")
            if player == 'Netflix':
                netflix.init(host, s, driver)
            elif player == 'Prime':
                prime.init(host, s, driver)
            elif player == 'Youtube':
                youtube.init(host, s, driver)
            elif player == 'Lookmovie':
                lookmovie.init(host, s, driver)
        except Exception:
            print("Error:")
        finally:
            print("FINITO")
            if host == 0:
                s.send("-2".encode())
                ob.Enable()
                player = ''
                sys.exit()


def clientThread():
    global driver, s, player

    while True:
        try:
            driver = webdriver.Chrome(options=sistem())#, executable_path="/usr/local/bin/chromedriver")
            while True:
                data = s.recv(4096)
                s.send('ricevuto'.encode())
                status = (Convert(data.decode()))
                if status[-1] == '0':
                    netflix.init(host, s, driver)
                    break
                elif status[-1] == '1':
                    prime.init(host, s, driver)
                    break
                elif status[-1] == '2':
                    youtube.init(host, s, driver)
                    break
                elif status[-1] == '3':
                    lookmovie.init(host, s, driver)
                    break

        except Exception:
            print("Error:")

        try:
            driver.close()
        except Exception as e:
            try:
                s.send("-2".encode())
            except:
                sys.exit()
        try:
            s.send("-2".encode())
        except:
            sys.exit()


def apps():
    print("Ciclo")
    while True:
        if host == 0:
            app = wx.App()
            frm = choiceFrame()
            frm.Show()
            app.MainLoop()
        if host == 1:
            processThread2 = threading.Thread(target=clientThread)
            processThread2.start()
            break


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
    app.Destroy()
    apps()


