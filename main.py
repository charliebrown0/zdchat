# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from tkinter import *
import tkinter.messagebox
import websocket
import threading
from threading import Thread
import time
import socket
#from Data import Data
import json
#import tkinter.scrolledtext
#from tkinter import scrolledtext
from tkinter.scrolledtext import ScrolledText
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
#net_msgs = "" #接收网络信息

def run():
    def fun_timer():
        print("timer running......")
        data = [
            {
                'type': 'ping',
            }
        ]
        ws.send(json.dumps(data))
        global timer
        timer = threading.Timer(30, fun_timer)
        timer.start()

    timer = threading.Timer(30, fun_timer)
    timer.start()

    ws.run_forever()

def sendMsg():
    strMsg = "我 ： " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n"
    txtMsgList.config(state=NORMAL)
    txtMsgList.insert(END, strMsg)
    txtMsgList.insert(END, txtMsg.get('0.0', END))
    txtMsgList.see(END)
    txtMsgList.config(state=DISABLED)
    data = [
        {
            'src': ip,
            'dst': "",
            'hostname': hostname,
            'msg': txtMsg.get('0.0', END)
        }
    ]
    ws.send(json.dumps(data))
    txtMsg.delete('0.0', END)

def cancelMsg():
    txtMsg.delete('0.0', END)


#UI
t = Tk()
t.title("zdchat")
frmLT = Frame(width=500, height=320, bg='white')
frmLC = Frame(width=500, height=150, bg='white')
frmLB = Frame(width=500, height=30)
frmRT = Frame(width=200, height=500)

frmLT.grid()
frmLC.grid()
frmLB.grid()
frmRT.grid(row=0, column=1, rowspan=3, padx=2, pady=3)

#创建控件
txtMsgList = ScrolledText(frmLT)

txtMsg = Text(frmLC)
btnSend = Button(frmLB, text='发送', width=8, command=sendMsg)
btnCancel = Button(frmLB, text='取消', width=8, command=cancelMsg)

txtMsgList.grid()
txtMsg.grid()
btnSend.grid(row=2, column=1)
btnCancel.grid(row=2, column=2)

#Thread(target=fresh, args=(txtMsgList,)).start()

def on_message(ws, message):
    print("from network : " + message)
    #global net_msgs # 此处必须用net_msgs
    #net_msgs = message
    txtMsgList.config(state=NORMAL)
    txtMsgList.insert(END, message)
    txtMsgList.see(END)
    tkinter.messagebox.showinfo("news")
    txtMsgList.config(state=DISABLED)

def on_error(ws, error):
    print(error)
def on_close(ws):
    print("### closed ###")
def on_open(ws):
    data = [
        {
            'type': 'reg',
            'src': ip,
            'dst': "",
            'hostname': hostname,
            'msg': ""
        }
    ]
    ws.send(json.dumps(data))
    print("websocket working......")

if __name__ == '__main__':
    ws = websocket.WebSocketApp("ws://121.37.188.58:8282", on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
    Thread(target=run).start() #websocket心跳另起线程
    t.mainloop()


