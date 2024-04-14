from django.contrib import admin

from core.models import *

# register all models defined in core/models.py
admin.site.register(Student)
admin.site.register(Internship)
admin.site.register(Company)
admin.site.register(Recruiter)
admin.site.register(Interview)
admin.site.register(ComputedMatch)
admin.site.register(SuperUser)
