# from django.shortcuts import render
import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render,redirect
from user.models import User,Item,Score
from recommend.recommend import recommendProducts
from django.core import serializers
# Create your views here.
def login(request):
    status=0
    if request.method == 'POST':
        res = {}
        try:
            login_type=request.POST['sub']
            status=1
        except:
            pass
        if status==1:  # 处理表单中的登录

            user_name = request.POST.get('username')
            user_pwd = request.POST.get('password')

            tmp = User.objects.filter(user_name=user_name).exists()
            if tmp:  # 若表中存在该用户名数据，则已注册
                is_reg = User.objects.filter(user_name=user_name, user_password=user_pwd).exists()

                if is_reg:  # 若查询有结果
                    print('login success')
                    request.session['is_login'] = True
                    # request.session['user_id'] = user_id
                    request.session['user_name'] = user_name
                    return redirect('/ShowItems')
                else:  # 若查询无结果，则用户名或密码错误
                    res['rlt'] = '用户名或密码错误'
                    return render(request, 'login.html', res)
            else:  # 若表中无该用户名数据，则未注册
                res['rlt'] = '该用户名未注册，请注册后登录'
                return render(request, 'login.html', res)
        elif  request.POST['reg1']:  # 处理表单中的注册，界面跳转
            return render(request, 'register.html')
        else:
            pass
    return render(request,'login.html',locals())



def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')

    elif request.method == 'POST':
        res = {}
        if 'reg2' in request.POST:
            username = request.POST.get('username')
            userid = request.POST.get('userid')
            password = request.POST.get('password')
            email = request.POST.get('email')

            tmp = User.objects.filter(user_id=userid).exists()
            if tmp:  # 若存在该用户名相关数据，则用户已注册
                res['rlt'] = '该用户名已注册,请登录'
                return render(request, 'register.html')

            else:  # 用户未注册，则向数据库中插入数据
                User.objects.create(user_id=userid,user_name=username, user_password=password,user_email=email)
                print('注册成功')
                res['rlt'] = '注册成功，请返回登录'
                return render(request, 'register.html', res)
        elif 'back' in request.POST:  # 处理返回，界面跳转
            return render(request, 'login.html')
        else:
            pass
        return render(request, 'register.html')



def logout(request):
    """登出"""
    # 清空session
    request.session.flush()
    return render(request,'login.html')


def Itemlist(request):
    data=Item.objects.values('item_id','item_name','item_price','item_class','item_content','item_score','img')
    # data=serializers.serialize('json',item)
    items={'items':data}
    return render(request,'ShowItems.html',items)
def recommend_list(request,):

    name=request.session['user_name']

    u=User.objects.get(user_name=name)

    user_id=u.user_id

    result=recommendProducts(user_id,50)
    books=result['data']
    p_book=[]
    filter_user_id=Score.objects.filter(user_id=user_id)

    for value in  filter_user_id:
        p_book.append(int(value.item_id))
    ls=[]
    for bk in books:
        bk_id=int(bk['item_id'])
        bk_sim=bk['similar']
        try:
            temp=Item.objects.get(item_id=bk_id)
            if temp.item_id not in p_book:
                dic_temp={}
                dic_temp['item_name']=temp.item_name
                dic_temp['item_price']=temp.item_price
                dic_temp['item_class']=temp.item_class
                dic_temp['item_score']=temp.item_score
                dic_temp['item_content']=temp.item_content
                dic_temp['img']=temp.img
                dic_temp['similar']=round(bk_sim,2)
                ls.append(dic_temp)
            #ls.append(temp)

        except:
            pass
    return render(request,'recommend.html',{'items':ls})
# #  评价
# def rate(request,):
#     result={}
#     book_id=request.POST.get('book_id')#获取前端传来的图书id
#     rate=request.POST.get('rate')#获取评分
#     name=request.session['user']#获取当前登录用户的名称
#     usr=user.objects.get(name=name)#查找用户
#     bk=book.objects.get(id=book_id)#查找图书
#     try:
#         if rating.objects.filter(user=usr,book=bk).count()>0:#判断是否已经评分
#             temp=rating.objects.get(user=usr,book=bk)#获取记录更新评分
#             temp.rate=rate
#             temp.save()
#     else:
#             temp=rating(user=usr,book=bk,rate=rate)#新增记录
#             temp.save()
#         result['state']=1
#         result['msg']='success'
#     except:
#         result['state']=0
#         result['msg']='failed'
#     return HttpResponse(json.dumps(result))#JsonResponse(result)
def evaluation(request,):
    user_name = request.session['user_name']
    user_value=User.objects.get(user_name=user_name)
    user_id=user_value.user_id
    print(user_name)
    print(type(user_id))
    # user_name = User.objects.get(user_name=user_name)
    item_id = request.POST['item_id']

    # goods_id = Goods.objects.get(goods_id=goods_id)
    item_name = request.POST['item_name']
    print(item_name)
    pf = int(request.POST.get('pf'))/10
    count = Score.objects.filter(user_id=user_id,item_id=item_id)
    if len(count) > 0:
        Score.objects.filter(user_id=user_id,item_id=item_id).update(item_score=pf)
    else:
        Score.objects.create(user_id=user_id, item_score=pf, item_id=item_id,item_name=item_name)
    return JsonResponse({"message": 1})
def visualize(request,):
    #价格前十
    price = Item.objects.values('item_price','item_name')
    num1 = pd.DataFrame.from_records(price)
    num= num1.sort_values(by="item_price", ascending=False,axis=0).head(10)  # 取前五
    item_price = list(num['item_price'])
    item_name = list(num['item_name'])
    #评分后商品
    objs = Score.objects.all()
    #价格占比
    data_list=[]
    data=Item.objects.all()
    for i in data:
        if int(i.item_price)>15:
            dic={"value":i.item_price,"name":i.item_name}
            data_list.append(dic)

    # #分类
    # conn = pymysql.connect(host='localhost', user='root', password='', db='secondhand')  # 建立数据库连接,data为数据库名
    # cur = conn.cursor()
    # sql = "select dict.item_class,sum(groupby(item_class)) from item"  # 联合查询
    # cur.execute(sql)  # 执行单条sql语句
    # total_rate = cur.fetchall()  # 接收全部的返回结果行
    # total_rate_df = pd.DataFrame(list(total_rate))  # 将执行结果转换为dataframe
    # total_rate_df.columns = ['name', 'value']
    # total_rate_dict = total_rate_df.to_dict(orient='records')

    return render(request, 'visualize.html', locals())
def already_evaluate(request):
    user_name = request.session['user_name']
    user_value = User.objects.get(user_name=user_name)
    user_id = user_value.user_id
    user_items=Score.objects.filter(user_id=user_id)
    ls=[]
    for user_item in user_items:
        item_dic = {}
        it_id=user_item.item_id
        item=Item.objects.get(item_id=it_id)
        item_dic['item_name'] = item.item_name
        item_dic['item_price'] = item.item_price
        item_dic['item_class'] = item.item_class
        item_dic['item_content'] = item.item_content
        item_dic['img'] = item.img
        item_dic['myscore'] = user_item.item_score
        ls.append(item_dic)
    return render(request, 'my_evaluate.html', {'items':ls})
