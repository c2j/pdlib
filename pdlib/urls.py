from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
#from django.contrib import admin
#admin.autodiscover()

#from horizon_client.views import retrieve

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pdlib.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),

    url(r"^$", TemplateView.as_view(template_name="pdlib/index.html"), name="home"),
    url(r'^retrieve/$', 'horizon_client.views.retrieve', name='retrieve'),
    url(r'^detail/$', 'horizon_client.views.detail', name='detail'),
)




