from django.db import models
from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model

class HomeInfo(models.Model):
    username = models.CharField(max_length=100, default='')
    logo_title = models.CharField(max_length=100, default='')
    full_name = models.CharField(max_length=100, default='')
    skill_title = models.CharField(max_length=100, default='')
    experience = models.PositiveIntegerField(default=0)
    image = models.URLField(max_length=700, blank=True, null=True)
    cv = models.URLField(max_length=700, blank=True, null=True)

    CV_MODE_CHOICES = [
        ('generated', 'Generated'),
        ('uploaded', 'Uploaded'),
    ]
    cv_mode = models.CharField(max_length=20, choices=CV_MODE_CHOICES, default='generated')

    CV_FORMAT_CHOICES = [
        ('pdf', 'PDF'),
        ('word', 'Word'),
    ]
    cv_format = models.CharField(
        max_length=10,
        choices=CV_FORMAT_CHOICES,
        default='pdf'
    )


    def __str__(self):
        return self.full_name


# ─────────────────────────────────────────────────────────────────
#  Add this model to your models.py
# ─────────────────────────────────────────────────────────────────

ALL_SECTIONS = [
    'summary', 'education', 'experience', 'skills',
    'certifications', 'achievements', 'projects',
]

DEFAULT_SECTIONS_VISIBLE = {s: True for s in ALL_SECTIONS}


class CVPreference(models.Model):
    username = models.CharField(max_length=100, unique=True)

    # ── File ──────────────────────────────────────────────
    file_name = models.CharField(max_length=100, blank=True, default='')
    # if blank, fallback = "{full_name}_CV"

    # ── Typography ────────────────────────────────────────
    font_family = models.CharField(max_length=50, default='Times New Roman')
    # allowed: 'Times New Roman', 'Helvetica', 'Georgia', 'Calibri', 'Garamond'

    font_size    = models.PositiveSmallIntegerField(default=12)   # 8–16
    line_spacing = models.FloatField(default=1.2)                 # 1.0–1.6

    # ── Colors (hex) ──────────────────────────────────────
    heading_color = models.CharField(max_length=7, default='#000000')
    text_color    = models.CharField(max_length=7, default='#000000')
    accent_color  = models.CharField(max_length=7, default='#000000')  # rules / bullets

    # ── Page setup ────────────────────────────────────────
    page_size = models.CharField(max_length=10, default='A4')  # 'A4' | 'Letter'

    margin_top    = models.FloatField(default=12)  # mm
    margin_bottom = models.FloatField(default=12)
    margin_left   = models.FloatField(default=13)
    margin_right  = models.FloatField(default=13)

    section_padding = models.FloatField(default=8)   # pt, space between sections

    # ── Sections ──────────────────────────────────────────
    sections_order   = models.JSONField(default=list)   # ordered list of section keys
    sections_visible = models.JSONField(default=dict)    # {key: bool}

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.sections_order:
            self.sections_order = ALL_SECTIONS.copy()
        if not self.sections_visible:
            self.sections_visible = DEFAULT_SECTIONS_VISIBLE.copy()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'CVPreference({self.username})'


class AboutInfo(models.Model):
    username = models.CharField(max_length=100, default='')
    s_one = models.CharField(max_length=100, default='')
    s_two = models.CharField(max_length=100, default='')
    projects = models.CharField(max_length=100, default='')
    education = models.CharField(max_length=100, default='')
    skill_pack = models.CharField(max_length=300, default='')
    image = models.URLField(max_length=700, blank=True, null=True)


class ProjectsInfo(models.Model):
    username = models.CharField(max_length=100, default='')
    p_name = models.CharField(max_length=100, default='')
    p_skills = models.CharField(max_length=100, default='')
    p_url = models.CharField(max_length=300, default='')
    image = models.URLField(max_length=700, blank=True, null=True)


class ProjectDetail(models.Model):
    project = models.OneToOneField(ProjectsInfo, on_delete=models.CASCADE, related_name='detail')
    intro = models.TextField(blank=True, default='')
    description = models.TextField(blank=True, default='')
    tech_stack = models.JSONField(default=list, blank=True)
    features = models.JSONField(default=list, blank=True)
    future = models.JSONField(default=list, blank=True)
    developer = models.TextField(blank=True, default='')
    extra_images = models.JSONField(default=list, blank=True)
    github_url = models.CharField(max_length=300, blank=True, default='')
    status = models.CharField(max_length=50, blank=True, default='')

    def __str__(self):
        return f"Detail → {self.project.p_name}"


class FooterInfo(models.Model):
    username = models.CharField(max_length=100, default='')
    full_name = models.CharField(max_length=100, default='')
    email = models.CharField(max_length=100, default='')
    c_title = models.CharField(max_length=100, default='')
    linkedin = models.CharField(max_length=100, default='')
    github = models.CharField(max_length=100, default='')
    whatsapp = models.CharField(max_length=100, default='')


