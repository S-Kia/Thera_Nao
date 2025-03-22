import connection

#physical robot
# NAO_IP = ""
# PORT = 9559

#virutal robot
NAO_IP = "127.0.0.1"
PORT = 65170

#connecting and activating NAO
connection.connect(NAO_IP,PORT)

#disconnect and exit NAO
# connection.disconnect(NAO_IP, PORT)
