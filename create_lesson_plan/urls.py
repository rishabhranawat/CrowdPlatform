from django.conf.urls import url

from create_lesson_plan import views

urlpatterns = [
    url(r'^$', views.create_lesson_plan, name="create_lesson_plan"),
    url(r"^show_lesson_plan/",views.show_lesson_plan, name="show_lesson_plan"),
    url(r"^remove_from_lp/",views.remove_from_lp, name="remove_from_lp"),
    #url(r"^show_temp_lesson_plan/",views.show_temp_lesson_plan, name="show_temp_lesson_plan"),
    url(r"^save_lesson_plan/",views.save_lesson_plan,name="save_lesson_plan"),
    url(r'^upload_lesson_plan/', views.upload_lesson_plan.as_view(), name="uplaod_lesson_plan"),
]
