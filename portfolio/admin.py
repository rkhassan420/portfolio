from django.contrib import admin
from .models import HomeInfo, FooterInfo, ProjectsInfo
from .models import AboutInfo


class HomeInfoAdmin(admin.ModelAdmin):
    list_display = ('logo_title',  'full_name', 'skill_title', 'experience', 'image', 'cv')


class AboutInfoAdmin(admin.ModelAdmin):
    list_display = ('s_one', 's_two', 'projects', 'education', 'skill_pack', 'image',)


class FooterInfoAdmin(admin.ModelAdmin):
    list_display = ('full_name',  'email', 'c_title', 'linkedin', 'github', 'whatsapp')

class ProjectsInfoAdmin(admin.ModelAdmin):
    list_display = ('p_name',  'p_skills', 'p_url', 'image')




admin.site.register(HomeInfo, HomeInfoAdmin)
admin.site.register(AboutInfo, AboutInfoAdmin)
admin.site.register(FooterInfo, FooterInfoAdmin)
admin.site.register(ProjectsInfo, ProjectsInfoAdmin)


