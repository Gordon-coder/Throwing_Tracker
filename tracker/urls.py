import django.urls
from tracker import views

urlpatterns = [
    django.urls.path('', views.index, name='index'),
]