from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('main_app.urls')),
    path('admin/', admin.site.urls),
    path('', include('PDF_Chatbot_App.urls')),
    path('', include('CSV_PDF_Analyzer_App.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)