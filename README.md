# Chaos
搜索引擎图片抓取服务，支持不同的搜索引擎根据关键字搜索图片，并返回图片链接。

## Introduction
服务端将会解析用户发来的请求，选择对应的搜索引擎与关键字，再构造出搜索引擎支持
的查询参数，再向搜索引擎发出搜索请求，拿到到搜索引擎的返回结果，并解析出图片
链接，返回给用户。

## Install and Deploy
暂略

## Usage
* 搜图接口: `/images`
* HTTP方法：GET
* 查询参数:
    - `engine` 指定搜图的搜索引擎，可取值`baidu` 或 `google`
    - `word` 搜索关键字，多个关键字用加号(+)链接，例`帅哥+美女`
    - `limit` 图片数量限制，必须传递此参数，指定需要多少张图片
    - `size` 图片尺寸限制，取值`WIDTH,HEIGHT`, 例如 `300,400`
    - `sizetype` 图片尺寸限制类型，取值`eq`(相等),`gte`(大于等于)，`lte`(小于等于)，百度支持`eq`

* 注意
    - `size` 和 `sizetype` 两个参数都不传递则无尺寸限制
    - 有 `sizetype` 参数时，必须指定 `size` 参数
    - 有 `size` 参数，无 `sizetype` 参数时，`sizetype` 的默认值为 `eq`
    - 当`engine=google`时，目前支持爬取到的图片url最多为100条

* 返回结果样例：
```json
    {
        "engine": "baidu",
        "word": ["胖美女", "瘦美女"],
        "limit": 100,
        "images": ["url1", "url2", "url3", ...,  "url100"]
    }
```

* 实例
打开浏览器，访问：
http://10.60.81.249:8888/images?engine=baidu&word=%E7%BE%8E%E5%A5%B3+%E5%B8%85%E5%93%A5&limit=100
* 实例
打开浏览器，访问：
http://10.60.81.249:8888/images?engine=google&word=%E7%BE%8E%E5%A5%B3+%E5%B8%85%E5%93%A5&limit=100

## Change Log
pass

## License
Not Open Source.
