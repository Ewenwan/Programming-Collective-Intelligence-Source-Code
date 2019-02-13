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
# 用户偏好 数据集
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 
 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 
 'You, Me and Dupree': 3.5}, 
 ...
 }

```
