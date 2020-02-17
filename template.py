# -*- coding:utf-8 -*-
# Author: Suummmmer
# Date: 2019-08-13

conf_template = {
  "inbounds": [{
        "listen": "127.0.0.1",
        "port": 1080,
        "protocol": "socks",
        "settings": {
            "auth": "noauth",
            "udp": True,
            "userLevel": 8
        },
        "sniffing": {
            "destOverride": [
                "http",
                "tls"
            ],
            "enabled": True
        },
        "tag": "socks"
    },
    {
        "listen": "127.0.0.1",
        "port": 1081,
        "protocol": "http",
        "settings": {
            "userLevel": 8
        },
        "tag": "http"
    }
  ],
  "log": {
      "loglevel": "warning",
      "access": "/etc/v2rayL/v2ray_access.log",
      "error": "/etc/v2rayL/v2ray_error.log",

  },
  "outbounds": [{
          "mux": {
              "enabled": False
          },
          "protocol": "",
          "settings": {},
          "streamSettings": {},
          "tag": "proxy"
      },
      {
          "protocol": "freedom",
          "settings": {},
          "tag": "direct"
      },
      {
          "protocol": "blackhole",
          "settings": {
              "response": {
                  "type": "http"
              }
          },
          "tag": "block"
      }
  ],
  "policy": {
      "levels": {
          "8": {
              "connIdle": 300,
              "downlinkOnly": 1,
              "handshake": 4,
              "uplinkOnly": 1
          }
      },
      "system": {
          "statsInboundUplink": True,
          "statsInboundDownlink": True
      }
  },
  "dns": {
      "servers": [
          "1.1.1.1"
      ]
  },
  "routing": {
      "domainStrategy": "IPIfNonMatch",
      "rules": []
  },
  "stats": {}
}
