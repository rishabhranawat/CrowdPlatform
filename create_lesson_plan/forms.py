from django import forms

class UploadLessonPlanForm(forms.Form):
	subject_name = forms.CharField(label='subject_name')
	course_name = forms.CharField(label='course_name')
	input_title = forms.CharField(label='lesson_title')
	input_grade = forms.CharField(label='grade')
	input_bullets = forms.CharField(label='bullets', widget=forms.Textarea)
	docfile = forms.FileField(label='Select a file', help_text='max. 42 megabytes')