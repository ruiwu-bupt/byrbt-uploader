import requests
import json
import byrbt_login
import resource_selector
import get_resource
import qbit
import os

# 获得磁盘剩余空间
def disk_free(path):
    if not os.path.exists(path):
        print("path don't exist")
    vfs=os.statvfs(download_path)
    return vfs.f_bfree*vfs.f_frsize/(1024*1024*1024)

def disk_total(path):
    if not os.path.exists(path):
        print("path don't exist")
    vfs=os.statvfs(download_path)
    return vfs.f_blocks*vfs.f_frsize/(1024*1024*1024)
# 读取配置文件
with open("config.json") as f:
    config = json.load(f)

# 初始化登录
login=byrbt_login.login(config)

# 返回最新torrents列表
torrents = get_resource.get_torrents(login)

# 根据特定规则对选出的torrent进行优先级排序
resource_selector.sort_torrent(torrents)

# 初始化下载模块
my_qbit = qbit.qbit(config)
download_path = os.path.expanduser("~")+config["download_path"]
if not os.path.exists(download_path):
    os.mkdir(download_path)

# 删除上传量过低的种子
my_qbit.delete()

# 添加热门种子，不超过硬盘空间的80%
for torrent in torrents:
    if disk_free(download_path) > 0.2*disk_total(download_path):
        if disk_free(download_path)+torrent["size"] > 0.2*disk_total(download_path):
            my_qbit.download(torrent["download_link"])
        else:
            continue

