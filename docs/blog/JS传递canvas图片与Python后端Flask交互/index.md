其实这东西是尝试把Neural Model部署在网页上时摸索的
<!--more-->
### 第一步 先整个canvas
```html
<canvas> </canvas>
```
~~好了~~

### 第二步 把canvas里的图片整下来
必须要获得canvas的内容才能发到服务器呀
这里推荐canvas 的dom对象自带的toDataUrl()函数
``` js
let canvas = document.getElementById('这里写你的canvas的id')
let url = canvas.toDataUrl('Image/png')
```
这个方式的参数是可选的，会把canvas的内容进行不同的编码，在进行base64加密
如果不写的话默认是转化成png格式

### 第三步 把图片url POST到服务器
这里就简单地用JQuery的POST就好了，别扯乱七八糟的了。
JQuery头部
```html
<script src="https://cdn.staticfile.org/jquery/1.10.2/jquery.min.js"></script>
````
POST的使用方法
```js
$.post(
    url,
    data,
    func(data, status)
)
```
其中url代表要POST到的地址，可以写相对地址的哦。
data是一个字典，代表你要传的内容，这里默认是以text的方式传，不是JSON。
func(data, status) 代表相应之后的回调函数，data表示收到的数据，status代表响应状态。

网页就写完了呢~

### 第四步 Flask 怎么处理 POST的数据呢
这里要对应上文的一句话 “data是一个字典，代表你要传的内容，这里默认是以text的方式传，不是JSON。”
这里传的是text而不是JSON，Flask的response对于两种类型有着不同的解析方式，这里只介绍text的情况。
```python
from Flask import response
data = response.form['POST是字典的Key']
```
看起来挺简单的

### 第五步 传过来的是图片Url我咋把它转成图片啊
#### 第一小步 把Url先解个码，转成二进制
```python
import urllib
data = urllib.request.urlopen(URL)
```
就完了，是不是很简单~

#### 第二小步 把二进制转成图片
这里图片使用的是PIL模块
加载PIL的Image
```python
from PIL import Image
```
然后就能发现Image有个frombytes方法可以从二进制生成图片，但是需要图片大小，这谁知道啊。~~其实可以从网页发一个呀2333~~

如果你再探索一下就能发现一个令人迷惑的现象，你可以把二进制写成图片，然后用Image读文件生成图片。

那岂不是每次都要做一次文件读写？
当然有方法避免，io.ByteIO()可以提供一个bytes流来模拟文件
使用方法如下
```python
    buffer = io.ByteIO()
    buffer.write(你的二进制数据)
    img = Image.open(buffer)
```
就好了

### 第六步 我咋知道图片是什么格式，我转格式啊，有什么坑啊
关于图片的模式可以通过img.mode查看
已知png图片为RGBA，jpeg图片为RGB
一般转格式都已可以通过convert 但是
把RGBA转成RGB或者灰度图的时候有坑，如果直接通过上面的方法会直接丢失掉透明度，即A
这里还有个迷惑行为是chrome中黑色有的时候用透明度维度表示

然后就没了~

