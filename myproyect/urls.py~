from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings
import os

admin.autodiscover()

path = os.getcwd()
pathAbs = path + "/RedTie/images/tie_logo.gif"

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^annotated/$', 'cms_users_put.views.authenticatedAnnotated'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^nuevo_usuario$', 'cms_users_put.views.signUp'),
    url(r'^inicio_sesion$', 'cms_users_put.views.signIn'),
    url(r'^cerrar_sesion$', 'cms_users_put.views.logOut'),
    url(r'^annotated/images/style.css$', 'cms_users_put.views.css'),
    url(r'^annotated/images/?P<path>.*$','django.views.static.serve',
       {'document_root': pathAbs}),
    url(r'^annotated/images/bg_submenu.gif$', 'cms_users_put.views.css'),
    url(r'^annotated/images/bg_menu.gif$', 'cms_users_put.views.css'),
    url(r'\w*', 'cms_users_put.views.authenticated'),
)
