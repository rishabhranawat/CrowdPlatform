from django.conf.urls import url
from create_lesson_plan import views
from create_lesson_plan import questions

urlpatterns = [
    url(r'^generate_lesson_plan/(?P<todo>[-\w]+)', views.GenerateLessonPlan.as_view(), name="generate_lesson_plan"),
    url(r'^profile/', views.user_profile.as_view(), name="profile"),
    url(r'^remove_from_lp/',views.remove_from_lp, name="remove_from_lp"),
    url(r'^(?P<pk>\d+)/add_questions/', questions.AddQuestions.as_view(), name="add_questions"),
    url(r'^save_lesson_plan/',views.save_lesson_plan,name="save_lesson_plan"),

    url(r'^upload_lesson_plan/', views.upload_lesson_plan.as_view(), name="upload_lesson_plan"),
    url(r'^(?P<pk>\d+)/user_lesson_plan/(?P<todo>[-\w]+)', views.UserLessonPlan.as_view(), name='user_lesson_plan'),
    url(r'^(?P<pk>\d+)/display_search_lesson_plan/', views.DisplaySearchLessonPlan.as_view(), 
    	name='display_search_lesson_plan'),
    url(r'^(?P<pk>\d+)/answer_questions/', questions.AnswerQuestions.as_view(), name="answer_questions"),

]

