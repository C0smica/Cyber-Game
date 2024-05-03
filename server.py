import socket
from _thread import *
import sys
import random
import time

server_ip = "172.28.3.71"
server_port = 36695
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server_socket.bind((server_ip, server_port))
except Exception as e:
    print("Failed to bind socket:", e)
    sys.exit()

server_socket.listen(30)
print("Waiting for connections")

current_id = 0
positions = [(0, 50, 50), (1, 100, 100)]  # Player positions

# Dictionary to store connection attempts and timestamps for each client IP
connection_attempts = {}

def threaded_client(conn, player_id):
    global positions
    conn.sendall(str.encode(str(player_id)))  # Send player ID to client
    while True:
        try:
            data = conn.recv(2048)
            if not data:
                print("Player", player_id, "disconnected")
                break
            else:
                message = data.decode('utf-8')
                print("Player", player_id, "sent:", message)

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

        except (socket.error, ConnectionResetError) as e:
            print("Player", player_id, "disconnected:", e)
            break
        except Exception as ex:
            print("Error:", ex)
            break

    print("Player", player_id, "connection closed")
    conn.close()

def check_connection_attempts(ip):
    # Check if the IP has exceeded the maximum connection attempts within a time frame
    timestamp = time.time()
    if ip in connection_attempts:
        attempts, last_attempt_time = connection_attempts[ip]
        if timestamp - last_attempt_time < 60:  # Time frame (60 seconds)
            if attempts >= 3:  # Maximum connection attempts within the time frame
                print("Blocked IP:", ip)
                return True
            else:
                connection_attempts[ip] = (attempts + 1, timestamp)
                return False
        else:
            connection_attempts[ip] = (1, timestamp)
            return False
    else:
        connection_attempts[ip] = (1, timestamp)
        return False

clients = []

while True:
    try:
        conn, addr = server_socket.accept()
        print("Connected to:", addr)
        
        ip = addr[0]
        if not check_connection_attempts(ip):
            if len(clients) < 30:
                clients.append(conn)
                start_new_thread(threaded_client, (conn, current_id))
                current_id += 1
            else:
                print("Server full. Connection rejected.")
                conn.sendall(str.encode("Server full."))
                conn.close()
        else:
            conn.sendall(str.encode("Too many connection attempts."))
            conn.close()

    except Exception as e:
        print("Connection error:", e)
        # Continue accepting new connections even if an error occurs
