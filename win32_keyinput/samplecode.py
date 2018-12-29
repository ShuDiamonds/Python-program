import ctypes
import string
import time
import json

class WINKEY:
    __KEY_A = 0x41
    __ASCII_A = 97
    __keystatus = [False] * 26
    __keydownstatus = [False] * 26
    __keyupstatus = [False] * 26

    def update(self):
        for i in range(26):
            status = self.__getkeywin(self.__KEY_A+i)
            if (status and not self.__keystatus[i]):
                self.__keydownstatus[i] = True
            else:
                self.__keydownstatus[i] = False
            if(not status and self.__keystatus[i]):
                self.__keyupstatus[i] = True
            else:
                self.__keyupstatus[i] = False
            self.__keystatus[i] = self.__getkeywin(self.__KEY_A+i)

    def __getkeywin(self, key):
        return(bool(ctypes.windll.user32.GetAsyncKeyState(key)&0x8000))

    def __asciiIndex(self, key):
        return(ord(key.lower())-self.__ASCII_A)

    def getkey(self, key):
        return(self.__keystatus[self.__asciiIndex(key)])

    def getkeydown(self, key):
        return (self.__keydownstatus[self.__asciiIndex(key)])

    def getkeyup(self, key):
        return (self.__keyupstatus[self.__asciiIndex(key)])

    def getESCAPE(self):
        return(bool(ctypes.windll.user32.GetAsyncKeyState(27)&0x8000))

if __name__ == '__main__':

    data = []
    data.append({"start":time.perf_counter()})
    print(time.perf_counter())
    agent = WINKEY()
    while True:
        agent.update()
        for c in string.ascii_letters[0:26]:
            if(agent.getkeydown(c)):
                data.append({c:time.perf_counter()})
                print(c)
        if(agent.getESCAPE()):
            fw = open("data.json", "w")
            json.dump(data, fw, indent=4)
            break
