import platform
import requests

url = "http://antpython.net/static/pubdatas/webspider/goodimgs/1.jpeg"
r = requests.get(url)
# 写入图片
with open("py017.jpeg", "wb") as f:
    f.write(r.content)
f.close()
print("Python 版本", platform.python_version())