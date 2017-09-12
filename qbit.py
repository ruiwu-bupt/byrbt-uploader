from qbittorrent import Client
import os
import time

class qbit:
    def __init__(self,login,config):
        self.config = config
        self.login=login
        self.localhost = self.config["host"]
        self.download_path = os.path.expanduser("~")+config["download_path"]
        self.qb = Client(self.localhost)
        self.qb.login(self.config["username"],self.config["passwd"])

    def download(self,download_link):
        if not os.path.exists(self.download_path):
            os.mkdir(self.download_path)
        self.qb.download_from_file(self.login.session.get(download_link,
                            headers=self.login.headers, cookies=self.login.cookies).content,
                                   savepath = self.download_path)

    def download_list(self,download_linklist):
        for download_link in download_linklist:
            self.download(download_link)

    def delete(self):
        torrents=self.qb.torrents()
        torrents_delete_hash=[]
        for torrent in torrents:
            exist_days = (time.time()-torrent["added_on"])/24*1024
            if exist_days>3 & torrent["uploaded"]/(torrent["total_size"]*exist_days)<0.2:
                torrents_delete_hash.append(torrent["hash"])
        self.qb.delete_permanently(torrents_delete_hash)
