from django import forms
from CSV_PDF_Analyzer_App.models import CSVUpload

class CSVUploadForm(forms.ModelForm):
    class Meta:
        model = CSVUpload
        fields = ('csv_file',)