class OTPVerification(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        return (timezone.now() - self.created_at).total_seconds() > 300  # 5 min

    def __str__(self):
        return f"{self.email} - {self.otp}"


class PortfolioVisit(models.Model):
    username = models.CharField(max_length=100)
    visited_at = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=100, blank=True, default='')
    device = models.CharField(max_length=50, blank=True, default='')
    browser = models.CharField(max_length=50, blank=True, default='')
    section = models.CharField(max_length=50, blank=True, default='home')

    def __str__(self):
        return f"{self.username} — {self.visited_at.strftime('%Y-%m-%d %H:%M')}"



User = get_user_model()

class PortfolioLink(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE, related_name='portfolio_link')
    slug       = models.SlugField(max_length=80, unique=True)

    def __str__(self):
        return f"{self.user.username} → {self.slug}"







class ProfileLinks(models.Model):
    """Contact info & social links — shown in CV header"""
    username      = models.CharField(max_length=100, unique=True)
    location      = models.CharField(max_length=150, blank=True, default='')
    phone         = models.CharField(max_length=20,  blank=True, default='')
    linkedin      = models.URLField(max_length=300,  blank=True, default='')
    github        = models.URLField(max_length=300,  blank=True, default='')
    portfolio_url = models.CharField(max_length=300, blank=True, default='')
    twitter       = models.URLField(max_length=300,  blank=True, default='')
    website       = models.URLField(max_length=300,  blank=True, default='')

    def __str__(self):
        return f'{self.username} — Links'


class ProfileSummary(models.Model):
    """Custom professional summary paragraph for CV"""
    username = models.CharField(max_length=100, unique=True)
    summary  = models.TextField(blank=True, default='')

    def __str__(self):
        return f'{self.username} — Summary'


class EducationInfo(models.Model):
    """Education entries — multiple per user"""
    username   = models.CharField(max_length=100)
    degree     = models.CharField(max_length=200, default='')
    cgpa       = models.CharField(max_length=20,  blank=True, default='')
    university = models.CharField(max_length=200, default='')
    location   = models.CharField(max_length=150, blank=True, default='')
    session    = models.CharField(max_length=50,  blank=True, default='')
    order      = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.username} — {self.degree}'


class ExperienceInfo(models.Model):
    """Work experience entries — multiple per user"""
    username = models.CharField(max_length=100)
    title    = models.CharField(max_length=200, default='')
    company  = models.CharField(max_length=200, default='')
    location = models.CharField(max_length=150, blank=True, default='')
    dates    = models.CharField(max_length=100, blank=True, default='')
    # Each bullet on a new line
    bullets  = models.TextField(blank=True, default='')
    order    = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.username} — {self.title} @ {self.company}'


class CertificationInfo(models.Model):
    """Certifications & courses"""
    username   = models.CharField(max_length=100)
    name       = models.CharField(max_length=200, default='')
    issuer     = models.CharField(max_length=200, blank=True, default='')
    date       = models.CharField(max_length=50,  blank=True, default='')
    verify_url = models.URLField(max_length=400,  blank=True, default='')

    def __str__(self):
        return f'{self.username} — {self.name}'


class AchievementInfo(models.Model):
    """Honours, awards, and achievements"""
    username    = models.CharField(max_length=100)
    title       = models.CharField(max_length=300, default='')
    description = models.TextField(blank=True, default='')

    def __str__(self):
        return f'{self.username} — {self.title}'


class LanguageSpoken(models.Model):
    """Spoken/written languages (English, Urdu etc.)"""
    PROFICIENCY_CHOICES = [
        ('Native',       'Native'),
        ('Fluent',       'Fluent'),
        ('Professional', 'Professional'),
        ('Intermediate', 'Intermediate'),
        ('Basic',        'Basic'),
    ]
    username    = models.CharField(max_length=100)
    language    = models.CharField(max_length=100, default='')
    proficiency = models.CharField(max_length=20,
                                   choices=PROFICIENCY_CHOICES,
                                   default='Professional')

    def __str__(self):
        return f'{self.username} — {self.language}'


class SoftSkillInfo(models.Model):
    """Soft skills — one row per skill"""
    username = models.CharField(max_length=100)
    skill    = models.CharField(max_length=100, default='')

    def __str__(self):
        return f'{self.username} — {self.skill}'


class HobbyInfo(models.Model):
    """Hobbies & interests"""
    username = models.CharField(max_length=100)
    hobby    = models.CharField(max_length=150, default='')

    def __str__(self):
        return f'{self.username} — {self.hobby}'


