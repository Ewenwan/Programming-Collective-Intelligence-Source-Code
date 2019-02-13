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
    

