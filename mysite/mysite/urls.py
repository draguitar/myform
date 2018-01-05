"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from blog.views import hello_world

from signup.views import sign_up
from signup.views import login
from signup.views import registration
from signup.views import profile
from signup.views import logout

from forum.views import go_forum
from forum.views import topic
from forum.views import new_post
from forum.views import save_post
from forum.views import save_reply

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_world),
    path('signup/', sign_up),
    path('forum/', go_forum),
    path('topic/',topic),
    path('topic/new/',new_post),
    path('topic/save/',save_post),
    path('topic/save_reply/',save_reply),

    path('login/',login),
    path('logout/',logout),
    path('registration/',registration),
    path('profile/',profile),
]
