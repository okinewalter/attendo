from django.urls import path
from . import views

app_name = 'record' 
urlpatterns = [
    path('create/', views.create_record, name='create_record'),
    path('update/<int:record_id>/', views.update_record, name='update_record'),
    path('complete/<int:record_id>/', views.complete_record, name='complete_record'),
    path('delete/<int:record_id>/', views.delete_record, name='delete_record'),
    path('generate_report/', views.generate_report, name='generate_report'),
    path('', views.record_list, name='record_list'),
]
