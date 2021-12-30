from modules import *

headers = {
        "Server" : "HTTP/1.1 (Ubuntu)",
        "Accept-Language" : "en-US,en;q=0.9"
        
}

status = {
        200 : 'OK',
        201 : 'Created',
        400 : 'Bad Request',
        404 : 'Not Found',
        204 : "No Content"
}

config = configparser.ConfigParser()
config.read('./settings.ini')
path = config['paths']['documentroot']
print(path)
os.chdir(path)
res_dir = config['files']['errorfiles']
print(res_dir)

def response_body( filename):
        content_type = mimetypes.guess_type(filename)[0]
        if content_type == 'text/html' or content_type == 'text/plain':
                with open(filename, 'r') as f:
                        response_body = f.read()
                return response_body, False
        else:
                return '', filename

def getLastModifiedTime(fileinfo):
        date = fileinfo.st_mtime
        temp=time.ctime(date).strip()
        d = temp.split()
        return f"{d[0]}, {d[2]} {d[1]} {d[4]} {d[3]} GMT"

def IsGzipEncoded(headers):
        try:
                headers['accept-encoding']
                return True
        except:
                return False
