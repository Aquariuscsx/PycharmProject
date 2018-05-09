from django.conf.urls import url



from home import views

urlpatterns = [
    url('search/', views.get_search_shop),
    url('login/', views.login),
    url('register/', views.register),
    url('show/', views.show_cate),
    url('cate/', views.get_category_data),
    url('shops/', views.get_shop_data),

]
