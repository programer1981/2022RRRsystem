#!/usr/bin/python
# -*- coding: UTF-8 -*-
import socket
from threading import Thread
import os
import shutil
import glob
import random
import sys
import fileinput
import datetime
import time
from datetime import datetime
word1 = 'Sensor ID'
word2 ="tmp outside"
Tempfile_path=r"C:\Users\sasha\OneDrive\Рабочий стол\тягун\tempFille\tempFille.txt"
Path = r'C:\Users\sasha\OneDrive\Рабочий стол\тягун'
# from openyfail.timr import now
from datetime import date

TCP_IP = ''
TCP_PORT = 9013
BUFFER_SIZE = 1024

count = 0
swit = 0
def errorFile(ID):
    PathData = os.path.join(Path, 'Database')
    if not os.path.exists(PathData):
        os.mkdir(PathData)

    err_Path = os.path.join(PathData,"err")
    if not os.path.exists(err_Path):
        os.mkdir(err_Path)
    with open(Tempfile_path, 'r') as r:
        current_datetime = datetime.now()
        data = str(current_datetime.year) + "-" + str(current_datetime.month) + "-" + str(current_datetime.day)
        time = str(current_datetime.hour) + ":" + str(current_datetime.minute) + ":" + str(
            current_datetime.minute) + ":" + str(current_datetime.second)
        with open(err_Path + '/' + str(ID) + data+" "+time + '_S' + ".txt", 'w') as w:
            for i in r:
                if i != "\n":
                    w.write(i)


def find_data(Tempfile_path):
    data=0
    time=0
    ID=0
    with open(Tempfile_path, 'r') as f:
        for line in f:

            if not line.find("Date"):
                data=line.split()[1]
                time=line.split()[2]
                print(data)
                print(time)

            elif not line.find("Sensor ID"):
                ID = line.split()[2]
            if data !=0 and  time !=0 and ID !=0:
                print(data)
                print(time)
                print(ID)
                break

        if data == 0 or time == 0 or ID == 0:
            current_datetime = datetime.now()
            data=str(current_datetime.year)+"-"+str(current_datetime.month)+"-"+str(current_datetime.day)
            time=str(current_datetime.hour)+":"+str(current_datetime.minute)+":"+str(current_datetime.minute)+":"+str(current_datetime.second)
            ID="error filr"


    return data,time,ID



def addFolder(ID,datafile,time):

    PathData = os.path.join(Path, 'Database')
    if not os.path.exists(PathData):
        os.mkdir(PathData)

    ID_Path = os.path.join(PathData,str(ID))
    if not os.path.exists(ID_Path):
        os.mkdir(ID_Path)

    yearPath = os.path.join(ID_Path, datafile[:4])
    if not os.path.exists(yearPath):
        os.mkdir(yearPath)

    monthPath = os.path.join(yearPath, datafile[5:7])
    if not os.path.exists(monthPath):
            os.mkdir(monthPath)

    dayPath = os.path.join(monthPath, datafile[8:10])
    if not os.path.exists(dayPath):
        os.mkdir(dayPath)

    hourPath = os.path.join(dayPath, time[3:5])
    os.mkdir(hourPath)

    print("Folder created"+hourPath)

    # print(hourPath)
    with open(Tempfile_path, 'r') as r:
        if os.path.isfile(hourPath +'/'+str(ID)+datafile+'_S'+".txt"):
            errorFile(ID)
        else:
            with open(hourPath +'/'+str(ID)+datafile+'_S'+".txt", 'w') as w:
                for i in r:
                    if i !="\n":
                        w.write(i)


class ClientThread():

    def __init__(self, ip, port, sock, count):
        self.ip = ip
        self.port = port
        self.sock = sock
        # print(" New thread started for " + ip + ":" + str(port))

    def run(self):
        with open(Tempfile_path, 'w') as f:
            while True:
                data = self.sock.recv(1024).decode("utf-8")
                if not data:
                    break
                line = data.rstrip()
                if not line.find("Data"):
                    print("+++++")
                f.write(line)
        self.sock.close()
        print("file received")

        self.sock.close()
        print("file received")
        # time.sleep(2)
        datafile,time,ID=find_data(Tempfile_path)
        addFolder(ID,datafile,time)


                # addFolder(word_strain_1)

        print("File save to folder sucssful")
tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpsock.listen(5)
    print("Waiting for incoming connections...")
    (conn, (ip, port)) = tcpsock.accept()
    print('Got connection from ', (ip, port))
    count = count + 1
    newthread = ClientThread(ip, port, conn, count)
    newthread.run()
    # print(count)

