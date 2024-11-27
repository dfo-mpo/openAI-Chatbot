from django.urls import path
from . import views
from CSV_PDF_Analyzer_App.views import demo_home
from PDF_Chatbot_App.views import french
from main_app.views import fence, scale, upload_video, analyze_sensitivity
urlpatterns = [
    path('', views.home, name='home'),  
    path('banner-image/', views.banner_image, name='banner-image'),
    path('demo_home/', demo_home, name = 'demo_home'),
    # path('french/', french, name = 'french'),
    path('fence/', fence, name = 'fence'),
    path('scale/', scale, name = 'scale'),
    path('upload_video/', upload_video, name = 'upload_video'),
    path('analyze_sensitivity/', analyze_sensitivity, name = 'analyze_sensitivity'),




]
