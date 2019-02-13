# -*- coding:utf-8 -*-
# A dictionary of movie critics and their ratings of a small set of movies
# 一个涉及影评者及其对几部影片评分情况的字典 嵌套字典
# 用户偏好 数据集  每个用户 的 多部电影评分
# 使用字典存储数据很方便进行查询和修改
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 
 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 
 'You, Me and Dupree': 3.5}, 
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
 'The Night Listener': 4.5, 'Superman Returns': 4.0, 
 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 
 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 2.0}, 
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

# 访问 & 修改         人           电影名                 评分
# prtint(critics['Lisa Rose']['Lady in the Water']) ===> 2.5

from math import sqrt

# Returns a distance-based similarity score for person1 and person2
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

# 测试
# sim_distance(critics,'Lisa Rose','Gene Seymour')

# Returns the Pearson correlation coefficient for p1 and p2
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

# Gets recommendations for a person by using a weighted average
# of every other user's rankings
def getRecommendations(prefs,person,similarity=sim_pearson):
  totals={}
  simSums={}
  for other in prefs:
    # don't compare me to myself
    if other==person: continue
    sim=similarity(prefs,person,other)

    # ignore scores of zero or lower
    if sim<=0: continue
    for item in prefs[other]:
	    
      # only score movies I haven't seen yet
      if item not in prefs[person] or prefs[person][item]==0:
        # Similarity * Score
        totals.setdefault(item,0)
        totals[item]+=prefs[other][item]*sim
        # Sum of similarities
        simSums.setdefault(item,0)
        simSums[item]+=sim

  # Create the normalized list
  rankings=[(total/simSums[item],item) for item,total in totals.items()]

  # Return the sorted list
  rankings.sort()
  rankings.reverse()
  return rankings

def transformPrefs(prefs):
  result={}
  for person in prefs:
    for item in prefs[person]:
      result.setdefault(item,{})
      
      # Flip item and person
      result[item][person]=prefs[person][item]
  return result


def calculateSimilarItems(prefs,n=10):
  # Create a dictionary of items showing which other items they
  # are most similar to.
  result={}
  # Invert the preference matrix to be item-centric
  itemPrefs=transformPrefs(prefs)
  c=0
  for item in itemPrefs:
    # Status updates for large datasets
    c+=1
    if c%100==0: print "%d / %d" % (c,len(itemPrefs))
    # Find the most similar items to this one
    scores=topMatches(itemPrefs,item,n=n,similarity=sim_distance)
    result[item]=scores
  return result

def getRecommendedItems(prefs,itemMatch,user):
  userRatings=prefs[user]
  scores={}
  totalSim={}
  # Loop over items rated by this user
  for (item,rating) in userRatings.items( ):

    # Loop over items similar to this one
    for (similarity,item2) in itemMatch[item]:

      # Ignore if this user has already rated this item
      if item2 in userRatings: continue
      # Weighted sum of rating times similarity
      scores.setdefault(item2,0)
      scores[item2]+=similarity*rating
      # Sum of all the similarities
      totalSim.setdefault(item2,0)
      totalSim[item2]+=similarity

  # Divide each total score by total weighting to get an average
  rankings=[(score/totalSim[item],item) for item,score in scores.items( )]

  # Return the rankings from highest to lowest
  rankings.sort( )
  rankings.reverse( )
  return rankings

def loadMovieLens(path='/data/movielens'):
  # Get movie titles
  movies={}
  for line in open(path+'/u.item'):
    (id,title)=line.split('|')[0:2]
    movies[id]=title
  
  # Load data
  prefs={}
  for line in open(path+'/u.data'):
    (user,movieid,rating,ts)=line.split('\t')
    prefs.setdefault(user,{})
    prefs[user][movies[movieid]]=float(rating)
  return prefs
