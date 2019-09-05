import requests,sys,subprocess,os
try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse
target = sys.argv[1]
try:
    os.mkdir( "./targets/%s"%(target), 0755 )
except:
    pass
url="http://web.archive.org/cdx/search/cdx?url=*.{}/*&output=text&fl=original&collapse=urlkey".format(target)
res = requests.get(url)
endpoints = set()
for line in res.text.splitlines():
    parsed_uri = urlparse(line)
    result = '{uri.scheme}://{uri.netloc}{uri.path}'.format(uri=parsed_uri)
    endpoints.add(result)
for i in endpoints:
    nopelist = ["jquery","wp-"]
    if ".js" in i and nopelist[0] not in i and nopelist[1] not in i:
        save = urlparse(i)
        pathname = '{uri.path}'.format(uri=save)
        print('Starting at %s' % (i))
        shell = subprocess.Popen("python linkfinder.py -i %s -o ./targets/%s/%s.html" %(i,target,os.path.basename(pathname)),shell=True)
        shell.wait()
    else:
        continue
