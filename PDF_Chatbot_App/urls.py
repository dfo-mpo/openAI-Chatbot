from django.urls import path
from django.contrib import admin
from PDF_Chatbot_App.views import french 
from django.conf import settings
from django.conf.urls.static import static


from PDF_Chatbot_App.views import chatbot_view, upload_document, chat, banner_image, refine_content, overview

urlpatterns = [
    # path('french/', french, name='french'),
    path('chat_upload/', upload_document, name='upload_document'),
    path('overview', overview, name='overview'),
    # path('chat/', chat, name='chat'),

    path('chatbot/', chatbot_view, name='chatbot'),
    path('banner-image/', banner_image, name='banner-image'),
    path('refine_content/', refine_content, name='refine_content')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)