
from methods import *

def run(port, host="127.0.0.1"):
        server = socket(AF_INET, SOCK_STREAM)
        server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(20)
        print("Server listening at", server.getsockname())
        All_Threads = []
        while True:        
                conn, addr = server.accept()
                print("Connected by", addr)
                thread = threading.Thread(target = manageconnection, args = [conn])
                thread.start()
                All_Threads.append(thread)

def manageconnection(conn):
        data = conn.recv(1024).decode()
        print(data)
        response, file, headers = handle_request(data)
        conn.sendall(response.encode())
        if file:
                try:
                        with open (file, 'rb') as f:
                                if(IsGzipEncoded(headers)):
                                        conn.sendall(gzip.compress(f.read()))
                                else:
                                        conn.sendfile(f)
                except:
                        pass
        conn.close()

def handle_request(data):
        data = data.split("\r\n")
        Error=False
        try:
                method,filename,version=data[0].split()
                if(version.split('/')[0]!='HTTP'):
                        Error=True
        except:
                Error=True
        headers={}
        index=0
        for i,line in enumerate(data[1:]):
                index=i
                if not line.strip("\r\n"):
                        break
                try:
                        FName,Fvalue = line.split(":",1)
                        headers[FName.lower()]=Fvalue
                except:
                        Error=True
                        break
        temp=data[index+2:]
        fileData=''
        for i in temp:
                fileData+=f"{i}\r\n"
        
        if Error or 'host' not in headers:
                response_code = 400
                response, file = handleError(response_code)
        
        else:
                if(method=="GET"):
                        response, file = getMethod(filename,headers)
                elif(method=="POST"):
                        response, file = postMethod(fileData)
                elif(method=="DELETE"):
                        print("hereee")
                        response, file = deleteMethod(filename)
                elif(method=="HEAD"):
                        response, file = headMethod(filename,headers)
                elif(method=="PUT"):
                        response, file = putMethod(filename,fileData)

        print(type(response))
        if(type(response)==int):
                print("Here you go")
                response, file = handleError(response)

        return response, file, headers

if __name__ == "__main__":
        port=int(sys.argv[1])
        run(port)
