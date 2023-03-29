
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# FTP 서버에서 사용할 사용자 계정 설정
authorizer = DummyAuthorizer()
authorizer.add_user("user", "password", "/home/kangjinseong", perm="elradfmwMT")

# FTP 서버 설정
handler = FTPHandler
handler.authorizer = authorizer
server = FTPServer(("127.0.0.1", 21), handler)

# FTP 서버 시작
server.serve_forever()
