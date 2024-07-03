import requests
from http import cookiejar
import json
import os
import re

DIR = 'export/'
OUT_DIR = 'output/'

s = requests.session()

# cookie = cookiejar.MozillaCookieJar('cookies.txt')
# s.cookies.update(cookie)

dir_scan = os.walk(DIR)
urls = []
r = re.compile(r'[^/\\&\?]+\.\w{3,4}(?=([\?&].*$|$))',) #special thanks to https://stackoverflow.com/a/26253039

for root, directory, filenames in dir_scan:
    for file in filenames:
        file_path = os.path.join(root,file)
        # print(file_path)
        with open(file_path) as j:
            data = json.loads(j.read())
            for msg in data:
                try:
                    for file in msg['files']:
                        url = file['url_private_download']
                        file_id = file['id']
                        out_path = os.path.join(OUT_DIR, os.path.splitext(file_path[len(DIR):])[0])
                        out_name = file_id + '_' + r.search(url)[0]
                        if not os.path.exists(out_path):
                            os.makedirs(out_path)
                        full_path = os.path.join(out_path,out_name)
                        with open(full_path, 'wb') as f:
                            download = s.get(url)
                            f.write(download.content)
                except KeyError: continue
                except TypeError: continue