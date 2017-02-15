from django.contrib import admin
from create_lesson_plan.models import lesson, lesson_plan, Evaluate_Urls, Engage_Urls, Explain_Urls, MCQ, Engage_Images, Explain_Images, Evaluate_Images, FITB, Document, Image

# Register your models here.
admin.site.register(lesson)
admin.site.register(lesson_plan)
admin.site.register(Engage_Urls)
admin.site.register(Explain_Urls)
admin.site.register(Evaluate_Urls)
admin.site.register(MCQ)
admin.site.register(FITB)
admin.site.register(Engage_Images)
admin.site.register(Explain_Images)
admin.site.register(Evaluate_Images)
admin.site.register(Document)
admin.site.register(Image)