import zmq
import json
import time

# Endpoint
endpoint = "tcp://127.0.0.1:5557"

# Inisialisasi 0MQ context
context = zmq.Context()

print("Server is running...", endpoint)

# Membuat soket tipe 'reply'
socket = context.socket(zmq.REP)

# Bind ke soket
socket.bind(endpoint)

while True:
    # Menerima pesan
    incoming_message = socket.recv()

    # Persiapan data
    robot_1_PosX = 700
    robot_1_PosY = 250
    robot_1_strategy = 0
    ball_x = 50
    ball_y = 0
    pickup_1 = True
    play_1 = False
    jarak = -1
    yaw = 115

    data = {
        "a": robot_1_PosX,
        "b": robot_1_PosY,
        "c": jarak,
        "d": ball_x,
        "e": pickup_1,
        "f": play_1,
        "g": yaw,
        "h": "",
        "i": "",
        "z": ball_y
    }

    message = json.dumps(data)

    # Kirim balasan
    socket.send(message.encode())

    print("Sent:", message)

    # Lakukan 'pekerjaan'
    time.sleep(1)
