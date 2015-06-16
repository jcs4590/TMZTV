import sys
import xbmcgui
import xbmcplugin
import urlparse
import urllib
from resources.lib import  Episode
import datetime
import requests
from bs4 import BeautifulSoup




base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle,'movies')


for a in sys.argv:
        print(a + "    GREAT loser")

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def getVideoURL(videoURLS):
    episodes = []
    for videoURL in videoURLS:
        page = requests.get(videoURL)
        tree = BeautifulSoup(page.text)
        url = tree.head.find(attrs={"name":"VideoURL"})['content']
        dateString = tree.head.find(attrs={"name":"ActivationDate"})['content']
        date = datetime.date(int(dateString[:4]), int(dateString[5:7]), int(dateString[8:]))
        title = tree.head.find(attrs={"name":"twitter:title"})['value']
        thumbnail = tree.head.find(attrs={"name":"ThumbURL"})['content']
        episodes.append(Episode.Episode(date, title, url, thumbnail))
    return episodes




def getAllVideosURL():
    urls = set()
    page = requests.get('http://www.tmz.com/when-its-on?adid=TMZ_Web_Nav_TMZ_On_TV')
    tree = BeautifulSoup(page.text)
    for a in tree.find_all('div', { "class" : "episode" }):
        url = a.find('a', href=True)['href'].rsplit('/', 1)[0]
        urls.add(url)
    return urls

mode = args.get('mode', None)

if mode is None:
    url = build_url({'mode':'folder','foldername':'All Episodes'})
    li = xbmcgui.ListItem('All Episodes', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li,
                                isFolder=True)
    url = build_url({'mode':'folder','foldername':'TMZ Live'})
    li = xbmcgui.ListItem('TMZ Live',iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li,
                                isFolder=True)
    print("lakers")
    print (mode)
    xbmcplugin.endOfDirectory(addon_handle)
    
elif mode[0] == 'folder':
    foldername = args['foldername'][0]
    if foldername == 'TMZ Live':
        url = 'http://tmz.vo.llnwd.net/o28/2015-06/11/0_1knf7bef_0_lxuqmreg_2.mp4'
        li = xbmcgui.ListItem('You Tube!', iconImage='DefaultVideo.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url = url, listitem=li)
        xbmcplugin.endOfDirectory(addon_handle)
    elif foldername == 'All Episodes':
        urls = getAllVideosURL()
        episodes = getVideoURL(urls)
        for episode in episodes:
            li = xbmcgui.ListItem(episode.title, iconImage=episode.thumbnail)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=episode.url, listitem=li)
        xbmcplugin.endOfDirectory(addon_handle)










