### Pytorch在训练时都该保存些什么东西

由于什么网络故障，时间限制，经常会从训练过程中中断，保存一些必要的信息可以使得继续训练得以实现。

废话少说，需要保存的东西为

1. 模型参数

2. 随机事件种子

3. 优化器

4. lr_scheduler

最后一种是可选择的，第二种其实也算是可选择的，如果不考虑可重现性的话（

类似的有些优化器只需要保存一下learning rate 就好，但是对于Adam这种类型其中优化参数可能随着训练过程发生变化的复杂优化器就有必要把里面的参数全都保存一下。

对于第二条可以挑一个自己喜欢的模数，最好是质数

```python
seed = 998244353
torch.manual_seed(seed)
torch.cuda.manual_seed(seed)
torch.cuda.manual_seed_all(seed)  
np.random.seed(seed)  # Numpy module.
random.seed(seed)  # Python random module.
torch.manual_seed(seed)
torch.backends.cudnn.benchmark = False
torch.backends.cudnn.deterministic = True
```

对于第一条第三条来说，可以利用Pytorch自带的序列化方法进行保存

```python
def set_checkpoint(checkpoint_name, model, optimizer):
	torch.save({
		'model': model.state_dict(),
		'optimizer': optimizer.state_dict()
	}, checkpoint_name);
```

加载的时候也很方便

```python
def load_checkpoint(checkpoint_name, model, optimzer):
	_dict = torch.load(checkpoint_name)
	model.load_state_dict(_dict['model'])
	optimizer.load_state_dict(_dict['optimizer'])

```

具体调用过程

```python
# 保存阶段
net = Net()
optimizer = torch.optic.................
set_checkpoint('你想要的的位置', net, optimzer)
```

```python
# 加载阶段
net = Net()
optimizer = torch.optic.................
load_checkpoint('你要的位置', net, optimizer);
```



