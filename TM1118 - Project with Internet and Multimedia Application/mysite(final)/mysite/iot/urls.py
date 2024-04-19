from django.urls import path
from . import views

urlpatterns = [
    path('', views.log),
    path('info/', views.info),
    path('data/', views.data),
    path('hour_analysis/', views.hour_analysis_page),
    path('node_analysis/', views.node_analysis_page),
    path('second_analysis/', views.second_analysis_page),
    path('temp_data', views.temp_data, name='temp_data'),
    path('hour_analysis_data',views.hour_analysis_data, name = 'hour_analysis_data'),
    path('second_analysis_data',views.second_analysis_data, name = 'second_analysis_data'),
    path('nav_bar/', views.navbar),
    path('dataWarning/',views.data_warning),
]