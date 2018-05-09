import json
from django.core.serializers.json import DjangoJSONEncoder
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render

# 序列化  生产json数据
# 反序列化  ---解析json数据
from home.models import Product, User, Category, CategorySub1, Banner, CategorySub, ProductImage, BaseModel


def index(request):
    return render(request, 'index.html', {})


def get_head_data(request):
    return


# 前后端分离 返回的不是模板 而是json\数据
def get_search_shop(request):
    result = {}
    try:
        keywords = request.GET.get('key')
        products = Product.objects.filter(name__contains=keywords)
        li = []
        for product in products:
            product.img_list = product.qs_to_dict(ProductImage.objects.filter(pid=product.id))
            li.append(product.to_dict())
        result.update(state=200, msg='成功', data=li)
    except BaseException as e:
        result.update(state=-1, msg='失败')
    return HttpResponse(json.dumps(result), content_type='Application/json')


def get_shop_shop(request):
    # 返回值
    result = {}
    try:
        # 从前端发送的请求中获取的查询关键字
        keywords = request.GET.get('key')
        # 通过条件查询出 所有包含 keywords 的数据
        products = Product.objects.filter(name__contains=keywords)
        li = []
        #     查询的结果返回的是一个 queryset 对象(是一个list 嵌套 qs对象 的格式) 所以需要遍历 得到每一条的qs对象
        # 然后才能通过 qs对象.字段 方式,
        for product in products:
            # 通过查询 结果里的product 的id 我们可以得到对应的 图片表 里的pid,因为这两个表中 product是图片表的主表
            # product.imgs_list 是相当于用一个qs对像 也是表里面的每一行(也就是每一条记录) 来 .
            # 就相当于虚拟的来创建一个 字段(也就是列),也在返回的json 中创建一个对象(也就是字典)
            # 因为ProductImage 图片表通过id 取出来的数据又是一个qs对象 所以为了使数据能够直接能被前端获取
            # 我们需要把qs对象转化为字典对象 qs_to_dict(这是自己封装的工具类)
            product.imgs_list = product.qs_to_dict(ProductImage.objects.all(pid=product.id))
            # 从products里面取出来product也是一个qs对象的字典,也要直接转化为字典类型,然后把所有的符合的数据加入列表,
            # 传入li返回到前端
            li.append(product.to_dict())
            # 返回到前端
        result.update(state=200, msg='成功', data=li)
    except BaseException as e:
        result.update(state=-1, msg='失败')
    #     前端是ajax获取数据,要转化为json数据,让前端能够获取,ajax 能够直接解析ajax的数据,如果不转化成接送数据,
    #   那么返回的数据就会一个地址,而不是想要获取的数据
    return HttpResponse(json.dumps(result), content_type='Application/json')


def get_category_data(request):
    result = {}
    try:
        # 这里获取的也是qs对象,获取的是[{},{}...] 形式的列表套这qs对象
        cate_list = Category.objects.all()
        # 这个也是一样的,把这个列表套qs对象转为列表嵌套字典
        banners = Banner.qs_to_dict(Banner.objects.all())
        # 将转化为列表嵌套字典了的格式,直接返回到前端 作为一个json数组
        result.update(banners=banners)
        li = []
        for cate in cate_list:
            sub_list = CategorySub1.objects.filter(cid=cate.id)
            # 这里的cate 相当于一个变量 ,只要是有qs_to_dict() 都行,并且工具类是设置的静态方法,所以都能用
            cate.subs = cate.qs_to_dict(sub_list)
            li.append(cate.to_dict())
        result.update(state=200, msg='成功', data=li)
    except BaseException as e:
        result.update(state=-1, msg='失败')
    return HttpResponse(json.dumps(result), content_type='Application/json')


def get_shop_data(request):
    result = {}
    li = []
    try:
        cates = Category.objects.all()

        for cate in cates:
            products = cate.product_set.all()
            for product in products:
                product.imgs = BaseModel.qs_to_dict(product.product_image.all())
            cate.products = BaseModel.qs_to_dict(products)
            li.append(cate.to_dict())
        result.update(state=200, msg='success', data=li)
    except:
        result.update(state=-1, msg='失败')
    return HttpResponse(json.dumps(result), content_type='Application/json')


def login(request):
    try:
        if request.method == 'GET':
            username = request.GET.get('username')
            password = request.GET.get('password')
            if User.objects.filter(name=username, password=password):
                return HttpResponse('登陆成功')
            else:
                return HttpResponse('账号或密码错误')
    except:
        return HttpResponse('网络错误')
    return render(request, 'index.html')


def register(request):
    try:
        if request.method == 'GET':
            username = request.GET.get('username')
            email = request.GET.get('email')
            password = request.GET.get('password')
            icon_password = request.GET.get('icon_password')

            user = User()
            if User.objects.filter(name=username):
                return HttpResponse('该用户已存在')
            else:
                user.name = username
                user.email = email
                user.password = password
                user.icon = icon_password
                if icon_password == password:
                    user.save()
                    return HttpResponse('注册成功')
                else:
                    return HttpResponse('两次密码不一致')
    except:
        return HttpResponse('网络错误')
    return render(request, 'index.html')


def show_cate(request):
    cate_list = Category.objects.all()
    for cate in cate_list:
        cate_sub_list = CategorySub1.objects.filter(cid=cate.id)
        cate.cate = cate_sub_list

    content = {
        'cate_list': cate_list,
    }
    return render(request, 'cate.html', content)
