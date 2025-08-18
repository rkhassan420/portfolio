# from rest_framework import serializers
# from datetime import datetime, date, timedelta
# from calendar import monthrange
#
# class AgeSerializer(serializers.Serializer):
#     birth_date = serializers.DateField()
#
#     def validate_birth_date(self, value):
#         if value > datetime.today().date():
#             raise serializers.ValidationError("Birth date cannot be in the future.")
#         return value
#
#     def to_representation(self, instance):
#         birth_date = instance['birth_date']
#         today = datetime.today().date()
#
#         # ---------- Accurate AGE ----------
#         years = today.year - birth_date.year
#         months = today.month - birth_date.month
#         days = today.day - birth_date.day
#
#         if days < 0:
#             months -= 1
#             prev_month = today.month - 1 if today.month > 1 else 12
#             prev_year = today.year if today.month > 1 else today.year - 1
#             days += monthrange(prev_year, prev_month)[1]
#
#         if months < 0:
#             years -= 1
#             months += 12
#
#         # ---------- Next Birthday ----------
#         next_birthday_year = today.year
#         if (today.month, today.day) >= (birth_date.month, birth_date.day):
#             next_birthday_year += 1
#
#         try:
#             next_birthday = date(next_birthday_year, birth_date.month, birth_date.day)
#         except ValueError:  # Leap day handling
#             next_birthday = date(next_birthday_year, 3, 1)
#
#         # ----- QUICK TEST (uncomment to force 2 mins left) -----
#         # next_birthday = today + timedelta(minutes=2)
#
#         # Countdown
#         remaining_days_total = (next_birthday - today).days
#         remaining_seconds_total = int((next_birthday - datetime.now().date()).days * 86400 +
#                                       (datetime.combine(next_birthday, datetime.min.time()) - datetime.now()).total_seconds())
#
#         # Months/days until next birthday
#         nb_years = next_birthday.year - today.year
#         nb_months = next_birthday.month - today.month
#         nb_days = next_birthday.day - today.day
#
#         if nb_days < 0:
#             nb_months -= 1
#             prev_month = next_birthday.month - 1 if next_birthday.month > 1 else 12
#             prev_year = next_birthday.year if next_birthday.month > 1 else next_birthday.year - 1
#             nb_days += monthrange(prev_year, prev_month)[1]
#
#         if nb_months < 0:
#             nb_years -= 1
#             nb_months += 12
#
#         return {
#             "years": years,
#             "months": months,
#             "days": days,
#             "next_birthday_in": f"{nb_months} months {nb_days} days",
#             "next_birthday_countdown_days": remaining_days_total,
#             "next_birthday_countdown_seconds": max(0, remaining_seconds_total)
#         }


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

        # ---------- Accurate AGE ----------
        years = today.year - birth_date.year
        months = today.month - birth_date.month
        days = today.day - birth_date.day

        if days < 0:
            months -= 1
            prev_month = today.month - 1 if today.month > 1 else 12
            prev_year = today.year if today.month > 1 else today.year - 1
            days += monthrange(prev_year, prev_month)[1]

        if months < 0:
            years -= 1
            months += 12

        # ---------- Next Birthday ----------
        next_birthday_year = today.year
        if (today.month, today.day) >= (birth_date.month, birth_date.day):
            next_birthday_year += 1

        try:
            next_birthday = date(next_birthday_year, birth_date.month, birth_date.day)
        except ValueError:  # Leap day handling
            next_birthday = date(next_birthday_year, 3, 1)

        # Months/days until next birthday
        nb_months = next_birthday.month - today.month
        nb_days = next_birthday.day - today.day

        if nb_days < 0:
            nb_months -= 1
            prev_month = next_birthday.month - 1 if next_birthday.month > 1 else 12
            prev_year = next_birthday.year if next_birthday.month > 1 else next_birthday.year - 1
            nb_days += monthrange(prev_year, prev_month)[1]

        if nb_months < 0:
            nb_months += 12

        # ---------- Countdown ----------
        now = datetime.now()
        next_birthday_datetime = datetime.combine(next_birthday, datetime.min.time())
        total_seconds = max(0, int((next_birthday_datetime - now).total_seconds()))

        days_left = total_seconds // 86400
        hours_left = (total_seconds % 86400) // 3600
        minutes_left = (total_seconds % 3600) // 60
        seconds_left = total_seconds % 60

        return {
            "years": years,
            "months": months,
            "days": days,
            "next_birthday_in": f"{nb_months} months {nb_days} days",
            "next_birthday_countdown": {
                "days": days_left,
                "hours": hours_left,
                "minutes": minutes_left,
                "seconds": seconds_left
            }
        }
