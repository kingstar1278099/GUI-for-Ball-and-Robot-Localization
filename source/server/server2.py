import zmq
import json
import time

# Endpoint
endpoint = "tcp://127.0.0.1:5556"

# Initialize the 0MQ context
context = zmq.Context()

print("Server is running...", endpoint)

# Generate a reply socket
socket = context.socket(zmq.REP)
socket.bind(endpoint)

while True:
    # Receive the message
    message = socket.recv()

    # Prepare data
    robot_1_PosX, robot_1_PosY, robot_1_strategy = 400, 380, 0
    yaw = 90
    ball_x, ball_y = 50, 100
    pickup_1, play_1 = True, False
    jarak = -1

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

    # Send reply
    socket.send_string(message)
    print("Sent:", message)

    # Do some 'work'
    time.sleep(1)
