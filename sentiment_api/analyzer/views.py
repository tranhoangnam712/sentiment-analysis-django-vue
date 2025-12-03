from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import AnalysisLog
from .serializers import AnalysisLogSerializer
from .sentiment_model import predict_sentiment

@api_view(["POST"])
def analyze(request):
    text = request.data.get("text", "")
    if not text.strip():
        return Response({"error": "Text is required"}, status=400)
    try:
        pred = predict_sentiment(text)
    except ValueError as e:
        return Response({"error": str(e)}, status=400)

    log = AnalysisLog.objects.create(text=text, prediction=pred)

    return Response({"text": text, "prediction": pred, "id": log.id})


@api_view(["GET"])
def history(request):
    logs = AnalysisLog.objects.all().order_by("-created_at")
    serializer = AnalysisLogSerializer(logs, many=True)
    return Response(serializer.data)
