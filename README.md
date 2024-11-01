# 网盘搜索 API

> 元站CMS&资源搜索引擎是一套内容管理系统，所有人都可以基于元站快速起站，构建自己的创意站点，目前盈利模式是基于内容做 SEO，通过底层的网盘分佣、会员以及流量广告赚钱。

元站本身是一个类似 WordPress 的内容管理系统，本身不提供资源搜索能力，仅仅是个站点构建系统，但是元站的用户可以通过元站的插件系统，自行开发一个网盘搜索 API 插件，实现网盘搜索功能，示例网站👉[夸克搜](https://www.quark.so/)。

本站就是一个符合[元站](https://www.moneysou.com/zsyz/89s4uc)搜索接口规范的网盘搜索 `API` 插件项目，基于本项目，所有购买元站的用户都可以自行搭建一个网盘搜索 API 服务，方便实现**全网搜**功能。

如果你感兴趣，可以通过我的[邀请码](https://www.moneysou.com/login?ref=moneysou)注册购买。

![元站](https://img.fre123.com/i/2024/10/11/6708f20fbc21d.jpg)

## 使用

直接基于 Docker 部署：

```shell
docker run -d -p 8067:8067 --name yz_pansearch_api --restart unless-stopped -e APP_TOKEN=your_token -e CACHE_TTL=604800 howie6879/yz_pansearch_api:http-v0.1.0
```

环境变量解释：

- APP_TOKEN：搭建完成后你自己访问的密钥 Token，根据自己喜好填写
- CACHE_TTL：缓存时间，单位秒，默认 604800 秒（7 天）

目前支持的源有：

- kk: 偏向最新剧集更新
- pansearch: 资源比较齐全
- dj: 短剧为主
- 更多资源可提交 PR 兼容

启动成功后，通过 `http://ip:8067`，curl 的请求示例如下：

```shell
curl --request POST \
  --url http://127.0.0.1:8067/v1/search/get_kk \
  --header 'APP-ID: yz_pansearch_api' \
  --header 'APP-TOKEN: 你启动服务自己设置的 Token' \
  --header 'PAN-TYPE: quark' \
  --header 'content-type: application/json' \
  --data '{
  "kw": "xx"
}'
```

关于请求 Header 头字段解释：

- APP-ID：固定值 `yz_pansearch_api`
- APP-TOKEN：你启动服务自己设置的 Token
- PAN-TYPE：网盘类型，取决于目标源支持哪些网盘，目前支持：
  - quark
  - baidu
  - xunlei
- IS-CACHE：是否使用缓存，取值 `1` 或 `0`，默认 `1`

返回格式（符合元站官方标准即可）：

```json
{
  "data": {
    "total": 1,
    "rows": [
      {
        "title": "七龙珠",
        "description": "",
        "res_dict": {
          "quark": [
            {
              "url": "https://pan.quark.cn/s/856e709b3ae7",
              "code": ""
            }
          ],
          "baidu": [
            {
              "url": "https://pan.baidu.com/s/1wXAwg439J0XLKlGwxmjJSg",
              "code": "4qhw"
            }
          ]
        }
      }
    ]
  },
  "info": "ok",
  "status": 0
}
```

关于如何集成到元站，进入**插件列表**，点击**全网搜**插件：

![全网搜案例](https://img.fre123.com/i/2024/10/24/671a4ea498e7f.png)

## 开发

```shell
git clone https://github.com/fre123-com/yz_pansearch_api
cd yz_pansearch_api
# 请先确认本机存在 python 3.11 的开发环境
# pipenv install --python=/~/anaconda3/envs/python3.11/bin/python3.11 --dev --skip-lock
pipenv install --python={YOUR_PYTGHON_PATH} --dev --skip-lock
# 推荐使用 VSCode 打开项目
```

## 说明

项目相关文档：
 - [接口文档](./docs/bruno/): 直接使用 [Bruno](https://github.com/usebruno/bruno) 打开即可调试接口&阅读文档

## 免费声明

本项目（以下简称“本项目”）是一个开源资源搜索引擎，软件名称为（yz_pansearch_api），仅限用于学习和研究目的。

- **使用目的**：本项目及软件（yz_pansearch_api）所提供的内容仅供个人学习与交流使用，严禁用于商业或非法目的。使用本软件时，用户必须遵守相关平台的服务条款和所在国家/地区的法律法规。用户对因使用本软件而产生的所有行为和后果负责，包括但不限于法律责任和财务责任。开发者不对因使用、修改或再发布本软件而导致的任何直接或间接损害承担任何责任。
- **版权声明**：使用本项目及软件（yz_pansearch_api）不拥有或控制所搜索到的任何资源的版权，版权争议与本项目无关。用户在下载后必须在24小时内从其设备中彻底删除相关内容。所有资源的版权归其各自的版权所有者所有，用户在使用这些资源时应遵循相关的版权法律法规。
- **风险承担**：使用本项目及软件（yz_pansearch_api）所存在的风险将完全由用户本人承担，软件（yz_pansearch_api）开发者不对因使用、修改或再发布本API而导致的任何直接或间接损害承担责任。
- **责任限制**：本项目及软件（yz_pansearch_api）仅提供工具，不存储任何文件，所有文件均来自互联网。因不当使用本项目或软件而导致的任何直接或间接损失，包括但不限于意外、疏忽、合约毁坏、诽谤、版权或其他知识产权侵犯及其所造成的任何损失，软件（yz_pansearch_api）作者概不负责，亦不承担任何法律责任。
- **用户责任**：用户在访问和下载本项目及软件（yz_pansearch_api）内容时，表示已阅读、理解并同意上述条款。用户应确保其使用本项目及软件的行为符合相关法律法规，并对其行为承担全部责任。
- **声明权利**：本项目及软件（yz_pansearch_api）相关声明的版权及其修改权、更新权和最终解释权均属开发者所有。开发者保留在不事先通知的情况下随时更新本免责声明的权利。

使用本软件即表示您同意这些条款，如果您不同意任何条款，请立即停止使用本软件，并删除所有相关文件。
