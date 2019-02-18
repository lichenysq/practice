import urllib
import re

f = urllib.urlopen('http://files.ute.nsn-rdnet.net/builds/wts/latestStable/')
data = f.read()
print(data.decode('utf-8'))

zipfile = re.findall(r'href="\S*?zip\b',data)[0].replace("href=\"", "")
tarfile = re.findall(r'href="\S*?core2.tar.bz2\b',data)[0].replace("href=\"","")
print(zipfile)
print(tarfile)


flodername = tarfile.split("_core")[0]
