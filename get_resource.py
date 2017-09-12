import requests
import bs4
import json
import time


def get_torrents_of_page(login, page_num):
    doc = bs4.BeautifulSoup(login.session.get(login.url + "&page=" + str(page_num),
                                              headers=login.headers, cookies=login.cookies).text, 'html5lib')
    torrents_tag = doc.select("table.torrents > tbody > tr.free_bg")
    torrents = []
    torrent_info_name = ['type', 'title', 'comment', 'upload_time', 'size', 'uploader', 'downloader', 'complete']
    for torrent_tag in torrents_tag:
        torrent_info = torrent_tag.select(" > td")
        tmp = {}
        for i in range(len(torrent_info_name)):
            if i == 0:
                tmp[torrent_info_name[i]] = torrent_info[i].find("img")["alt"]
            else:
                tmp[torrent_info_name[i]] = torrent_info[i].get_text()
        tmp['download_link'] = "http://bt.byr.cn/" + torrent_tag.find(attrs={"title": "下载本种"}).parent["href"]
        torrents.append(tmp)
    return torrents


def get_torrents(login):
    torrents = []
    with open("config.json") as f:
        page_num = json.load(f)["page_num"]
    for i in range(page_num):
        torrents.extend(get_torrents_of_page(login, i))
        time.sleep(0.2)
    for torrent in torrents:
        torrent["uploader"] = int(torrent["uploader"])
        torrent["downloader"] = int(torrent["downloader"])
        torrent["comment"] = int(torrent["comment"])
        torrent["complete"] = int(torrent["complete"].replace(',', ''))
        size = torrent["size"]
        if size[-2] == 'K':
            size = float(size[0:-2]) / (1024 * 1024)
        elif size[-2] == 'M':
            size = float(size[0:-2]) / 1024
        elif size[-2] == 'T':
            size = float(size[0:-2]) * 1024
        else:
            size = float(size[0:-2])
        torrent["size"] = size
    return torrents
