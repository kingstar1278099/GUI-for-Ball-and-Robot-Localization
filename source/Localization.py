import tkinter as tk

import zmq
import json

class Localization:
    def __init__(self, root):
        self.root = root
        self.root.title("Set address")
        # self.root.geometry("300x90")  # Mengatur ukuran jendela

        # Menonaktifkan kemampuan merubah ukuran jendela
        self.root.resizable(False, False)

        # Data mentah
        self.raw_data = [0, 0, 0, 0, 0]

        # Variabel Posisi Robot
        self.pos_robot_x = [0, 0, 0, 0, 0]
        self.pos_robot_y = [0, 0, 0, 0, 0]
        self.pos_robot_yaw = [0, 0, 0, 0, 0]

        # Ball position for all robots
        self.ball_robot_x = [0, 0, 0, 0, 0]
        self.ball_robot_y = [0, 0, 0, 0, 0]

        # Variabel Strategi Robot
        self.strategy_robot = [0, 0, 0, 0, 0]
        self.play_robot = [0, 0, 0, 0, 0]
        self.role_robot = [0, 0, 0, 0, 0]
        self.pickup_robot = [0, 0, 0, 0, 0]

        # Variabel Bola Robot
        self.found_ball_robot = [0, 0, 0, 0, 0]
        self.nearest_robot = 0

        self.ball_coor_x = 0
        self.ball_coor_y = 0

        # ZeroMQ handler
        self.context = zmq.Context()

        self.s0 = tk.StringVar()
        self.s1 = tk.StringVar()
        self.s2 = tk.StringVar()
        self.s3 = tk.StringVar()

        # # local
        self.s0.set("tcp://127.0.0.1:5555")
        self.s1.set("tcp://127.0.0.1:5556")
        self.s2.set("tcp://127.0.0.1:5557")
        self.s3.set("tcp://127.0.0.1:5558")

        # # # Socket to talk to server
        # self.s0.set("tcp://192.168.5.101:5555")
        # self.s1.set("tcp://192.168.5.102:5555")
        # self.s2.set("tcp://192.168.5.103:5555")
        # self.s3.set("tcp://192.168.5.104:5555")

        # Tambahkan teks ke kotak teks
        # self.text.insert("2.0", "Done!\n")

        # # Buat teks seperti terminal
        # self.text = tk.Text(root, height=4, width=40)
        # self.text.pack()

        self.s0_entry = tk.Entry(root, textvariable=self.s0, font=("Helvetica", 12), width=20)  # Set the width to 20 characters
        self.s0_entry.pack()
        self.s1_entry = tk.Entry(root, textvariable=self.s1, font=("Helvetica", 12), width=20)  # Set the width to 20 characters
        self.s1_entry.pack()
        self.s2_entry = tk.Entry(root, textvariable=self.s2, font=("Helvetica", 12), width=20)  # Set the width to 20 characters
        self.s2_entry.pack()
        self.s3_entry = tk.Entry(root, textvariable=self.s3, font=("Helvetica", 12), width=20)  # Set the width to 20 characters
        self.s3_entry.pack()

        # Tampilkan tombol Mulai
        self.start_button = tk.Button(self.root, text="Start", command=self.start_)
        self.start_button.pack()

        # Loop app
        root.mainloop()

    def start_(self):
        # Connecting
        self.socket0 = self.context.socket(zmq.REQ)
        self.socket0.connect(self.s0.get())
        self.socket1 = self.context.socket(zmq.REQ)
        self.socket1.connect(self.s1.get())
        self.socket2 = self.context.socket(zmq.REQ)
        self.socket2.connect(self.s2.get())
        self.socket3 = self.context.socket(zmq.REQ)
        self.socket3.connect(self.s3.get())

        # Menutup aplikasi
        self.root.destroy()

    def loop_collect_data(self):
        print("loop_collect_data...")

        #### Robot 1
        print("request...")
        print(self.s0.get())
        self.socket0.send_string("Request")
        message0 = self.socket0.recv_string()
        print("request done...")

        # Deserialize the data
        data0 = json.loads(message0)
        self.pos_robot_x[0] = data0['a']
        self.pos_robot_y[0] = data0['b']
        self.found_ball_robot[0] = int(data0['c'])
        self.ball_robot_x[0] = int(data0['d'])
        self.pickup_robot[0] = data0['e']
        self.play_robot[0] = data0['f']
        self.pos_robot_yaw[0] = data0['g']
        self.strategy_robot[0] = data0['h']
        self.role_robot[0] = data0['i']
        self.ball_robot_y[0] = int(data0['z'])

        # Print the data
        print("Received Robot 1: ", data0)
        # Save the data
        self.raw_data[0] = data0

        #### Robot 2
        print("request...")
        print(self.s1.get())
        self.socket1.send_string("Request")
        message1 = self.socket1.recv_string()
        print("request done...")

        # Deserialize the data
        data1 = json.loads(message1)
        self.pos_robot_x[1] = data1['a']
        self.pos_robot_y[1] = data1['b']
        self.found_ball_robot[1] = int(data1['c'])
        self.ball_robot_x[1] = int(data1['d'])
        self.pickup_robot[1] = data1['e']
        self.play_robot[1] = data1['f']
        self.pos_robot_yaw[1] = data1['g']
        self.strategy_robot[1] = data1['h']
        self.role_robot[1] = data1['i']
        self.ball_robot_y[1] = int(data1['z'])

        # Print the data
        print("Received Robot 2: ", data1)
        # Save the data
        self.raw_data[1] = data1

        #### Robot 3
        print("request...")
        print(self.s2.get())
        self.socket2.send_string("Request")
        message2 = self.socket2.recv_string()
        print("request done...")

        # Deserialize the data
        data2 = json.loads(message2)
        self.pos_robot_x[2] = data2['a']
        self.pos_robot_y[2] = data2['b']
        self.found_ball_robot[2] = int(data2['c'])
        self.ball_robot_x[2] = int(data2['d'])
        self.pickup_robot[2] = data2['e']
        self.play_robot[2] = data2['f']
        self.pos_robot_yaw[2] = data2['g']
        self.strategy_3 = data2['h']
        self.role_robot[2] = data2['i']
        self.ball_robot_y[2] = int(data2['z'])

        # Print the data
        print("Received Robot 3: ", data2)
        # Save the data
        self.raw_data[2] = data2

        #### Robot 4
        print("request...")
        print(self.s3.get())
        self.socket3.send_string("Request")
        message3 = self.socket3.recv_string()
        print("request done...")

        # Deserialize the data
        data3 = json.loads(message3)
        self.pos_robot_x[3] = data3['a']
        self.pos_robot_y[3] = data3['b']
        self.found_ball_robot[3] = int(data3['c'])
        self.ball_robot_x[3] = int(data3['d'])
        self.pickup_robot[3] = data3['e']
        self.play_robot[3] = data3['f']
        self.pos_robot_yaw[3] = data3['g']
        self.strategy_4 = data3['h']
        self.role_robot[3] = data3['i']
        self.ball_robot_y[3] = int(data3['z'])

        # Print the data
        print("Received Robot 4: ", data3)
        # Save the data
        self.raw_data[3] = data3

    def loop(self, app):
        print("loop...")

        # Data
        data_robot = {}

        if self.found_ball_robot[0] != 999:
            data_robot["Robot1"] = {"Jarak": self.found_ball_robot[0], "ball_x": self.ball_robot_x[0], "ball_y": self.ball_robot_y[0]}

        if self.found_ball_robot[1] != 999:
            data_robot["Robot2"] = {"Jarak": self.found_ball_robot[1], "ball_x": self.ball_robot_x[1], "ball_y": self.ball_robot_y[1]}

        if self.found_ball_robot[2] != 999:
            data_robot["Robot3"] = {"Jarak": self.found_ball_robot[2], "ball_x": self.ball_robot_x[2], "ball_y": self.ball_robot_y[2]}

        if self.found_ball_robot[3] != 999:
            data_robot["Robot4"] = {"Jarak": self.found_ball_robot[3], "ball_x": self.ball_robot_x[3], "ball_y": self.ball_robot_y[3]}

        print(data_robot)

        # Mencari robot dengan jarak terdekat jika data_robot tidak kosong
        if data_robot:
            nama_robot_terdekat = min(data_robot, key=lambda x: data_robot[x]["Jarak"])

            # Mengambil data ball_x dan ball_y dari robot terdekat
            ball_x = data_robot[nama_robot_terdekat]["ball_x"]
            ball_y = data_robot[nama_robot_terdekat]["ball_y"]

            print(f"Robot dengan jarak terdekat adalah {nama_robot_terdekat} dengan jarak {data_robot[nama_robot_terdekat]['Jarak']}")
            print(f"Data ball_x: {ball_x}, Data ball_y: {ball_y}") 
        else:
            print("Semua robot tidak mendeteksi bola.")
        
        data_robot = {
            "Robot1": {"Jarak": self.found_ball_robot[0], "ball_x": self.ball_robot_x[0], "ball_y": self.ball_robot_y[0]},
            "Robot2": {"Jarak": self.found_ball_robot[1], "ball_x": self.ball_robot_x[1], "ball_y": self.ball_robot_y[1]},
            "Robot3": {"Jarak": self.found_ball_robot[2], "ball_x": self.ball_robot_x[2], "ball_y": self.ball_robot_y[2]},
            "Robot4": {"Jarak": self.found_ball_robot[3], "ball_x": self.ball_robot_x[3], "ball_y": self.ball_robot_y[3]},
        }

        nama_robot_terdekat = min(data_robot, key=lambda x: data_robot[x]["Jarak"])

        # Mengambil data ball_x dan ball_y dari robot terdekat
        ball_x = data_robot[nama_robot_terdekat]["ball_x"]
        ball_y = data_robot[nama_robot_terdekat]["ball_y"]


        self.nearest_robot = nama_robot_terdekat

        self.ball_coor_x, self.ball_coor_y = ball_x, ball_y
        print("Ball X = ", ball_x, "Ball_Y", ball_y)

        # Update data to GUI
        app.pos_robot_x = self.pos_robot_x
        app.pos_robot_y = self.pos_robot_y
        app.pos_robot_yaw = self.pos_robot_yaw

        app.ball_robot_x = self.ball_robot_x
        app.ball_robot_y = self.ball_robot_y

        app.strategy_robot = self.strategy_robot
        app.play_robot = self.play_robot
        app.role_robot = self.role_robot
        app.pickup_robot = self.pickup_robot

        app.found_ball_robot = self.found_ball_robot

        app.ball_coor_x = self.ball_coor_x
        app.ball_coor_y = self.ball_coor_y

        app.nearest_robot = self.nearest_robot

        app.raw_data = self.raw_data