from django.db import models


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
    projects = models.CharField(max_length=100, default='')
    education = models.CharField(max_length=100, default='')
    skill_pack = models.CharField(max_length=100, default='')
    image = models.URLField(max_length=700, blank=True, null=True)



class LatestInfo(models.Model):
    username = models.CharField(max_length=100, default='')
    s_one = models.CharField(max_length=100, default='')
    s_two = models.CharField(max_length=100, default='')
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



class ProjectsInfo(models.Model):
    p_name = models.CharField(max_length=100, default='')
    p_skills = models.CharField(max_length=100, default='')
    p_url = models.CharField(max_length=300, default='')
    image = models.ImageField(upload_to='uploads/images/', blank=True, null=True, default=None)
