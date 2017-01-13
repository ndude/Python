# The folowing script SSH to a dives and ad a description to the Eth 1/3 interface.
# You need to manually enter an IP address of the device you want to configure.

import paramiko
import time

ip = raw_input("IP address: ")
username = "cisco"
password = "cisco"

remote_conn_pre=paramiko.SSHClient()
remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
remote_conn_pre.connect(ip, port=22, username=username,
                        password=password,
                        look_for_keys=False, allow_agent=False)

remote_conn = remote_conn_pre.invoke_shell()
output = remote_conn.recv(65535)
print output

cmds = ["conf t", "interface Ethernet 1/3", "descr \"Test number 1 python\"",
 "exit", "exit", "wr mem"]

for cmd in cmds:
    remote_conn.send(cmd+"\n")
    time.sleep(.5)
    output = remote_conn.recv(65535)
    print output
