## AlphaZero-五子棋-GUI

这是另外一个项目的继承，原仓库：[Github-AlphaZero_Gomoku](https://github.com/junxiaosong/AlphaZero_Gomoku)

### 运行前的准备

环境要求：

- Python >=3.5

如果你只想和AI下棋：

- PyQt >= 5.10.1
- Numpy >= 1.11

如果你还想训练自己的AI：

- Theano >= 0.7 and Lasagne >= 0.1      
或者
- PyTorch >= 0.2.0    
或者
- TensorFlow

**ps**: if your Theano's version > 0.7, please follow this [issue](https://github.com/aigamedev/scikit-neuralnetwork/issues/235) to install Lasagne,  
otherwise, force pip to downgrade Theano to 0.7 ``pip install --upgrade theano==0.7.0``

### 让我们开始吧

开始GUI下的游戏请运行：

```
python gui.py
```

开始CUI下的游戏请运行：

```
python human_play.py
```

训练AI请运行：

```
python tran.py
```

**ps**: 训练之前记得修改`tran.py`里面相关的参数设置。

**训练小记**
1. 在6*6棋盘上的4子棋训练效果非常好，训练了2个小时，大约500~1000次自我博弈就得到了很好的结果。
1. 在8*8棋盘上的5子棋训练了2000~3000轮才得到比较好的结果，这在个人电脑上耗费了大约两天的时间。
1. 在19*19棋盘上的5子棋现在训练了5天3000+轮依旧没有得到理想的模型，AI大概发展到懂得5子棋规则的状态。
> 这三个模型都是19*19 的 5子棋版本
> * `current_policy.model` 大约训练了 200 轮
> * `current_policy1.model` 大约训练了 1000 轮
> * `current_policy2.model` 训练了 3050 轮

### 更多阅读
原作者的知乎页面:[AlphaZero实战：从零学下五子棋（附代码）-知乎](https://zhuanlan.zhihu.com/p/32089487)
我的个人博客:[Xice-博客](https://blog.xice.cf)