from django.urls import path
from CSV_PDF_Analyzer_App import views

urlpatterns = [
    path('demo_home', views.demo_home, name='demo_home'),  # Home page
    path('gif-image/', views.giphy_image, name='gif-image'),
    path('gif-image2/', views.giphy_image2, name='gif-image2'),
    path('gif-image3/', views.giphy_image3, name='gif-image3'),

    path('upload/', views.OpenAIView.as_view(), name='upload'),  # Upload page, using the existing OpenAIView
    # Uncomment the next line when you're ready to implement the export functionality
    # path('openai/export/', views.OpenAIExportView.as_view(), name='export_openai_data'),
]
