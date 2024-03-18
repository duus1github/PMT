# 过程
- load data
- build model
- train and test
- transfer learning

## load data ##
1.引入torch.utils.data.Dataset,继承这个类
    1).并实现__len__，__getitem__这两个方法
    ```
    class NumbersDataset(Dataset):
        def __init__(self,training=True):
            if training:
                self.samples = list(range(1,1001))
            else:
                self.samples = list(range(1001,1501))
        def __len__(self):
            return len(self.samples)
        def __getitem__(self,idx):
            return self.samples[idx]
    ```
2.preprocessing 数据预处理部分
- image resize
- Data Argumentation(数据增强):增加数据的规模，可以辅助性的提升模型性能。
    - rotate,crop
- Normalize(数据标准化):使得数据趋于稳定
    - mean,std
- ToTensor
# 过程详解 
- 首先是导入数据集吧：
  - 1、继承了Dataset——>加载pokemon数据集——>分别取它们文件存储路径和标签——>使用glob.glob()函数读取image数据,并存入到CSV文件中,
    ——>加载csv的数据集,得到的是文件路径和对应标签——>获取它们的数据,分为train,val,test三个数据集
    ——>实现__getitem__(),是用于将对应的照片转化为矩阵数据，这里是使用了transforms.Compose()方法
- 模型部分：  
  - 1、这里是使用的resnet18()的模型，我就在想，这个模型是不是直接不用改呢，我们要做的就是把自己的数据处理成它需要的数据，然后给喂进去。
- 训练部分：
  - 1、这里其实先是使用的原始的训练方法，但是得到的结果并没有很好，所以后来就是加入了迁移学习，然后提升了3个点的准确率
  - 2、来说说具体的步骤：
    - 导入参数数据args——>获取数据——>使用DataLoader(db),这样就可以得到train,val,test三笔数据集——>model初始化,使用Sequential(),获取前几个model,这里是迁移学习
     ——>定义adam优化器,交叉熵损失函数——>for循环开始训练——>for循环train_loader数据集——>将x放入到model中——>损失函数计算——>开始梯度下降
    ——>定义evalute()函数来记录每次的准确率，并将准确率最高的模型保存下来——>加载保存的模型，并使用测试数据进行测试。
- 
## 其他知识点
- stride：表示卷积的步幅，
- padding:表示输入的高和宽的两侧填充元素
# 进展
目前是已经把这个都学习好了，那接下来的化，就需要完成一下的内容了：  
1.重新回顾整理这个代码，了解其中没一个部分
2、为这个代码加上各种曲线。先来看看这个吧。这个我做了尝试，发现这些都是针对二分类的性能评价指标，而不是多分类的指标。
3、又知道了个问题，我之前以为的model是错误的，正确的理解应该是model的原理，你必需要知道，但其中的少数部分可以作出适当的修改，比如in_channel,out_channel，以及一些激活函数等
# run
-visdom: python -m visdom .server
