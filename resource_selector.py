def torrent_priority(torrent):
    priority=10*torrent["downloader"]/(min(torrent["uploader"],1))
    if(torrent["size"]>10):
        priority+=(torrent["size"]-10)*2
    return priority

def sort_torrent(torrents):
    torrents[:] = sorted(torrents,key=torrent_priority,reverse=True)
    return torrents