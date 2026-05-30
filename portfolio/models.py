from django.db import models
from django.utils import timezone


class HomeInfo(models.Model):
    username = models.CharField(max_length=100, default='')
    logo_title = models.CharField(max_length=100, default='')
    full_name = models.CharField(max_length=100, default='')
    skill_title = models.CharField(max_length=100, default='')
    experience = models.PositiveIntegerField(default=0)
    image = models.URLField(max_length=700, blank=True, null=True)
    cv = models.URLField(max_length=700, blank=True, null=True)

    def __str__(self):
        return self.full_name


class AboutInfo(models.Model):
    username = models.CharField(max_length=100, default='')
    s_one = models.CharField(max_length=100, default='')
    s_two = models.CharField(max_length=100, default='')
    projects = models.CharField(max_length=100, default='')
    education = models.CharField(max_length=100, default='')
    skill_pack = models.CharField(max_length=100, default='')
    image = models.URLField(max_length=700, blank=True, null=True)


class ProjectsInfo(models.Model):
    username = models.CharField(max_length=100, default='')
    p_name = models.CharField(max_length=100, default='')
    p_skills = models.CharField(max_length=100, default='')
    p_url = models.CharField(max_length=300, default='')
    image = models.URLField(max_length=700, blank=True, null=True)


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
