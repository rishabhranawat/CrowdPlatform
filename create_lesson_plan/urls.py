from django.conf.urls import url

from create_lesson_plan import views

urlpatterns = [
    url(r'^generate_lesson_plan/', views.GenerateLessonPlan.as_view(), name="generate_lesson_plan"),
    url(r'^profile/', views.user_profile.as_view(), name="profile"),
    url(r"^remove_from_lp/",views.remove_from_lp, name="remove_from_lp"),

    url(r"^save_lesson_plan/",views.save_lesson_plan,name="save_lesson_plan"),
    url(r'^upload_lesson_plan/', views.upload_lesson_plan.as_view(), name="upload_lesson_plan"),
    url(r'^(?P<pk>\d+)/lesson_plan/', views.user_lesson_plan.as_view(), name='lesson_plan'),
]
