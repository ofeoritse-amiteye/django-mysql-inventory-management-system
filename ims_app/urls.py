from django.contrib import admin
from django.urls import path,include
from ims import settings
from ims_app import views
from django.conf.urls.static import static


urlpatterns = [
    path("",views.login_user),
    path("login",views.login_user),
    path("add_user",views.add_user),
    path('index',views.index),
    path('dashboard',views.dashboard),
    path('signout',views.signout),
    path('analysis', views.analytics),
    path('update/<id>',views.update, name='update'),
    path('updated/<batch_number>',views.updated,name='updated'),
    path('delete/<id>',views.delete,name='delete'),
    path('delete2/<number>',views.delete2,name='delete'),
    path('category',views.category),
    path('report',views.report),
    path('add_user',views.add_user),
    path('index', views.index),
    path('update_description',views.update_description),
    path('category/products/', views.get_category_products, name='get_category_products'),
    path('search',views.search),
    path('print/<id>',views.printc),
    path('product_details/<id>',views.p_details)
    
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)