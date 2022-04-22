from pyspark import SparkContext
from pyspark.mllib.recommendation import MatrixFactorizationModel
import os
import json

sc=SparkContext('local[*]')
def recommendProducts(user_id,result_num):
    #模型的调用
    base_dir=os.path.dirname(os.path.abspath(__file__))
    save_path=os.path.join(base_dir,'model')
    model=MatrixFactorizationModel.load(sc,save_path)
    dic={}
    ls=[]
   #输出在用户id=x的情况下 对其推荐的result_num本书籍
    for r in model.recommendProducts(user_id,result_num):
        temp={}
        user_id,item_id,similar=r[0],r[1],r[2]
        temp['user_id']=user_id
        temp['item_id']=item_id
        temp['similar']=similar
        ls.append(temp)
    #状态码
    dic['state']=1
    dic['msg']='success'
    #数据
    dic['data']=ls
    return dic


# a=recommendProducts(1,15)
# print(a['data'])