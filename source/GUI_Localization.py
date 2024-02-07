import tkinter as tk
from PIL import Image, ImageTk

import datetime

class GUI_Localization:
    def __init__(self, root):
        self.root = root
        self.root.title("GUI Localization")

        # Simpan waktu pertama kali
        self. previous_iteration_time = datetime.datetime.now().timestamp()

        # Offset lapangan ketika layar gede
        self.field_offset_x = 235
        self.field_offset_x_temp = 0
        self.the_size_of_the_field_is_large = 0
        
        # Posisi ujung lapangan
        self.field_width_max_pos = 900
        self.field_height_max_pos = 600

        # Rasio ukuran lapangan
        self.width_ratio = 9
        self.height_ratio = 6

        # Rasio ukuran kotak penalti
        self.penalty_box_width_ratio = 1
        self.penalty_box_height_ratio = 5

        # Rasio ukuran gawang
        self.goal_depth_ratio = 0.6
        self.goal_height_ratio = 2.6

        # Rasio jarak titik pinalty ke gawang
        self.penalty_mark_dis_width_ratio = 2.1

        # Titik tengah
        self.centre_point_x = 0
        self.centre_point_y = 0
        self.zero_point_x = 0
        self.zero_point_y = 0

        # Data mentah
        self.raw_data = ["", "", "", "", ""]

        # Variabel Posisi Robot
        self.pos_robot_x = [0, 0, 0, 0, 0]
        self.pos_robot_y = [0, 0, 0, 0, 0]
        self.pos_robot_yaw = [0, 0, 0, 0, 0]
        self.pos_robot_pitch = [0, 0, 0, 0, 0]
        self.pos_robot_roll = [0, 0, 0, 0, 0]

        # Ball position for all robots
        self.ball_robot_x = [0, 0, 0, 0, 0]
        self.ball_robot_y = [0, 0, 0, 0, 0]

        # Variabel Strategi Robot
        self.strategy_robot = [0, 0, 0, 0, 0]
        self.play_robot = [0, 0, 0, 0, 0]
        self.role_robot = [0, 0, 0, 0, 0]
        self.pickup_robot = [0, 0, 0, 0, 0]
        self.release_robot = [0, 0, 0, 0, 0]

        # Variabel Bola Robot
        self.found_ball_robot = [0, 0, 0, 0, 0]
        self.nearest_robot = 0

        self.ball_coor_x = 0
        self.ball_coor_y = 0

        # Buat canvas
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Groupbox
        self.groupbox1 = tk.LabelFrame(self.root, text="Robot Pose", bg="white", padx=10, pady=10)
        self.groupbox2 = tk.LabelFrame(self.root, text="Robot Detail", bg="white", padx=10, pady=10)
        self.groupbox1.place(x=10, y=59, width=360, height=120)
        self.groupbox2.place(x=10, y=199, width=360, height=120)
        
        # Groupbox label
        self.groupbox1_label = tk.Label(self.groupbox1, text="", bg="white", anchor="nw", justify="left")
        self.groupbox2_label = tk.Label(self.groupbox2, text="", bg="white", anchor="nw", justify="left")  
        self.groupbox1_label.pack(fill="x", anchor="nw")
        self.groupbox2_label.pack(fill="x", anchor="nw")

        # Memindah Groupbox
        self.groupbox1.lower()
        self.groupbox2.lower()
        
        # Inisialisasi atribut lapangan
        self.field_x, self.field_y, self.field_width, self.field_height = self.calculate_field_size(900, 600)
        self.draw_soccer_field()

        # Mengikat fungsi on_resize ke peristiwa perubahan ukuran jendela
        self.root.bind("<Configure>", self.on_resize)
        
        
    def calculate_field_size(self, width, height):
        # Layar lebih lebar, ukuran lapangan disesuaikan dengan tinggi
        field_height = height * 0.8
        field_width = (height * 0.8) * (self.width_ratio / self.height_ratio)

        if width / height > self.width_ratio / self.height_ratio:
            # Menyatakan lapangannya berukuran besar
            self.the_size_of_the_field_is_large = 1

            # Memindah Groupbox
            self.groupbox1.lift()
            self.groupbox2.lift()
        else:
            # Menyatakan lapangannya berukuran kecil
            self.the_size_of_the_field_is_large = 0

            # Memindah Groupbox
            self.groupbox1.lower()
            self.groupbox2.lower()

        field_x = (width - field_width) * 0.5
        field_y = (height - field_height) * 0.5

        return field_x, field_y, field_width, field_height
    
    def draw_soccer_field(self):
        self.canvas.delete("all")  # Menghapus elemen-elemen sebelumnya

        # Menggambar latar hitam pada lapangan
        self.canvas.create_rectangle(
            self.field_x + self.field_offset_x_temp, self.field_y, self.field_x + self.field_offset_x_temp + self.field_width, self.field_y + self.field_height,
            fill="black", outline="black", width=12  # Menjadikan garis lebih tebal
        )

        # Menggambar lapangan hijau + Menggambar garis lapangan (tebal dan di atas garis putih)
        self.canvas.create_rectangle(
            self.field_x + self.field_offset_x_temp, self.field_y, self.field_x + self.field_offset_x_temp + self.field_width, self.field_y + self.field_height,
            fill="green", outline="white", width=4  # Menjadikan garis lebih tebal
        )
        
        # Menggambar garis tengah
        self.canvas.create_line(
            self.root.winfo_width() * 0.5  + self.field_offset_x_temp, self.field_y, self.root.winfo_width() * 0.5  + self.field_offset_x_temp, self.field_y + self.field_height,
            fill="white", width=4  # Menjadikan garis lebih tebal
        )

        # Menghitung ukuran lingkaran tengah relatif terhadap lebar lapangan
        circle_radius = min(self.field_width, self.field_height) * 0.135

        # Menggambar lingkaran tengah
        self.canvas.create_oval(
            self.root.winfo_width() * 0.5 - circle_radius + self.field_offset_x_temp, self.root.winfo_height() * 0.5 - circle_radius,
            self.root.winfo_width() * 0.5 + circle_radius + self.field_offset_x_temp, self.root.winfo_height() * 0.5 + circle_radius,
            outline="white", width=4  # Menjadikan garis lebih tebal
        )

        # Menghitung ukuran gawang relatif terhadap lebar lapangan
        goal_width = self.field_width * (self.goal_depth_ratio / self.width_ratio)
        goal_height = self.field_height * (self.goal_height_ratio / self.height_ratio)

        # Menggambar gawang kiri
        goal_x = self.field_x - goal_width
        goal_y = (self.root.winfo_height() - goal_height) * 0.5
        self.canvas.create_rectangle(
            goal_x + self.field_offset_x_temp, goal_y, goal_x  + self.field_offset_x_temp+ goal_width, goal_y + goal_height,
            outline="black", width=4  # Menjadikan garis lebih tebal
        )

        # Menggambar gawang kanan
        goal_x = self.field_x + self.field_width
        self.canvas.create_rectangle(
            goal_x + self.field_offset_x_temp, goal_y, goal_x + self.field_offset_x_temp + goal_width, goal_y + goal_height,
            outline="black", width=4  # Menjadikan garis lebih tebal
        )

        # Menghitung ukuran kotak penalti relatif terhadap lebar lapangan
        penalty_box_width = self.field_width * (self.penalty_box_width_ratio / self.width_ratio)
        penalty_box_height = self.field_height * (self.penalty_box_height_ratio / self.height_ratio)

        # Menggambar kotak penalti kiri
        penalty_box_x = self.field_x
        penalty_box_y = (self.root.winfo_height() - penalty_box_height) * 0.5
        self.canvas.create_rectangle(
            penalty_box_x + self.field_offset_x_temp, penalty_box_y, penalty_box_x + self.field_offset_x_temp + penalty_box_width, penalty_box_y + penalty_box_height,
            outline="white", width=4  # Menjadikan garis lebih tebal
        )

        # Menggambar kotak penalti kanan
        penalty_box_x = self.field_x + self.field_width - penalty_box_width
        self.canvas.create_rectangle(
            penalty_box_x + self.field_offset_x_temp, penalty_box_y, penalty_box_x + self.field_offset_x_temp + penalty_box_width, penalty_box_y + penalty_box_height,
            outline="white", width=4  # Menjadikan garis lebih tebal
        )
        
        # Menggambar garis-garis hitam untuk kotak-kotak persegi di dalam lapangan
        num_rows = 6
        num_cols = 9
        square_size_x = self.field_width / num_cols
        square_size_y = self.field_height / num_rows
        for i in range(num_rows):
            for j in range(num_cols):
                x1 = self.field_x + j * square_size_x
                y1 = self.field_y + i * square_size_y
                x2 = x1 + square_size_x
                y2 = y1 + square_size_y
                self.canvas.create_rectangle(x1 + self.field_offset_x_temp, y1, x2 + self.field_offset_x_temp, y2, outline="black")
        
        # Menghitung titik pinalty antara lingkaran tengah dan kotak penalti
        corner_x_right = self.root.winfo_width() * 0.5 + self.field_width * 0.5 - self.field_width * (self.penalty_mark_dis_width_ratio / self.width_ratio)
        corner_x_left = self.root.winfo_width() * 0.5 - self.field_width * 0.5 + self.field_width * (self.penalty_mark_dis_width_ratio / self.width_ratio)
        corner_x = self.root.winfo_width() * 0.5
        corner_y = self.root.winfo_height() * 0.5

        # Menggambar titik pinalty
        self.canvas.create_oval(
            corner_x_right - 4 + self.field_offset_x_temp, corner_y - 4, corner_x_right + 4 + self.field_offset_x_temp, corner_y + 4,
            outline="white", fill="white"
        )
        self.canvas.create_oval(
            corner_x_left - 4 + self.field_offset_x_temp, corner_y - 4, corner_x_left + 4 + self.field_offset_x_temp, corner_y + 4,
            outline="white", fill="white"
        )

        # Gambar bola
        # image = Image.open("ball.png")
        # photo = ImageTk.PhotoImage(image)
        # self.ball = self.canvas.create_image(200, 200, image=photo)
        
        # Membuat bola
        self.ball_2 = self.canvas.create_text(-10, -10, text="•", fill="black", font=("Arial", int(0.095 * self.field_width), "bold")) # 0.015

        # Membuat text sebagai mark robot berada
        self.centre_point_x = self.root.winfo_width() * 0.5
        self.centre_point_y = self.root.winfo_height() * 0.5

        self.zero_point_x = self.centre_point_x - self.field_width * 0.5
        self.zero_point_y = self.centre_point_y - self.field_height * 0.5
        
        self.robot_1_pos = self.canvas.create_text(-10, -10, text="1<", fill="black", font=("Arial", int(0.035 * self.field_width), "bold")) # 0.015
        self.robot_2_pos = self.canvas.create_text(-10, -10, text="2<", fill="black", font=("Arial", int(0.035 * self.field_width), "bold")) # 0.015
        self.robot_3_pos = self.canvas.create_text(-10, -10, text="3<", fill="black", font=("Arial", int(0.035 * self.field_width), "bold")) # 0.015
        self.robot_4_pos = self.canvas.create_text(-10, -10, text="4<", fill="black", font=("Arial", int(0.035 * self.field_width), "bold")) # 0.015
        self.robot_5_pos = self.canvas.create_text(-10, -10, text="5<", fill="black", font=("Arial", int(0.035 * self.field_width), "bold")) # 0.015

        # Membuat kotak text
        self.raw_data_text = self.canvas.create_text(200, 200, text="", anchor="nw", font=("Arial", 8))

    def update_text(self):
        self.canvas.coords(self.raw_data_text, 10 + (int(not self.the_size_of_the_field_is_large) * -1000), 10 + (int(not self.the_size_of_the_field_is_large) * -1000))

        # Format waktu untuk menampilkan jam, menit, detik, dan mikrodetik
        time =  datetime.datetime.now()
        formatted_time =time.strftime("%H:%M:%S:%f")

        # Menampikan waktu iterasi
        now = time.timestamp()
        iteration_time = now - self. previous_iteration_time
        self. previous_iteration_time = now

        # Detail data Robot
        detail_data_1, detail_data_2 = "", ""

        for i in range(0, 5):
            detail_data_1 = detail_data_1 + str(i+1) + ": x: " + str(self.pos_robot_x[i]) + ", y: " + str(self.pos_robot_y[i]) + ", yaw: " + str(self.pos_robot_yaw[i]) + "\n"
            detail_data_2 = detail_data_2 + str(i+1) + ": Role: " + str(self.role_robot[i]) + ", Found Ball: " + str(self.found_ball_robot[i]) + ", Strategy: " + str(self.strategy_robot[i]) + ", Pickup: " + str(self.pickup_robot[0]) + "\n"

        iter_data = "=== Updated: " + formatted_time + ", Iteration Time: " + str(iteration_time) + " ===\nSee terminal when data is not updated!\n"
        
        """
        detail_data = "\n\n=== Detail Data ====\n" + detail_data_1 + detail_data_2 + "\n\n=== Ball Data ====\nx: " + str(self.ball_coor_x) + ", y: " + str(self.ball_coor_y)  + ", Nearest Robot: " + str(self.nearest_robot)
        raw_data = "\n=== Raw Data ===\nRobot 1:\n" + str(self.raw_data[0]) + "\nRobot 2:\n" + str(self.raw_data[1]) + "\nRobot 3:\n" + str(self.raw_data[2]) + "\nRobot 4:\n" + str(self.raw_data[3]) + "\nRobot 5:\n" + str(self.raw_data[4])
        
        self.canvas.itemconfigure(self.raw_data_text, text=iter_data+raw_data+detail_data)  # Mengubah isi teks objek teks
        """

        self.canvas.itemconfigure(self.raw_data_text, text=iter_data)  # Mengubah isi teks objek teks
        self.groupbox1_label.config(text=detail_data_1) # txt groupbox 1
        self.groupbox2_label.config(text=detail_data_2) # txt groupbox 2

        # self.raw_data_text.lift()

    def update_robot_1_pos(self, pos_x, pos_y, pos_yaw):
        multiplier = self.field_width / 1000
        pos_x = self.zero_point_x + pos_x * multiplier * 1000 / self.field_width_max_pos
        pos_y = self.zero_point_y + pos_y * multiplier * 665 / self.field_height_max_pos

        self.canvas.coords(self.robot_1_pos, pos_x + self.field_offset_x_temp, pos_y)
        self.canvas.itemconfigure(self.robot_1_pos, angle=pos_yaw)

    def update_robot_2_pos(self, pos_x, pos_y, pos_yaw):
        multiplier = self.field_width / 1000
        pos_x = self.zero_point_x + pos_x * multiplier * 1000 / self.field_width_max_pos
        pos_y = self.zero_point_y + pos_y * multiplier * 665 / self.field_height_max_pos

        self.canvas.coords(self.robot_2_pos, pos_x + self.field_offset_x_temp, pos_y)
        self.canvas.itemconfigure(self.robot_2_pos, angle=pos_yaw)

    def update_robot_3_pos(self, pos_x, pos_y, pos_yaw):
        multiplier = self.field_width / 1000
        pos_x = self.zero_point_x + pos_x * multiplier * 1000 / self.field_width_max_pos
        pos_y = self.zero_point_y + pos_y * multiplier * 665 / self.field_height_max_pos

        self.canvas.coords(self.robot_3_pos, pos_x + self.field_offset_x_temp, pos_y)
        self.canvas.itemconfigure(self.robot_3_pos, angle=pos_yaw)

    def update_robot_4_pos(self, pos_x, pos_y, pos_yaw):
        multiplier = self.field_width / 1000
        pos_x = self.zero_point_x + pos_x * multiplier * 1000 / self.field_width_max_pos
        pos_y = self.zero_point_y + pos_y * multiplier * 665 / self.field_height_max_pos

        self.canvas.coords(self.robot_4_pos, pos_x + self.field_offset_x_temp, pos_y)
        self.canvas.itemconfigure(self.robot_4_pos, angle=pos_yaw)

    def update_robot_5_pos(self, pos_x, pos_y, pos_yaw):
        multiplier = self.field_width / 1000
        pos_x = self.zero_point_x + pos_x * multiplier * 1000 / self.field_width_max_pos
        pos_y = self.zero_point_y + pos_y * multiplier * 665 / self.field_height_max_pos

        self.canvas.coords(self.robot_5_pos, pos_x + self.field_offset_x_temp, pos_y)
        self.canvas.itemconfigure(self.robot_5_pos, angle=pos_yaw)

    def update_ball_pos(self, pos_x, pos_y):
        multiplier = self.field_width / 1000
        pos_x = self.zero_point_x + pos_x * multiplier * 1000 / self.field_width_max_pos
        pos_y = self.zero_point_y + pos_y * multiplier * 665 / self.field_height_max_pos

        # self.canvas.coords(self.ball, pos_x + self.field_offset_x_temp, pos_y)
        self.canvas.coords(self.ball_2, pos_x + self.field_offset_x_temp, pos_y)
    
    def on_resize(self, event):
        # Ubah nilai offset lapangan
        self.field_offset_x_temp = int(self.field_offset_x * self.field_width / 1000) * self.the_size_of_the_field_is_large

        self.field_x, self.field_y, self.field_width, self.field_height = self.calculate_field_size(event.width, event.height)
        self.draw_soccer_field()

        centre_point_x = self.root.winfo_width() * 0.5
        centre_point_y = self.root.winfo_height() * 0.5

        zero_point_x = centre_point_x - self.field_width * 0.5
        zero_point_y = centre_point_y - self.field_height * 0.5

    def update_localization_data(self):
        # Update posisi robot ke GUI
        self.update_robot_1_pos(self.pos_robot_x[0], self.pos_robot_y[0], self.pos_robot_yaw[0])
        self.update_robot_2_pos(self.pos_robot_x[1], self.pos_robot_y[1], self.pos_robot_yaw[1])
        self.update_robot_3_pos(self.pos_robot_x[2], self.pos_robot_y[2], self.pos_robot_yaw[2])
        self.update_robot_4_pos(self.pos_robot_x[3], self.pos_robot_y[3], self.pos_robot_yaw[3])
        self.update_robot_5_pos(self.pos_robot_x[4], self.pos_robot_y[4], self.pos_robot_yaw[4])

        # Update text GUI
        self.update_text()

        # Update posisi bila
        self.update_ball_pos(self.ball_coor_x, self.ball_coor_y)
