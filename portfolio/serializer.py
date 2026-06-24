from rest_framework import serializers
from .models import HomeInfo, FooterInfo, ProjectsInfo, AboutInfo, OTPVerification, PortfolioLink
from .models import ProjectDetail

class HomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeInfo
        fields = '__all__'


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutInfo
        fields = '__all__'


class FooterSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterInfo
        fields = '__all__'


class ProjectsSerializer(serializers.ModelSerializer):
    image = serializers.URLField(required=False, allow_null=True)

    class Meta:
        model = ProjectsInfo
        fields = '__all__'



class ProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ProjectDetail
        fields = '__all__'


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPVerification
        fields = ['email', 'otp', 'is_verified']



class PortfolioLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model  = PortfolioLink
        fields = ['id', 'slug']






# ─────────────────────────────────────────────────────────────
#  ADD THESE TO YOUR serializer.py
# ─────────────────────────────────────────────────────────────

from .models import (
    ProfileLinks, ProfileSummary,
    EducationInfo, ExperienceInfo, CertificationInfo,
    AchievementInfo, LanguageSpoken, SoftSkillInfo, HobbyInfo,
)


class ProfileLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ProfileLinks
        fields = '__all__'


class ProfileSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model  = ProfileSummary
        fields = '__all__'


class EducationInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = EducationInfo
        fields = '__all__'


class ExperienceInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ExperienceInfo
        fields = '__all__'


class CertificationInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = CertificationInfo
        fields = '__all__'


class AchievementInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = AchievementInfo
        fields = '__all__'


class LanguageSpokenSerializer(serializers.ModelSerializer):
    class Meta:
        model  = LanguageSpoken
        fields = '__all__'


class SoftSkillInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = SoftSkillInfo
        fields = '__all__'


class HobbyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = HobbyInfo
        fields = '__all__'



class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeInfo
        fields = ['cv_mode', 'cv_format']


from rest_framework import serializers
from .models import CVPreference, ALL_SECTIONS


class CVPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CVPreference
        fields = [
            'file_name',
            'font_family', 'font_size', 'line_spacing',
            'heading_color', 'text_color', 'accent_color',
            'page_size',
            'margin_top', 'margin_bottom', 'margin_left', 'margin_right',
            'section_padding',
            'sections_order', 'sections_visible',
        ]

    # ── Validation guardrails ──────────────────────────────
    def validate_font_size(self, value):
        if not (8 <= value <= 16):
            raise serializers.ValidationError('Font size must be between 8 and 16pt.')
        return value

    def validate_line_spacing(self, value):
        if not (1.0 <= value <= 1.6):
            raise serializers.ValidationError('Line spacing must be between 1.0 and 1.6.')
        return value

    def validate_margin_top(self, value):
        return self._check_margin(value)

    def validate_margin_bottom(self, value):
        return self._check_margin(value)

    def validate_margin_left(self, value):
        return self._check_margin(value)

    def validate_margin_right(self, value):
        return self._check_margin(value)

    def _check_margin(self, value):
        if not (5 <= value <= 25):
            raise serializers.ValidationError('Margins must be between 5mm and 25mm.')
        return value

    def validate_section_padding(self, value):
        if not (2 <= value <= 24):
            raise serializers.ValidationError('Section padding must be between 2pt and 24pt.')
        return value

    def validate_font_family(self, value):
        allowed = {'Times New Roman', 'Helvetica', 'Georgia', 'Calibri', 'Garamond'}
        if value not in allowed:
            raise serializers.ValidationError(f'Font must be one of: {", ".join(allowed)}.')
        return value

    def validate_page_size(self, value):
        if value not in ('A4', 'Letter'):
            raise serializers.ValidationError('Page size must be A4 or Letter.')
        return value

    def validate_sections_order(self, value):
        if sorted(value) != sorted(ALL_SECTIONS):
            raise serializers.ValidationError('sections_order must contain exactly the known sections.')
        return value

    def validate_sections_visible(self, value):
        if not set(value.keys()).issubset(set(ALL_SECTIONS)):
            raise serializers.ValidationError('sections_visible has unknown section keys.')
        return value

    def _validate_hex(self, value, field):
        import re
        if not re.match(r'^#[0-9A-Fa-f]{6}$', value):
            raise serializers.ValidationError(f'{field} must be a valid hex color, e.g. #1a1a1a.')
        return value

    def validate_heading_color(self, value):
        return self._validate_hex(value, 'heading_color')

    def validate_text_color(self, value):
        return self._validate_hex(value, 'text_color')

    def validate_accent_color(self, value):
        return self._validate_hex(value, 'accent_color')
