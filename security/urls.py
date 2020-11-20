"""Security Urls"""

# Django

from django.urls import path

# Views
import security.views as security
import security.business.views as Bussiness

urlpatterns = [
    path(route='', view=security.HomeView.as_view(), name='home'),
    path(route='profile/', view=security.ProfileView.as_view(), name='profile'),
    path(route='login/', view=security.LoginView.as_view(), name='login'),
    path(route='logout/', view=security.LogoutView.as_view(), name='logout'),
    path(route='register/', view=security.RegisterView.as_view(), name='register'),
    path(route='setting/bussiness/<pk>',view=Bussiness.Update.as_view(),name='setting.update'),
    path(route='setting/bussiness/',view=Bussiness.Create.as_view(),name='setting.store'),
    #path('dashboard/',security.Filterdashboard,name='dashboard')

]


