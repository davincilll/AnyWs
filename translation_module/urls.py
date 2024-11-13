from django.urls import path

from translation_module.views import translate

app_name = 'translation_module'
urlpatterns = [
    path('translate/', translate, name='translate'),

]
