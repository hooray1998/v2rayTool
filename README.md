# v2ray 订阅更新工具

## 一、准备工作

> 确保安装了 v2ray

## 二、配置


### 添加订阅

编辑`sub.json`即可

### 建立`config.json`的软连接

**该脚本会在当前目录生成`config.json`，需要让 v2ray 找到它**

1. 例如你的 v2ray 的配置文件路径为`/etc/v2ray/config.json`, 本地路径为`/home/itt/v2rayTool`
2. 执行如下命令删除它并建立软连接
```sh
sudo rm /etc/v2ray/config.json
sudo ln -s /home/itt/v2rayTool/config.json /etc/v2ray/config.json
```

## 三、使用

`python v2rayTool.py`更新订阅并选择服务器

