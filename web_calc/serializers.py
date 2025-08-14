from rest_framework import serializers
from datetime import datetime
from django.utils.timezone import now

class AgeSerializer(serializers.Serializer):
    birth_date = serializers.DateField()

    def validate_birth_date(self, value):
        if value > datetime.today().date():
            raise serializers.ValidationError("Birth date cannot be in the future.")
        return value

    def to_representation(self, instance):
        birth_date = instance['birth_date']
        today = datetime.today().date()


        # Calculate years, months, and days
        years = today.year - birth_date.year
        months = today.month - birth_date.month
        days = today.day - birth_date.day

        if days < 0:
            months -= 1
            days += 30  # Approximation

        if months < 0:
            years -= 1
            months += 12

        return {
            "years": years,
            "months": months,
            "days": days,

        }
