from rest_framework import serializers
from datetime import datetime, date
from calendar import monthrange

class AgeSerializer(serializers.Serializer):
    birth_date = serializers.DateField()

    def validate_birth_date(self, value):
        if value > datetime.today().date():
            raise serializers.ValidationError("Birth date cannot be in the future.")
        return value

    def to_representation(self, instance):
        birth_date = instance['birth_date']
        today = datetime.today().date()

        # ----- Accurate Age Calculation -----
        years = today.year - birth_date.year
        months = today.month - birth_date.month
        days = today.day - birth_date.day

        if days < 0:
            months -= 1
            prev_month = today.month - 1 if today.month > 1 else 12
            prev_year = today.year if today.month > 1 else today.year - 1
            days += monthrange(prev_year, prev_month)[1]  # Days in prev month

        if months < 0:
            years -= 1
            months += 12

        # ----- Next Birthday Calculation -----
        next_birthday_year = today.year
        if (today.month, today.day) >= (birth_date.month, birth_date.day):
            next_birthday_year += 1

        # Handle Feb 29 birthdays in non-leap years
        try:
            next_birthday = date(next_birthday_year, birth_date.month, birth_date.day)
        except ValueError:
            next_birthday = date(next_birthday_year, 3, 1)  # Shift to March 1

        # Total countdown days & seconds
        remaining_days_total = (next_birthday - today).days
        remaining_seconds_total = remaining_days_total * 24 * 60 * 60

        # Convert remaining days to months + days (exact)
        rem_months = 0
        rem_days = 0
        temp_date = today

        while True:
            if temp_date.month == next_birthday.month and temp_date.year == next_birthday.year:
                rem_days = (next_birthday - temp_date).days
                break

            days_in_current_month = monthrange(temp_date.year, temp_date.month)[1]
            rem_months += 1
            temp_date = date(
                temp_date.year + (temp_date.month // 12),
                (temp_date.month % 12) + 1,
                1
            )

        return {
            "years": years,
            "months": months,
            "days": days,
            "next_birthday_in": f"{rem_months} months {rem_days} days",
            "next_birthday_countdown_days": remaining_days_total,
            "next_birthday_countdown_seconds": remaining_seconds_total
        }
