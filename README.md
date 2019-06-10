# python_yadisk
Python Yandex.Disk API:
1. Importing:
```
from yadisk import Yadisk
```
2. Downloading "main.py" file from this link "https://yadi.sk/d/Tid5zLokLHb30g":
```
disk = Yadisk(auth=False)
disk.download_public("https://yadi.sk/d/Tid5zLokLHb30g", path="main.py", path_to_save="qwe.py")
```
3. Uploading file to your ya.disk:
```
disk = Yadisk(auth=True)
print(disk.upload("qwe.py", "main.py"))
```
