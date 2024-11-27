from django.urls import path
from django.contrib import admin
from PDF_Chatbot_App.views import chat_home, translation_home, chatbot_view_translate
from django.conf import settings
from django.conf.urls.static import static


from PDF_Chatbot_App.views import chatbot_view, upload_document,upload_document_translation, chat, banner_image, refine_content, overview, chatfrench

urlpatterns = [
    path('chat_home/', chat_home, name='chat_home'),
    path('translation_home/', translation_home, name='translation_home'),
    path('translation_upload/', upload_document_translation, name='upload_document_translation'),
    path('chat_upload/', upload_document, name='upload_document'),
    path('overview', overview, name='overview'),
    path('chat/', chat, name='chat'),
    path('chatfrench/', chatfrench, name='chatfrench'),
    path('chatbot/', chatbot_view, name='chatbot'),
    path('translatebot/', chatbot_view_translate, name='translatebot'),
    path('banner-image/', banner_image, name='banner-image'),
    path('refine_content/', refine_content, name='refine_content')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)