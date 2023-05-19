'''
Date: 2022.06.17
Title: 
By: Kang Jin Seong
'''
#라즈베리파이에서 연결된 LED제어하는 HTTP GET 서버프로그

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import parse
import RPi.GPIO as GP

#다중 query를 &를 기준으로 분리하고 딕셔너리로 반환한다.
def query_parse(query):
    a = query.split('&')
    temp = []
    for item in a:
        temp.append(item.split('='))
    for i in range(len(temp)):
        if len(temp[i]) == 1:
            temp[i].append('')
    return dict(temp)

def setGPIO(pin,mode):	#라즈베리파이 GPIO 설정
	GP.setmode(GP.BCM)
	GP.setwarnings(False)
	GP.setup(pin, mode)

class SimpleHTTPRequestHandelr(BaseHTTPRequestHandler):
	def do_GET(self):
		parsed_path = parse.urlparse(self.path)
		msg = parsed_path.query
		if msg == '':
			return
		
		parsed_query = query_parse(msg)
		
		if parsed_query["led"] == "on":
			resp = "the led is on"
			GP.output(18,1)
		elif parsed_query["led"] == "off":
			GP.output(18,0)
			resp = "the led if off"
		else:
			resp = "Fault"
		
		self.send_response(200)
		self.send_header('Content-Type', 'text/plain; charset = utf-8')
		self.end_headers()
		self.wfile.write(resp.encode())

setGPIO(18,GP.OUT)
httpd = HTTPServer(('30.0.1.16',8080), SimpleHTTPRequestHandelr)
httpd.serve_forever()
