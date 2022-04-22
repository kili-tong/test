import os
from pyspark.sql import SparkSession
master='local[*]'
spark=SparkSession.builder.master(master).appName("recommend").getOrCreate()
#spark连接数据库读取shixi001.score表数据
sensor_df=spark.read.format('jdbc').option(
    'url','jdbc:mysql://localhost:3306/shixi001?user=root&password=123456'
).option('dbtable','score').load()
#创建临时表rating
sensor_df.createOrReplaceTempView('rating')
#查询表中的user_id,item_id,item_score字段返回成dataframe类型的数据赋值给result
result=spark.sql("select user_id,item_id,item_score from rating")
print(result.show())
print(type(result))
#调用spark 机器学习库中ALS算法
from pyspark.mllib.recommendation import ALS
#将dataframe转化成rdd
rating_rdd = result.rdd
#利用ALS对数据进行训练第一个参数：ratings 数据类型是是rdd格式，第二个参数rank：数据类型是int 将A（m*n）矩阵
#分解成m*rank 和rank*n的矩阵  第三个参数Iterations 数据类型是int 表示算法执行的次数 第四个参数double类型 建议值0.01
#返回数据类型Matrix...Model 即model的数据类型
#rank，根据数据的分散情况测试出来的值，特征向量纬度，如果这个值太小拟合的就会不够，误差就很大；如果这个值很大，就会导致模型大泛化能力较差；所以就需要自己把握一个度了，一般情况下10～1000都是可以的
# lambda也是和rank一样的，如果设置很大就可以防止过拟合问题，如果设置很小，其实可以理解为直接设置为0，那么就不会有防止过拟合的功能了
model = ALS.train(rating_rdd, 10, 10, 0.01)

#模型的保存
import os
import shutil
base_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(base_dir, 'model')
print(os.path.join(base_dir, 'model'))
if os.path.exists(save_path):
   shutil.rmtree(save_path)
model.save(spark.sparkContext, save_path)