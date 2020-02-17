#!python
# -*- coding:utf-8 -*-
import copy
import argparse
import subprocess
import requests
import base64
import urllib.parse as parse
import json
import os
from template import conf_template

class Sub2Conf(object):
    def __init__(self):
        try:
            with open("/usr/share/v2rayTool/sub.json", "r") as f:
                self.subs_url = json.load(f)
        except:
            raise Exception("[sub.json]: 无订阅或订阅无效")

        # 解析后配置
        # try:
            # with open("/usr/share/v2rayTool/conf.json", "r") as f:
                # self.conf = json.load(f)
        # except:
        self.conf = {}


        '''
        self.conf结构
        {
            "Moon-HK"： "配置(remark, address, port, id ... )",
            ...
        }
        '''

    def update(self):
        all_subs = []
        for name,url in self.subs_url.items():
            try:
                ret = requests.get(url, timeout=30, headers={'user-agent': 'hooray1998'})
                if ret.status_code != 200:
                    print("无法获取订阅({})的信息，订阅站点{}访问失败".format(name, url))
                subs = base64.b64decode(ret.text + "==").decode().strip()
                all_subs.extend(subs.split("\n"))
                print("订阅{} 服务器数量{}".format(name,len(subs.split("\n"))))
            except:
                raise Exception("无法获取订阅({})的信息，订阅站点{}访问失败".format(name, url))

        origin = []
        for sub in all_subs:
            origin.append(sub.split("://"))

        for ori in origin:
            if ori[0] == "vmess":
                ret = json.loads(parse.unquote(base64.b64decode(ori[1]+"==").decode()).replace("\'", "\""))
                region = ret['ps']
                self.conf[region] = ret
                # print("服务器:",region)
            else:
                print("暂不支持",ori[0],"其他协议")

        # 保存到conf.json, 有中文
        with open('/usr/share/v2rayTool/conf.json','w',encoding='utf-8') as f:
            json.dump(self.conf,f,ensure_ascii=False,indent=4)

    def setconf(self, region, http, socks):
        """
        生成配置
        :param region: 当前VPN别名
        :param http: http端口
        :param socks: socks端口
        :return:
        """
        use_conf = self.conf[region]
        conf = copy.deepcopy(conf_template)
        conf["inbounds"][0]["port"] = socks
        conf["inbounds"][1]["port"] = http

        conf['outbounds'][0]["protocol"] = "vmess"
        conf['outbounds'][0]["settings"]["vnext"] = list()
        conf['outbounds'][0]["settings"]["vnext"].append({
            "address": use_conf["add"],
            "port": int(use_conf["port"]),
            "users": [
                {
                    "id": use_conf["id"],
                    "alterId": int(use_conf["aid"]),
                    "security": "auto",
                    "level": 8,
                }
            ]
        })
        # webSocket 协议
        if use_conf["net"] == "ws":
            conf['outbounds'][0]["streamSettings"] = {
                "network": use_conf["net"],
                "security": "tls" if use_conf["tls"] else "",
                "tlssettings": {
                    "allowInsecure": True,
                    "serverName": use_conf["host"] if use_conf["tls"] else ""
                },
                "wssettings": {
                    "connectionReuse": True,
                    "headers": {
                        "Host": use_conf['host']
                    },
                    "path": use_conf["path"]
                }
            }
        # mKcp协议
        elif use_conf["net"] == "kcp":
            conf['outbounds'][0]["streamSettings"] = {
                "network": use_conf["net"],
                "kcpsettings": {
                    "congestion": False,
                    "downlinkCapacity": 100,
                    "header": {
                        "type": use_conf["type"] if use_conf["type"] else "none"
                    },
                    "mtu": 1350,
                    "readBufferSize": 1,
                    "tti": 50,
                    "uplinkCapacity": 12,
                    "writeBufferSize": 1
                },
                "security": "tls" if use_conf["tls"] else "",
                "tlssettings": {
                    "allowInsecure": True,
                    "serverName": use_conf["host"] if use_conf["tls"] else ""
                }
            }
        # tcp
        elif use_conf["net"] == "tcp":
            conf['outbounds'][0]["streamSettings"] = {
                "network": use_conf["net"],
                "security": "tls" if use_conf["tls"] else "",
                "tlssettings": {
                    "allowInsecure": True,
                    "serverName": use_conf["host"] if use_conf["tls"] else ""
                },
                "tcpsettings": {
                    "connectionReuse": True,
                    "header": {
                        "request": {
                            "version": "1.1",
                            "method": "GET",
                            "path": [use_conf["path"]],
                            "headers": {
                                "User-Agent": ["Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"],
                                "Accept-Encoding": ["gzip, deflate"],
                                "Connection": ["keep-alive"],
                                "Pragma": "no-cache",
                                "Host": [use_conf["host"]]
                            }
                        },
                        "type": use_conf["type"]
                    }
                } if use_conf["type"] != "none" else {}
            }

        with open('/usr/share/v2rayTool/config.json','w') as f:
            f.write(json.dumps(conf, indent=4))


if __name__ == "__main__":

    # parser = argparse.ArgumentParser(description="v2ray 工具")
    # parser.add_argument("update",nargs='?', help="更新订阅",default=False)
    # args = parser.parse_args()

    os.environ["all_proxy"] = ""
    s = Sub2Conf()

    print("开始更新订阅...")
    s.update()
    all_server = list(s.conf.keys())
    size = len(all_server)
    for index,name in enumerate(all_server):
        print(index+1, name)
    print('other-key >>>退出<<<')
    select = input("\n选择服务器 输入[1-%d]\n"%size)
    if select not in [ str(i) for i in range(1,size)]:
        print("exit 0")
        exit(0)
    select_server = all_server[int(select)-1]
    print('select:',select_server)
    # print('conf:',s.conf[select_server])

    s.setconf(select_server,10809,1080)
    output = subprocess.getoutput(["sudo systemctl status v2ray.service"])
    if "Active: active" in output:
        reCode = subprocess.call(["sudo systemctl restart v2ray.service"], shell=True)
        print(subprocess.getoutput(["sudo systemctl status v2ray.service"]))
        if reCode != 0:
            print("重启v2ray失败")
        else:
            print("重启v2ray成功")
    else:
        reCode = subprocess.call(["sudo systemctl start v2ray.service"], shell=True)
        print(subprocess.getoutput(["sudo systemctl status v2ray.service"]))
        if reCode != 0:
            print("启动v2ray失败")
        else:
            print("启动v2ray成功")
