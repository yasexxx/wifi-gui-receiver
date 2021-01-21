import os
import time
import tkinter as tk
import threading
import socket
import vlc
import pyaudio


dir_path = os.path.dirname(os.path.realpath(__file__))+'\\elec.ico'

dir_path_alarm = os.path.dirname(os.path.realpath(__file__))+'\\alarm.wav'

dir_path_waves = os.path.dirname(os.path.realpath(__file__))+'\\waves.wav'

a = vlc.MediaPlayer(dir_path_alarm)
b = vlc.MediaPlayer(dir_path_waves)

# a = vlc.MediaPlayer('alarm.wav')
# b = vlc.MediaPlayer('waves.wav')

main_root = tk.Tk()
main_root.title('Electors Receiver App')
main_root.iconbitmap(r'{}'.format(dir_path))
ip_var = tk.StringVar(master=main_root)
connect_to = tk.StringVar(master=main_root)
not_operating = False

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.p1 = StandbyPage(self)
        self.p2 = LivePage(self)
        self.p3 = EmergencyPage(self)
        self.p4 = BellPage(self)


        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        buttonframe.configure(background='gold')
        container.pack(side="top", fill="both", expand=True)

        self.p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.p1.configure(background='gold')
        self.p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.p2.configure(background='gold')
        self.p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.p3.configure(background='gold')
        self.p4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.p4.configure(background='gold')
        self.p1.show()

    def show_p1(self):
        self.p1.show()

    def show_p2(self):
        self.p2.show()

    def show_p3(self):
        self.p3.show()

    def show_p4(self):
        self.p4.show()




class StandbyPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        frame = tk.Frame(self, width=350, height=100, bg='gold')
        frame.pack(side='bottom')
        label = tk.Label(self, text="Standby Mode", fg='maroon',
                         bg='gold', width=20, font=('broadway', 25, 'bold'))
        label2 = tk.Label(master=frame, textvariable=ip_var, fg='blue', width=25, font=('verdana', 10))
        label3 = tk.Label(master=frame, textvariable=connect_to , bg='gold', width=45, font=('verdana', 12) )
        label.pack(side="top", fill="both", expand=True)
        label.place(x=5, y=100)
        label2.pack(side='bottom')
        label3.pack(side='top')
        


class LivePage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        label = tk.Label(self, text="Live Announcement", fg='maroon',
                         bg='gold', width=20, font=('broadway', 25, 'bold'))
        label.pack(side="top", fill="both", expand=True)
        label.place(x=5, y=100)


class EmergencyPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        label = tk.Label(self, text="Emergency Alarm", fg='maroon',
                         bg='gold', width=20, font=('broadway', 25, 'bold'))
        label.pack(side="top", fill="both", expand=True)
        label.place(x=5, y=100)


class BellPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        label = tk.Label(self, text="School Bell", fg='maroon',
                         bg='gold', width=20, font=('broadway', 25, 'bold'))
        label.pack(side="top", fill="both", expand=True)
        label.place(x=5, y=100)


class Speaker_Live(object):
    def __init__(self,ip = None, port = None):
        super(Speaker_Live, self).__init__()
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        chunks =1024
        self.format = FORMAT
        self.rate = RATE
        self.channels = CHANNELS
        self.chunks = chunks
        self.frames = []
        self.ip = ip
        if port is not None:
            self.port = int(port)
        self.address = (self.ip, self.port)
        self.resuming()
        self.initialize_speaker()


    def initialize_speaker(self):
        self.Audio = pyaudio.PyAudio()
        stream = self.Audio.open(format=self.format,
                            channels=self.channels,
                            rate=self.rate,
                            output=True,
                            frames_per_buffer=self.chunks,
                            )

        self.udpThread = threading.Thread(target=self.udpStream, daemon=True)
        self.AudioThread = threading.Thread(target=self.play, args=(stream,), daemon=True)
        self.udpThread.start()
        self.AudioThread.start()
        self.udpThread.join()
        self.AudioThread.join()
        
    def udpStream(self):
        global not_operating
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            udp.bind(self.address)
        except Exception as e:
            e
        udp.settimeout(4)
        while True:
            try:
                soundData ,addr = udp.recvfrom(self.chunks*self.channels*2)
                self.frames.append(soundData)
                if soundData !=b'':
                    self.resuming()
                else:
                    pass
            except Exception as e:
                e
                not_operating = True
                break
        udp.close()


    def play(self,stream):
        BUFFER = 10
        while True:
            if not_operating:
                break
            if len(self.frames) == BUFFER:
                while True:
                    try:
                        stream.write(self.frames.pop(0), self.chunks)
                    except:
                        break
        stream.stop_stream()
        stream.close()
        self.Audio.terminate()

    def resuming(self):
        global not_operating
        not_operating = False


class Controller(object):
    def __init__(self, host, port):
        super(Controller, self).__init__()
        self.root = main_root
        connect_to.set('Connect the Sender at IP Address:')
        str_port = str(port)
        ip_var.set(host+' : '+str_port)
        self.host = host
        self.port = port
        self.main = MainView(self.root)
        self.host = host
        self.port = port
        thread_1 = threading.Thread(target=self.recv_msg, daemon=True)
        thread_1.start()
        self.main.pack(side="top", fill="both", expand=True)
        self.root.geometry('477x253')
        self.root.mainloop()


    def recv_msg(self):
        i = 0
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen(5)
        conn, addr = s.accept()
        while True:
            try:
                connect_to.set('Connected')
                ip_var.set('Successfully!')
                data = conn.recv(4098)

                data1 = data.decode("ascii")
            except ConnectionResetError:
                data1 = 'stop'
                self.main.show_p1()
                break
            if data1 == 'live':
                a.stop()
                b.stop()
                self.main.show_p2()
                w = Speaker_Live(self.host,self.port)
            elif data1 == 'alarm':
                b.stop()
                self.main.show_p3()
                a.play()
            elif data1 == 'bell':
                a.stop()
                self.main.show_p4()
                b.play()
            elif data1 == 'stop':
                a.stop()
                b.stop()
                self.main.show_p1()
            if i > 300:
                break
            i += 1
        s.close()
        time.sleep(1)
        connect_to.set('Connect the Sender at IP Address:')
        ip_var.set(self.host+' : '+str(self.port))
        self.recv_msg()



if __name__ == "__main__":
    hostname = socket.gethostname()
    host = socket.gethostbyname(hostname)
    port = 50002
    Controller(host, port)

