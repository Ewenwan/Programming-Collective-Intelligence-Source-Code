# Programming-Collective-Intelligence-Source-Code
集体智慧编程源代码

[笔记&思维导图](https://github.com/ahangchen/PCInotes)

## 中文版PDF电子书免费下载地址

http://pan.baidu.com/s/1ntKHRPB

# 一、集体智慧导言
1、什么是集体智慧？

集体智慧（Collective Intelligence）:为了创造新的想法，而将一群人的行为、偏好或思想组合在一起。
    
    最早，调查问卷
    群体智能? 群体意识?
    
    利用开放的API搜集资料(群体智慧的结晶，缺点数据量大)，
    使用机器学习等方法提取其中有用的信息。

2、什么是机器学习？

机器学习是人工智能（AI，artificial intelligence）领域中与算法相关的一个子域，它允许计算机不断地进行学习。大多数情况下，这相当于将一组数据传递给算法，并由算法推断出与这些数据的属性相关的信息————借助这些信息，算法就能准确预测出未来有可能会出现的其他数据。为了实现归纳，机器学习会利用它所认定的出现于数据中的重要特征对数据进行“**训练**”，并借此得到一个**模型**。
    
    实际例子：
        1. 网页排名 PageRank
        2. 推荐系统 商品推荐、音乐推荐、旅游线路推荐、服务推荐
        3. 市场预测 股票预测、交友信息匹配
        4. 生物工艺学 DNA序列、蛋白质结构、RNA表达
        5. 金融欺诈侦测 信用卡欺诈侦测
        6. 机器视觉 智能监控
        7. 产品市场化 产品归类划分(聚类等方法)
        8. 供应链优化 产品区域需求分析
        9. 国家安全 恐怖袭击 


# 二、提供推荐

根据群体偏好来为人们提供推荐。有许多针对于此的应用，如在线购物中的**商品推荐、热门网站的推荐，以及帮助人们寻找音乐和影片的应用**。

![](https://github.com/ahangchen/PCInotes/raw/master/imgs/%E6%8F%90%E4%BE%9B%E6%8E%A8%E8%8D%90.png)

> 搜集偏好

```python
# recommendations.py
# 一个涉及影评者及其对几部影片评分情况的字典 嵌套字典
# 用户偏好 数据集 每个用户 的 多部电影评分
# 使用字典存储数据很方便进行查询和修改
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 
 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 
 'You, Me and Dupree': 3.5}, 
 ...
 }
 
# 访问 & 修改         人           电影名                评分
# prtint(critics['Lisa Rose']['Lady in the Water']) ===> 2.5


```
当然，我们也可以去网上下载数据量更大的数据集供我们学习，

如[GroupLens项目组开发的涉及电影评价的真实数据集](https://grouplens.org/datasets/)

或者通过获取RSS订阅源数据来构建数据集。


> 寻找相近用户
    
    使用一种方法确定人们在品味方面的相似程度。
    
    评价值           特点
    欧几里德距离     多维空间中两点之间的距离，用来衡量二者的相似度。距离越小，相似度越高。

    皮尔逊相关度评价 判断两组数据与某一直线拟合程度的一种度量。
                    在数据不是很规范的时候
                   （如影评者对影片的评价总是相对于平均水平偏离很大时），
                    会给出更好的结果。
                    相关系数越大，相似度越高。
    jaccard系数
    曼哈顿距离
    
                    
```python
# 返回一个有关person1和person2的基于欧式距离的相似度评价
def sim_distance(prefs,person1,person2):
    # 获取共有条目列表 shared_items
    si={}
    for item in prefs[person1]:
	# 数据匹配
        if item in prefs[person2]:
            si[item]=1
    
    # if they have no ratings in common, return 0
    # 如果两者没有 共同之处，计算不了
    if len(si)==0:
	# 无共有条目
	return 0
    
    # 对共有条目的平方 计算欧氏距离(差平方) 越相近距离越短
    sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2) 
                      for item in prefs[person1] if item in prefs[person2]])
    # 加1(避免除零)后取其倒数，新函数返回值介于0~1之间，返回1表示两人具有一样的偏好
    return 1/(1+sum_of_squares)
    
# 返回p1和p2之间的皮尔逊相关系数 评价指标
def sim_pearson(prefs,p1,p2):
    # Get the list of mutually rated items
    # 得到双方都 评价过的 商品列表
    si={}
    for item in prefs[p1]: 
        if item in prefs[p2]: 
	    si[item]=1
    # 得到 共有 条目数量
    n=len(si)
	
    # if they are no ratings in common, return 0
    if n==0:
	# 没有共有偏好
        return 0
	
    # 对每个用户所有共有偏好 求和
    sum1=sum([prefs[p1][it] for it in si])
    sum2=sum([prefs[p2][it] for it in si])
  
    # 平方和
    sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
    sum2Sq=sum([pow(prefs[p2][it],2) for it in si])	
     
    # 两方乘积之和
    pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])
  
    # 计算皮尔逊评价值 Calculate r (Pearson score)
    num=pSum-(sum1*sum2/n)
    den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
    if den==0: 
	return 0

    r=num/den

    return r
```

	为评论者打分
	 
```python
# 返回 与 persor人 品味最相似的前五个人
def topMatches(prefs,person,n=5,similarity=sim_pearson):
    # person 和 除去 person本人之外的其他人 计算相似度 得分
    scores=[(similarity(prefs,person,other),other) 
                  for other in prefs if other != person]
    
    scores.sort() # 升序排列
    scores.reverse()# 逆序 大->小
    return scores[0:n] # 取前n个

# 测试
# topMatches(critics,'Toby',n=3)
# 最相似的为 Lisa Rose
# 所以应该根据  Lisa Rose 的品味(喜好，来源其撰写的影评)为Toby推荐

```

> 为用户推荐电影,根据和其他用户的相似度和未看电影的平方加权求和后求均值，后逆序推荐
```python
# 推荐物品
# 利用 与其他所有人相似度对电影评分进行加权求和后平均，为 某人person 提供建议
def getRecommendations(prefs,person,similarity=sim_pearson):
    totals={}  # 电影 相似度 加权 电影评分
    simSums={} # 相似度之和
    for other in prefs:
        #不要和自己做比较
        if other == person: 
	    continue
	# 与另一个人的 相似度得分
        sim=similarity(prefs,person,other)

        #忽略相似度为零或小于零的情况
        if sim<=0: 
	    continue
        
	# 遍历这个其他人看过的电影
        for item in prefs[other]:
            # 只对自己还未曾看过的影片item 进行评价
            if item not in prefs[person] or prefs[person][item] == 0:
                #相似度*评价值
                totals.setdefault(item,0)
		# 使用相似度对电影评分加权后求和
                totals[item] += prefs[other][item] * sim
                # 相似度之和
                simSums.setdefault(item,0)
                simSums[item] += sim

    # 建立一个归一化的列表 加权求和归一化值,电影名
    rankings=[(total/simSums[item],item) for item,total in totals.items()]   

    # 返回经过排序的列表
    rankings.sort()# 升序 小->大 
    rankings.reverse()# 逆序 大->小
    return rankings
```

> 匹配商品：通过将数据集中的人员和物品对换，构建新的数据集即可。
```python
#匹配商品
#商品与人员对换
def transformPrefs(prefs):
    result={}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})

            #将物品和人员对调
            result[item][person]=prefs[person][item];
    return result
```

# 三、发现群组

https://www.cnblogs.com/xiaoYu3328/p/5173854.html

![](https://github.com/ahangchen/PCInotes/raw/master/imgs/%E5%8F%91%E7%8E%B0%E7%BE%A4%E7%BB%84.png)


	聚类是把相似的对象通过静态分类的方法分成不同的组别或者更多的子集（subset），
	这样让在同一个子集中的成员对象都有相似的一些属性，
	常见的包括在坐标系中更加短的空间距离等。
	一般把数据聚类归纳为一种非监督式学习。
	
1、监督学习和无监督学习

	学习方式	种类	          方式
	监督学习	神经网络、决策树、贝叶斯过滤等	
	                     通过检查一组输入和期望的输出来进行“学习”。
	无监督学习	聚类算法	
	                     在一组数据中找寻某种结构，采集数据，然后找出不同的群组。

2、分级聚类


3、列聚类

	同时在行和列上对数据进行聚类常常是很有必要的。
	以上的例子中标签是博客，将数据集矩阵进行转置（行变列，列变行），
	使其标签变为单词，来进行聚类。
	
4、K-均值聚类

	分级聚类的缺点：不易操作，合并项之后关系还得在计算，计算量非常大。

	K-均值聚类算法首先会随机确定k个中心位置（位于空间中代表聚类中心的点），
	然后将各个数据项分配给最临近的中心点。
	待分配完成后，聚类中心就会移到分配给该聚类的所有节点的平均位置处，
	然后整个分配过程重新开始。这一过程会一直重复下去，直到分配过程不再产生变化为止。

5、多维缩放
	
	前面我们已经用数据可视化方式来表示聚类，然而在大多数情况下，
	我们所要的聚类的内容都不只包含两个数据，
	所以我们不可能按照之前的方法来采集数据并以二维形式表现出来。
	
	通过多维缩放为数据集找到一种二维表达形式。
	算法根据每对数据项之间的差距情况，尝试绘制出一幅图来，
	图中各数据项之间的距离远近，对应于它们彼此间的差异程度。（欧几里德距离算法）
	
	
	




	
