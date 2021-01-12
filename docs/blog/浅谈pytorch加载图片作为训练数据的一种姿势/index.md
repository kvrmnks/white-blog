本文以HWDB1.1 数据的处理作为例子，简单介绍如何简单地将图片作为训练/测试数据

---

一般在深度学习中，训练数据集都十分庞大，无法一次加载到内存中，只能分批次加载到内存中去。


幸运地是 torchvision 中自带了一种可以分批次加载数据的方式。




## 在硬盘上建立正确的文件结构

对于HWDB1.1 这个数据集来说，一个文件中包含了许多的图片， 我们首先需要获取到这些图片和图片对应的 label，这一部分可以在 [从零开始的解析HWDB1.1数据之路](../../blog/从零开始的解析HWDB1.1数据之路/index.md)找到。


这个方法会返回features，labels数组。


假设我们要把所有的训练数据放在train_data文件夹下，我们需要建立这样一种结构


1. 每个图片存在于其label对应的文件夹内


2. 同一个label的文件夹内图片名不能相同


3. 各个label文件夹都在train_data下


打个比方来说，有一张图片对应的label是1，那么它的路径就是/train_data/1/xxx


之后我们就可以用torchvision.datasets.ImageFolder 对这个结构进行解析，具体步骤见下文。


**注意这里有一个很严重的坑**


ImageFolder  会对每个label进行重新赋值为一个数字，具体来说就是，按照label名的字典序依次转化为0, 1, ...


所以如果train_data文件夹下有1, 2, 10这3个文件夹，ImageFolder转化10的label会被标成1而不是10，因为10作为一个字符串，排在字典序的第2位。


这里由于不是没有涉及太多科技，代码不再给出。


## 如何解析这个文件结构 并且对读入的图片做预处理


这里介绍的ImageFolder 与下一节的DataLoader是配套的，所以如果在这一节中没看懂“为什么这么做”，可以看一下下一节一起理解。


正如上一句所说，我们使用ImageFolder自动解析"数据结构"(并非那个数据结构)。


用法如下


```python
from torchvision import datasets
from torchvision import transforms,utils
train_data = datasets.ImageFolder('train_data', transform=transforms.Compose([
    MyResize(64,64),
    transforms.ToTensor()
]))
```


第一个参数便是train_data这个文件夹的路径，可以看到第二个是个看不懂的参数（，这个参数有关加载之后图像的初始化。


现在就讲，不会咕不会咕。


首先trainsforms.Compose([...])，是将参数tuple里的参数依次执行。


先忽略原文中的那个MyResize(64,64)


先来看看那个transforms.ToTensor()


这是tranforms 自带的一个transform类，可以将图片转化为tensor数组，并且把图片的值域压缩到$[0,1]$上，方便训练。


再来细说一下那个MyResize(64, 64), 这是一个自定义transform类，要自定义这样一个类需要定义$\_\_call\_\_$方法，即如下形式


```python
class MyTransform():
	def __init__(self, ):
		# 初始化
		pass
	def __call__(self, img):
		# 对图像做一些操作
		return img
```

由于tranforms 自带的resize太拉胯了，我就自己写了resize，具体方法见 [从零开始的解析HWDB1.1数据之路](../..//blog/从零开始的解析HWDB1.1数据之路/index.md)


这里仅仅给出代码

```python
class MyResize(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    def __call__(self, img):
        raw_width, raw_height = img.size
        ratio = min(self.height/raw_height, self.width/raw_width)
        twidth, theight = (min(int(ratio * raw_width), self.width - 15), min(int(ratio * raw_height), self.height - 15))
        img = img.resize((twidth, theight), Image.ANTIALIAS)
        # 拼接图片，补足边框 居中
        ret = Image.new('L',(self.width, self.height), 255)
        ret.paste(img, (int((self.width-twidth)/2),int((self.height-theight)/2)))
        return ret
```

值得一提的是transforms​中还有很多有用的变换方式，可以用来加强数据的噪声，提高模型的泛化能力。

每个变换看完之后，再来回顾一下一开始的定义方式。
```python
from torchvision import datasets
from torchvision import transforms,utils
train_data = datasets.ImageFolder('train_data', transform=transforms.Compose([
    MyResize(64,64),
    transforms.ToTensor()
]))
```

这里的含义便是从"train_data"加载数据自动表示label，并对每张图片先放缩到大小为(64, 64)，再将图片转化为Tensor类型。

那怎么从这个里面取出数据来训练呢？

## 如何自动分批次读取数据

又幸运的是，pyTorch也提供了和ImageFolder一起的分批次加载数据的方式，即DataLoader。

```python
import torch.utils.data as Data
batch_size = 32
train_loader = Data.DataLoader(train_data,batch_size=batch_size, shuffle=True)
# train_data 是ImageFolder
```

就这样定义十分简单(

batch_size 就是每个批次的大小

shuffle代表是否随机据取数据，True为随机

用法如下

```python
for x, y in train_loader:
    # x 是 data 就愉快地可以训练了
    # y 是 label
```

严格来说ImageFolder在初始化阶段不会真正地将数据加载到内存，只会标明数据的label和数据的位置。

在向DataLoader进行请求的时候ImageFolder会从硬盘读取数据，这样有效防止了爆内存的事情发生，当然不可避免地会拖慢图片加载的速度。

其实DataLoader有一个num_works参数可以多核读数据，但是windows好像有bug...

