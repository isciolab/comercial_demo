from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

from experience import views as experience_views ##le coloco alias para poder llamar distintas vistas
from calls import views  as calls_views #le coloco alias para poder llamar distintas vistas

urlpatterns = [
    url(r'^$',  login_required(TemplateView.as_view(template_name='home.html'), 'login', 'login'), name='home'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='logged_out.html'), name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^experience/register', experience_views.RegisterExperience),
    url(r'^experience/getexpandcalls', experience_views.getExpAndCalls),
    url(r'^custom_login', experience_views.custom_login),
    url(r'^calls/getCalls', calls_views.getCalls),
    url(r'^calls/registerCall', calls_views.registerCall)

]
