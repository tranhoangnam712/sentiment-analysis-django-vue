from rest_framework import serializers
from django.utils import timezone
from .models import AnalysisLog

class AnalysisLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisLog
        fields = '__all__'
