import socket
import sys
import subprocess
import re


for i in sys.argv[1:]:
    print(i)
    f = open(i,"r");

    index = 0;

    HOST = ""
    PORT = 25

    s1 = ""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        for line in f:
            if(index==0):
                s1 = line.split()[-1];
            elif(index==1):
                s2 = line.split()[-1];
                mail_domain = re.search("@.*",s2).start()
                mail_domain = s2[mail_domain+1:-1]
                proc = subprocess.run(['host', '-t', 'mx',mail_domain], encoding='utf-8', stdout=subprocess.PIPE)
                HOST = proc.stdout.split('\n')[0].split()[-1].replace('com.','com')
                s.connect((HOST, PORT))
                data = s.recv(1024)
                data = data.decode();
                print("S :",data)
                s.send('HELO Alice\r\n'.encode())
                print("C : HELO Alice\r\n")
                data = s.recv(1024)
                data = data.decode();
                print("S :",data)
                msg = "MAIL FROM:"+s1+"\r\n"
                s.send(msg.encode())
                print("C: "+msg)
                data = s.recv(1024)
                data = data.decode();
                print("S :",data)
                msg = "RCPT TO:"+s2+"\r\n"
                s.send(msg.encode())
                print("C : RCPT TO:"+s2+"\r\n")
                data = s.recv(1024)
                data = data.decode();
                print("S :",data)
                s.send("DATA\r\n".encode())
                print("C : DATA\r\n")
                data = s.recv(1024)
                data = data.decode();
                print("S :",data)
            else:
                s1 = line
                s.send(s1.encode())
                print("C :",s1);
            index = index + 1
        s.send(".\r\n".encode())
        print("C : .\r\n")
        data = s.recv(1024)
        data = data.decode();

        print("S :",data)
        s.send("QUIT\r\n".encode())
        print("C : QUIT\r\n")
        data = s.recv(1024)
        data = data.decode();

        s.close()
