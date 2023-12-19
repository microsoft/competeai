"""
URL configuration for restaurant_sys project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from menu import views as menu_views
from chef import views as chef_views
from advertisement import views as advertisement_views
from basic_info import views as basic_info_views
from comment import views as comment_views
from daybook import views as daybook_views

from basic_info.views import Show
from menu.views import get_score_per_dish
from comment.views import get_last_comment

router = routers.DefaultRouter()

router.register(r"menu", menu_views.MenuViewSet, basename="menu")
router.register(r"chef", chef_views.ChefViewSet, basename="chef")
router.register(r"advertisement", advertisement_views.AdvertisementViewSet, basename="advertisement")
router.register(r"basic_info", basic_info_views.BasicInfoViewSet, basename="basic_info")
router.register(r"comment", comment_views.CommentViewSet, basename="comment")
router.register(r"daybook", daybook_views.DayBookViewSet, basename="daybook")

urlpatterns = [
    path('', include(router.urls)),
    path('show/', Show, name="show"),
    path('score/', get_score_per_dish, name="score"),
    path('last_comment/', get_last_comment, name="last_comment"),
    path("admin/", admin.site.urls),
]
