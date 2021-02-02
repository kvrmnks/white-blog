### 简介
机器学习基础课为什么要安排一个深度学习的作业？
### ~~大事~~记录
#### 20200728之前
* 把Anaconda的环境搭建好了，一定记住安装一些类似于pyTorch的模块时一定要去官网找到正确的姿势。
* 还用了Anaconda的虚拟环境，除了有点占用硬盘以外，都挺好的。
![不也挺好吗？](file://C:/Users/Kvrmnks/Documents/Gridea/post-images/1595920396482.jpg)
* 简单的试了试把环境搭好，读了读数据集和测试集，试了试LeNet，发现好像可以识别1000种汉字？不过还没进行泛化实验
#### 20200728
* 尝试把测试集的格式直接存成numpy。
  存个啥，发现了正确的读数据的方式，比原来一个一个像素读快到不知道哪里去了
```python
content = file.read(height*width)
img = np.frombuffer(content, dtype=np.uint8).reshape(height,width)
 ```
 注意从byte 转 numpy 要用 np.formbuffer()
* 尝试进行图片大小的robust，计划直接按比例缩放，之前用的pyTorch自带的AdaptAvePool
用PIL的库写好了
* 跑了跑LeNet 全集