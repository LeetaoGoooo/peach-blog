---
title: axios中使用application/x-www-form-urlencoded
tag: [nodejs]
date: 2017-12-26
---

## 问题
这几天用go写了一个api接口，用postman测试的时候,数据返回都正常的,然后用 axios 请求的时候,服务器始终接收不到前台发来的的参数,感觉问题可能出现在请求头,然后打开chrome开发者工具,查看一下请求详情

## axios 请求的详情

Request-Headers 的 **Content-Type** 是 **application/json;charset=UTF-8**,Request Payload格式为
>{param1: "value1", params: "value2"}

## postman 请求的详情

Request-Headers 的 **Content-Type** 是 **application/x-www-form-urlencoded**,URL encode 为
>param1=value1&param2=value2

对比了一下很明显问题就出在这里,接下来该怎么解决问题

## 问题的解决

###  使用 URLSearchParams

此方法不推荐,兼容性不太好,见下图:

![](http://ww1.sinaimg.cn/large/006wYWbGly1fmudwfsis1j31h30jz76f.jpg)

使用示例代码:

```javascript
var params = new URLSearchParams();
params.append('param1', 'value1');
params.append('param2', 'value2');
axios.post('/foo', params);
```

### 使用 qs 库

使用示例代码:

```javascript
var qs = require('qs');
axios.post('/foo', qs.stringify({ 'bar': 123 }));
```
