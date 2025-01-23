import platform
import requests

def threedig(page: int) -> str:
    page = str(page)
    while len(page) < 3:
        page = "0" + page
    return page

def down(page: int) -> bool:
    url =  "https://www.pearsonactivelearn.com/r00/r0091/r009134/r00913465/current/OPS/images/913465-"
    url +=  threedig(page) + ".jpg"
    r = requests.get(url)
    print(r.status_code, r.encoding)
    with open(f"./math/page{page}.jpg", "wb") as f:
        f.write(r.content)
        #print("okay")
        f.flush()
        f.close()

for i in range(21,1000):
    down(i)
    print(i)
#print("Python version", platform.python_version())


# https://www.pearsonactivelearn.com/r01/r0115/r011517/r01151727/current/OPS/images/9781292729541
# https://www.pearsonactivelearn.com/r00/r0091/r009134/r00913465/current/OPS/images/913465-001.jpg