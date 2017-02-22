"""CrowdPlatform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from create_lesson_plan import views as v

from django.contrib import admin


urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),
    url(r"^create_lesson_plan/",include("create_lesson_plan.urls",namespace="clp")),
    #url(r"^submit_question/",v.submit_question, name="submit_question"),
    #url(r"^submittted_question/",v.submitted_question, name="submitted_question"),
    url(r"^search_lesson_plan/",v.search_lp, name="search_lesson_plan"),
    #url(r"^search_questions/",v.search_que, name="search_questions"),
    #url(r"^generate_question_paper/",v.generate_q_paper, name="generate_question_paper"),
    #url(r"^question_paper/",v.generate_qp_results, name="question_paper"),
    #url(r"^search_results/",v.search_results, name="search_results"),
    url(r"^search_results_terse/",v.search_results_terse, name="search_results_terse"),
    #url(r"^search_q_results/",v.search_q_results, name="search_q_results"),
    url(r"^lesson_plan/(?P<lesson_plan_id>.+)/$", v.display_lesson_plan, name="show_lesson_plan"),
    #url(r"^create_lesson_plan/",v.create_lesson_plan, name='create_lesson_plan'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
