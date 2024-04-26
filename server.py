import socket
from _thread import *
import sys
import random

server_ip = "172.28.1.81"
server_port = 36695
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server_socket.bind((server_ip, server_port))
except Exception as e:
    print("Failed to bind socket:", e)
    sys.exit()

server_socket.listen(30)
print("Waiting for a connection")
current_id = "0"
positions = ["0:50,50", "1:100,100"]

def threaded_client(conn):
    global current_id, positions
    conn.sendall(str.encode(current_id))
    current_id = "1"
    while True:
        try:
            data = conn.recv(2048)
            if not data:
                print("Client disconnected")
                break
            else:
                message = data.decode('utf-8')
                print("Received:", message)

                if message == "generate_obstacles":
                    gap_y = random.randint(100, 400)
                    x = random.randint(200, 600)
                    reply = f"{gap_y}:{x}"
                    print("Generated obstacle data:", reply)
                    conn.sendall(str.encode(reply))
                elif message == "check_collision":
                    reply = "collision"
                    conn.sendall(str.encode(reply))
                elif message == "update_score":
                    reply = "increment_score"
                    conn.sendall(str.encode(reply))
                else:
                    print("Invalid message:", message)
                    conn.sendall(str.encode("Invalid message"))

        except socket.error as e:
            print("Socket error:", e)
            break
        except Exception as ex:
            print("Error:", ex)
            break

    print("Connection closed")
    conn.close()

while True:
    conn, addr = server_socket.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn,))
