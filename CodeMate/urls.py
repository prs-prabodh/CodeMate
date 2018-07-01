# url in browser is matched with the patterns below and
# a matching function or class is instigated

from django.urls import path
from django.conf.urls import url
from . import views

app_name='code'

urlpatterns=[
    path('',views.index,name='index'),
    path('create/',views.createView,name='create'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.logIn,name='logIn'),
    path('logout/',views.logOut,name='logOut'),
    path('loggedIn/',views.loggedIn,name='loggedIn'),
    path('create/addObject/',views.addObject,name='addObject'),
    path('loggedIn/addObject/',views.addObject,name='addObject'),
    path('signup/validUser/',views.validUser,name='validUser'),
    path('login/authUser/',views.authUser,name='authUser'),
    path('login/failed/',views.loginFailure,name='loginFailure'),
    path('paste/<slug:slug>',views.details.as_view(),name='details'),
    path('paste/<slug:slug>/modify',views.modify,name='modify'),
    path('paste/<slug:slug>/delete',views.deleteView.as_view(),name='delete'),
]
