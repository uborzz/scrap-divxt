import urllib
from bs4 import *
import re
import requests
import os

# ------------------------------------------
# User Config
# serieName: Nombre de la serie
# outpath: directorio de descarga
#
serieName = 'the walking dead'
outpath = 'C:/autodl/'
#
# --------------------------------------------

serieName = serieName.lower()
outpath = outpath + serieName + '/'
basepath = 'http://www.divxtotal.com'

if not os.path.exists(outpath):
    os.makedirs(outpath)


# fh = urllib.urlopen('http://www.divxtotal.com/series/breaking-bad-138/').read()
fh = urllib.urlopen(basepath + '/buscar.php?busqueda=' + serieName.replace(' ', '+')).read()
soup = BeautifulSoup(fh, 'html.parser')
tags = soup('a')


for tag in tags:
    seriePage = re.findall('^/series/' + serieName.replace(' ', '-') + '-[0-9]+/$',tag.get('href'))
    if len(seriePage) > 0:
        break


fhp = urllib.urlopen(basepath + seriePage[0]).read()
soup = BeautifulSoup(fhp, 'html.parser')
hrs = soup.find_all('a')
downloaded = dict()


for hr in hrs:
    if hr.get('title') == '':
        relative_url = hr.get('href')
        torrenturl = basepath + relative_url
        key = re.findall('[0-9]{1,2}x[0-9]{1,2}',relative_url)[0]
        if torrenturl.endswith('.torrent') and  downloaded.get(key) != True:
            downloaded[key] = True

            outfname = outpath +  torrenturl.split('/')[-1]
            r = requests.get(torrenturl, stream=True)

            if( r.status_code == requests.codes.ok) :
                fsize = int(r.headers['content-length'])
                print 'Downloading %s (%sMb)' % ( outfname, fsize )
                with open(outfname, 'wb') as fd:
                    for chunk in r.iter_content(chunk_size=1024): # chuck size can be larger
                        if chunk: # ignore keep-alive requests
                            fd.write(chunk)
                    fd.close()

print "\nFinalizado!!"