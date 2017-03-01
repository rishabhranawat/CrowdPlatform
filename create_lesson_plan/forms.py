from django import forms

class UploadLessonPlanForm(forms.Form):
	GRADE_CHOICES = (
        ('Undergraduate', 'Undergraduate'),
        ('Graduate', 'Graduate'),
    )
	subject_name = forms.CharField(label='Subject Name')
	course_name = forms.CharField(label='Course Name')
	input_title = forms.CharField(label='Lesson Title')
	input_grade = forms.ChoiceField(label='Grade', choices=GRADE_CHOICES)
	input_bullets = forms.CharField(label='Bullets', widget=forms.Textarea)