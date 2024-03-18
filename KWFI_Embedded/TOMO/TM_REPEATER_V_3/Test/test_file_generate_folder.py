import os
import datetime

now = datetime.datetime.now()
if not os.path.exists('./CSV_Data'):
    os.makedirs('./CSV_Data')
if not os.path.exists('./CSV_Data'+f"/{now.year}년"):
    os.makedirs('./CSV_Data'+f"/{now.year}년")
if not os.path.exists('./CSV_Data'+f"/{now.year}년"+f"/{now.month}월"):
    os.makedirs('./CSV_Data'+f"/{now.year}년"+f"/{now.month}월")
if not os.path.exists('./CSV_Data'+f"/{now.year}년"+f"/{now.month}월"+ f"/{now.day}일"):
    os.makedirs('./CSV_Data'+f"/{now.year}년"+f"/{now.month}월"+ f"/{now.day}일")
    
path = './CSV_Data'+f"/{now.year}년"+f"/{now.month}월"+ f"/{now.day}일"
print(path)


