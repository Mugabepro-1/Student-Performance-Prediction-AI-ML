from rest_framework import serializers
from .models import StudentPerformance


class StudentPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentPerformance
        fields = '__all__'


class PredictionInputSerializer(serializers.Serializer):
    hours_studied = serializers.FloatField(min_value=0.0, max_value=24.0)
    previous_scores = serializers.FloatField(min_value=0.0, max_value=100.0)
    extracurricular = serializers.BooleanField()
    sleep_hours = serializers.FloatField(min_value=0.0, max_value=24.0)
    sample_papers = serializers.IntegerField(min_value=0)

    def validate(self, data):
        # Additional cross-field validation if needed
        # Example: warn if both hours_studied and sample_papers are zero
        if data.get('hours_studied', 0) == 0 and data.get('sample_papers', 0) == 0:
            raise serializers.ValidationError(
                "At least one of 'hours_studied' or 'sample_papers' should be greater than 0."
            )

        # Realistic daily time constraint: studying + sleep + extracurricular shouldn't exceed a sane total.
        # We'll assume extracurricular activities take ~2 hours per day when selected.
        hours_studied = float(data.get('hours_studied', 0))
        sleep_hours = float(data.get('sleep_hours', 0))
        extracurricular = bool(data.get('extracurricular', False))
        extra_time = 2.0 if extracurricular else 0.0

        total_allocated = hours_studied + sleep_hours + extra_time
        # Enforce that these three don't exceed 20 hours to leave time for other life activities
        if total_allocated > 20.0:
            raise serializers.ValidationError(
                f"The sum of hours_studied ({hours_studied}), sleep_hours ({sleep_hours}) and extracurricular (~{extra_time}) "
                f"is {total_allocated:.1f} which exceeds a recommended daily allocation of 20 hours. "
                "Please adjust values so they add up to 20 hours or less."
            )

        return data