import socket
import os.path
import threading
import shutil
import glob
import sys
import fileinput
import datetime
import time
from datetime import datetime
TCP_IP = "95.170.130.163"
TCP_PORT = 9013
BUFFER_SIZE = 1024

Path = os.path.dirname(os.path.abspath(sys.argv[0]))
OmniPath = r"C:\Users\sasha\OneDrive\Рабочий стол\тягун\Omni"
res_path=r"C:\Users\sasha\OneDrive\Рабочий стол\тягун\reserved"
notsent_path=r"C:\Users\sasha\OneDrive\Рабочий стол\тягун\notsend"

def get_time(file,ID_line): # функция получает из файлу дату создания
    Time_file = time.ctime(os.path.getmtime(file))
    month = (Time_file[6:8])
    day = (Time_file[9:10])
    hours = (Time_file[11:13])
    min = (Time_file[14:16])
    sec = (Time_file[17:19])
    return str(ID_line+"_"+day+"_"+hours+"_"+min+"_"+sec)

def write_file(in_path,out_path,ID_line):
    flag = 1
    time_path = get_time(in_path, ID_line)

    # резервное копирование, и отчистка информаци
    f = open(in_path, "r")
    out = open(out_path + "/" + time_path + "_S.txt", "w")
    for line in f:
        if flag == 1:
            if not line.find("Sensor ID") == -1:
                out.write("Sensor ID" + " " + ID_line + "\n") #можно переименовывать сенсор
            else:
                out.write(line)
        if not line.find("[DATA]") == -1:#начала сбора данных
            flag = 0
        if flag == 0:
            if line.find("[DATA]") == -1:
                out.write(line.split()[0] + " " + line.split()[1] + "\n")
    f.close()
    out.close()


def Seve_to_BD_S(ID_line, file_path): # функция сохрняет резервную копию в отдельный папке, и сохоняет в папку неотправленые

    try: #резервное копирование, и отчистка информаци
        write_file(file_path, res_path, ID_line)
    except:
        exit(-1)

    linePath = os.path.join(notsent_path, ID_line) #создание минибазы данных для более удобной отправки
    if not os.path.exists(linePath):
        os.mkdir(linePath)

    time_path = get_time(file_path, ID_line)
    time_folder = os.path.join(linePath,time_path)
    if not os.path.exists(time_folder):
        os.mkdir(time_folder)
    print(time_folder)
    write_file(file_path, time_folder, ID_line)
    os.remove(file_path)

def get_files():
    ID_line=0
    for i in glob.glob(OmniPath + "\*mtx.txt"):  # Удаление файлов матриц
        os.remove(i)

    for i in glob.glob(OmniPath + "\*"):  # Удаление буферных измерений из системы
        f = open(i, "r")
        for line in f:
            if not line.find("Sensor ID"):
                ID_line= line.split()[2]
                break
        f.close()
        Seve_to_BD_S(ID_line,i)

def send_data(): #отправка данных
    for i in glob.glob(notsent_path + "/*/*"):
        print(i)
        try:
            for file in glob.glob(i+"/*"):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((TCP_IP, TCP_PORT))
                print(file)
                f = open(file, 'rb')
                l = f.read(1024)
                while (l):
                    s.send(l)
                    l = f.read(1024)
                f.close()
                print('Successfully get the file')
                s.close()
                print('connection closed')

            path = os.path.join(os.path.abspath(os.path.dirname(__file__)),i)
            shutil.rmtree(path)
            time.sleep(5)

        except Exception as e: print(e)

while(True):
    get_files()#сбор файлов с омнисенса резервное копирование
    print("sent")
    send_data() # Отправка файлов на сервер
    time.sleep(3)