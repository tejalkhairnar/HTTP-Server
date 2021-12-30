from utility import *
from modules import *

def handleError( error_code):
        message = ''
        message += f"HTTP/1.1 {error_code} {status[error_code]}\r\n"
        message += f"Date : {time.strftime('%a, %d %b %Y %I:%M:%S', time.gmtime())} GMT\r\n"
        for content in headers:
                message += f"{content}: {headers[content]}\r\n"
        res_file = res_dir + '/' + str(error_code) + '.html'
        print(res_file)
        with open(res_file) as res_f:
                response_body = res_f.read()
        message += '\r\n'
        message += response_body
        print(message)
        return message, None

def headMethod(filename,headers):
        more_headers = {}
        filename=filename.strip("/")
        if(not os.path.isfile(filename)):
                filename=None
        if filename == None:
                return 404,None
        else:
                fileInfo = os.stat(filename)
                fileSize = fileInfo.st_size
                contentType = mimetypes.guess_type(filename)[0]
                lastModified = getLastModifiedTime(fileInfo)
                accept_ranges = 'bytes'
                _, file = response_body(filename)
                if(file and IsGzipEncoded(headers)):
                        more_headers['Content-Encoding'] = 'gzip'  
                more_headers['Content-Length'] = fileSize
                more_headers['Last-Modified'] = lastModified
                more_headers['Content-Type'] = contentType
                more_headers['Accept-Ranges'] = accept_ranges
                message = ""
                message += f"HTTP/1.1 {200} {status[200]}\r\n"
                message+=f"Date: {time.strftime('%a, %d %b %Y %I:%M:%S', time.gmtime())} GMT\r\n"
                for h in headers:
                        message+=f"{h}: {headers[h]}\r\n"

                for h in more_headers:
                        message+=f"{h}: {more_headers[h]}\r\n"
                message += "\r\n"
                return message, file

def getMethod(filename,headers):
        more_headers = {}
        filename=filename.strip("/")
        if(not os.path.isfile(filename)):
                filename=None
        if filename == None:
                return 404,None
        else:
                fileInfo = os.stat(filename)
                contentType = mimetypes.guess_type(filename)[0]
                lastModified = getLastModifiedTime(fileInfo)
                fileSize = fileInfo.st_size
                acceptRanges = 'bytes'
                response_bd, file = response_body(filename)
                if(file and IsGzipEncoded(headers)):
                        more_headers['Content-Encoding'] = 'gzip'  
                more_headers['Content-Length'] = fileSize
                more_headers['Last-Modified'] = lastModified
                more_headers['Content-Type'] = contentType
                more_headers['Accept-Ranges'] = acceptRanges
                message = ""
                message += f"HTTP/1.1 {200} {status[200]}\r\n"
                message+=f"Date: {time.strftime('%a, %d %b %Y %I:%M:%S', time.gmtime())} GMT\r\n"
                for h in headers:
                        message+=f"{h}: {headers[h]}\r\n"

                for h in more_headers:
                        message+=f"{h}: {more_headers[h]}\r\n"
                message += "\r\n"
                message += response_bd
                return message, file
    
def postMethod(fileData):
        accept_range = 'bytes'
        more_headers = {}
        more_headers['Accept-Ranges'] = accept_range
        message = ""
        message += f"HTTP/1.1 {200} {status[200]}\r\n"
        message += f"Date: {time.strftime('%a, %d %b %Y %I:%M:%S', time.gmtime())} GMT\r\n"
        for h in headers:
                message+=f"{h}: {headers[h]}\r\n"
        for h in more_headers:
                message+=f"{h}: {more_headers[h]}\r\n"
        message += "\r\n"
        print(fileData)
        return message, None


def deleteMethod( filename):
        filename=filename.strip("/")
        if(not os.path.isfile(filename)):
                filename=None
        if filename == None:
                return 404,None
        filename = filename.replace("/", "", 1)
        isFile = os.path.isfile(filename)
        if(isFile == False):
                return 400, None
        os.remove(filename)
        message = ""
        message += f"HTTP/1.1 {200} {status[200]}\r\n"
        message+=f"Date: {time.strftime('%a, %d %b %Y %I:%M:%S', time.gmtime())} GMT\r\n"
        for h in headers:
                message+=f"{h}: {headers[h]}\r\n"
        message += "\r\n"
        res_file = res_dir + '/' + 'deleted.html'
        with open(res_file) as f:
                message += f.read()
        print(message)
        return message, None

def putMethod(filenamnew,fileData):
        more_headers = {}
        filename=filenamnew.strip("/")
        if(not os.path.isfile(filename)):
                filename = None
        if filename == None:
                filename = filenamnew.strip('/')
                response_code = 201
        else : 
                response_code = 204

        contentType = mimetypes.guess_type(filename)[0]
        if contentType == 'text/html':
                with open (filename, 'w') as f:
                        f.write(fileData)
        else:
                with open (filename, 'wb') as f:
                        f.write(fileData.encode("utf-8"))
        message = ""
        message += f"HTTP/1.1 {response_code} {status[response_code]}\r\n"
        message += f"Date: {time.strftime('%a, %d %b %Y %I:%M:%S', time.gmtime())} GMT\r\n"
        for h in headers:
                message+=f"{h}: {headers[h]}\r\n"
        more_headers['Content-Type'] = contentType
        more_headers['Content-Location']= "/"
        for h in more_headers:
                message += f"{h}: {more_headers[h]}\r\n"
        message += "\r\n"
        return message, None

