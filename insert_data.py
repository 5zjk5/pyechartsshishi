import csv
import time
import random
import pandas as pd
import numpy as np


'''
创建 3 张表，并插入初始数据
'''
with open('data/food_sale.csv','w+',encoding='utf8',newline='') as f1,\
     open('data/people.csv','w+',encoding='utf8',newline='') as f2,\
     open('data/comment.csv','w+',encoding='utf8',newline='') as f3:
    w1 = csv.writer(f1)
    w2 = csv.writer(f2)
    w3= csv.writer(f3)

    # 插入头部
    w1.writerow(['food_name','price','sale'])
    w2.writerow(['eat_peo','queue_peo','seat'])
    w3.writerow(['score','comment'])

    # 为 food_sale.csv 插入初始数据
    w1.writerows([['菲力牛排', 75, 0],['果奶', 24, 0],['炸薯条', 17, 0],
                  ['套餐1', 88, 0], ['套餐2', 40, 0], ['套餐3', 57, 0],
                  ['意大利面', 35, 0], ['通心粉', 35, 0], ['西冷牛排', 67, 0],
                  ['罗宋汤', 25, 0], ['慕斯蛋糕', 15, 0], ['香煎三文鱼', 40, 0],
                  ['儿童餐', 35, 0], ['土豆泥', 15, 0], ['黄金虾', 45, 0],
                  ['咖喱牛肉饭', 35, 0], ['土豆饼', 15, 0], ['芝士蜗牛肉', 30, 0],
                  ['甜心薯块', 15, 0], ['南瓜粥', 15, 0], ['水果披萨', 20, 0],
                 ])


'''
每隔 1.5 秒更新一次数据
'''
while True:
    # food_sale.csv 菜品销量表更新菜品销量
    df1 = pd.read_csv('data/food_sale.csv',encoding='utf8')
    # 生成 [0,4) 之间长度为 21 的随机数组
    new_sale = np.random.randint(4, size=21)
    new_sale = pd.Series(new_sale).values
    # 更新销量，sale 字段
    df1['sale'] = new_sale + df1['sale']
    df1.to_csv('data/food_sale.csv',encoding='utf8',index=False)

    # people.csv 人数状况表插入
    df2 = pd.read_csv('data/people.csv',encoding='utf8')
    # 生成数据
    eat_peo = random.randint(0,100)
    if eat_peo > 50:
        eat_peo = 50
        queue_peo = random.randint(10,30)
    else:
        queue_peo = 0
    # 插入数据
    s = pd.DataFrame({'eat_peo': [eat_peo], 'queue_peo': [queue_peo],'seat': [50]})
    df2 = df2.append(s, ignore_index=True)
    df2.to_csv('data/people.csv',encoding='utf8',index=False)

    # comment.csv 评论表插入数据
    df3 = pd.read_csv('data/comment.csv',encoding='utf8')
    # 生成数据
    score = random.randint(1,5)
    f = open('data/comment.txt', 'r', encoding='utf8')
    comments = f.readlines()
    f.close()
    comment = random.choice(comments)
    # 插入数据
    df3 = df3.append({'score' : score,'comment' : comment}, ignore_index=True)
    df3.to_csv('data/comment.csv',index=False)
    time.sleep(1.5)





