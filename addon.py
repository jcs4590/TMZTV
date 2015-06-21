import sys, os
import xbmcgui
import xbmcplugin, xbmcaddon
import urlparse
import urllib
import requests
import ASettings
from bs4 import BeautifulSoup
import datetime
from resources.lib import Episode

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')
settings = xbmcaddon.Addon(id='plugin.video.tmztv')
icon = os.path.join(settings.getAddonInfo('path'), 'icon.png')
fanart = os.path.join(settings.getAddonInfo('path'),'fanart.jpg')

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)


def getVideoURL(videoURLS):
    episodes = []
    for videoURL in videoURLS:
        page = requests.get(videoURL)
        tree = BeautifulSoup(page.text)
        url = tree.head.find(attrs={"name": "VideoURL"})['content']
        dateString = tree.head.find(attrs={"name": "ActivationDate"})['content']
        date = datetime.date(int(dateString[:4]), int(dateString[5:7]), int(dateString[8:]))
        title = tree.head.find(attrs={"name": "twitter:title"})['value']
        thumbnail = tree.head.find(attrs={"name": "ThumbURL"})['content']
        episodes.append(Episode.Episode(date, title, url, thumbnail))
    return episodes


def getLiveURLS(URL):
    urls = []
    page = requests.get(URL)
    tree = BeautifulSoup(page.text)
    for a in tree.find_all('a',href=True):
        if("/videos/0" in a["href"]):
            urls.append("http://www.tmz.com" + a["href"])
    return urls


mode = args.get('mode', None)

if mode is None:
    url = build_url({'mode': 'folder', 'foldername': 'TV Episodes'})
    li = xbmcgui.ListItem('TV Episodes', iconImage=icon, thumbnailImage=icon)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li,
                                isFolder=True)
    url = build_url({'mode': 'folder', 'foldername': 'TMZ Live'})
    li = xbmcgui.ListItem('TMZ Live', iconImage=icon, thumbnailImage=icon)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li,
                                isFolder=True)
    url = build_url({'mode': 'folder', 'foldername': 'TMZ Raw & Uncut'})
    li = xbmcgui.ListItem('TMZ Raw & Uncut', iconImage=icon, thumbnailImage=icon)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li,
                                isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'folder':
    foldername = args['foldername'][0]
    if foldername == "TMZ Live":
        urls = getLiveURLS('http://m.tmz.com/category/tmz-live-archive-full-episodes/')
        episodes = getVideoURL(urls)
        for episode in episodes:
            li = xbmcgui.ListItem(episode.title, iconImage=episode.thumbnail)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=episode.url, listitem=li)
        xbmcplugin.endOfDirectory(addon_handle)
    if foldername == "TMZ Raw & Uncut":
        urls = getLiveURLS('http://m.tmz.com/videos/?view_page=1')
        episodes = getVideoURL(urls)
        for episode in episodes:
            li = xbmcgui.ListItem(episode.title, iconImage=episode.thumbnail)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=episode.url, listitem=li)
        xbmcplugin.endOfDirectory(addon_handle)
    if foldername == 'TV Episodes':
        headers = {
            ASettings.SIDDB: ASettings.IDDB,
            ASettings.SKDB: ASettings.KDB,
        }
        params = urllib.urlencode({"order": "-date"})
        r = requests.get(ASettings.EUL, headers=headers, params=params)
        content = r.json()["results"]
        for episode in content:
            li = xbmcgui.ListItem(episode["title"], iconImage=episode["thumbnail"])
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=episode["url"], listitem=li)
        xbmcplugin.endOfDirectory(addon_handle)
