from pyexpat import features
from urllib import request
from django.shortcuts import render
import joblib
import numpy as np
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PredictionInputSerializer


# Load model once at import-time
model = joblib.load('performance/model.pkl')


def _generate_recommendations(validated_data, prediction):
    """Generate actionable recommendations and tips based on input and prediction."""
    recs = []
    tips = []

    hs = float(validated_data['hours_studied'])
    prev = float(validated_data['previous_scores'])
    ext = bool(validated_data['extracurricular'])
    sleep = float(validated_data['sleep_hours'])
    papers = int(validated_data['sample_papers'])

    # Hours studied
    if hs < 1:
        recs.append('Increase daily study time. Start with at least 1–2 hours focused study and build up.')
    elif hs < 3:
        recs.append('Good start — try focused study sessions of 25–50 minutes with short breaks (Pomodoro).')
    else:
        recs.append('Strong study habit. Keep consistency and add targeted practice on weak areas.')

    # Previous scores
    if prev < 50:
        recs.append('Previous scores are low — consider guided tutoring and topic-wise revision.')
        tips.append('Focus on fundamentals first; use spaced repetition for difficult topics.')
    elif prev < 75:
        recs.append('Moderate previous scores — prioritise past-paper practice and error analysis.')

    # Extracurricular balance
    if ext:
        recs.append('Extracurricular activities can boost skills. Ensure you balance time and avoid last-minute cramming.')
    else:
        recs.append('Consider light extracurricular activities to improve time-management and reduce stress.')

    # Sleep
    if sleep < 6:
        recs.append('Increase nightly sleep to 7–9 hours for better memory consolidation.')
    elif sleep > 10:
        recs.append('Very long sleep might indicate inconsistent schedule — aim for consistent 7–9 hours.')

    # Sample papers
    if papers == 0:
        recs.append('Start practicing sample papers — begin with 2–3 timed papers per week to build exam stamina.')
    elif papers < 5:
        recs.append('Increase frequency of timed sample papers and review mistakes in detail.')

    # Prediction-based suggestions
    try:
        p = float(prediction)
        if p < 50:
            recs.append('Predicted performance is low — consider an action plan: tutoring, mock tests, and focused revision.')
        elif p < 75:
            recs.append('Predicted performance is moderate — address weak topics and increase timed practice.')
        else:
            recs.append('Predicted performance looks strong — maintain current routine and target advanced practice.')
    except Exception:
        pass

    # Engineering / data tips to improve future predictions
    tips.append('Instead of cramming, review material at increasing intervals over several days or weeks.')
    tips.append('Test yourself frequently rather than just re-reading notes. Use flashcards or create your own practice quizzes.')

    return {'recommendations': recs, 'tips': tips}


@api_view(['POST'])
def predict_performance(request):
    serializer = PredictionInputSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'errors': serializer.errors}, status=400)

    validated = serializer.validated_data

    features = np.array([[
        validated['hours_studied'],
        validated['previous_scores'],
        1 if validated['extracurricular'] else 0,
        validated['sleep_hours'],
        validated['sample_papers'],
    ]])

    prediction = model.predict(features)[0]

    recs = _generate_recommendations(validated, prediction)

    return Response({
        'predicted_performance_index': round(float(prediction), 2),
        'recommendations': recs['recommendations'],
        'tips': recs['tips']
    })