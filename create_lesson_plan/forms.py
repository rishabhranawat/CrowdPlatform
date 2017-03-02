from django import forms
from multiupload.fields import MultiFileField, MultiMediaField


class GenerateLessonPlanForm(forms.Form):
	GRADE_CHOICES = (
        ('Undergraduate', 'Undergraduate'),
        ('Graduate', 'Graduate'),
    )
	subject_name = forms.CharField(label='Subject Name')
	course_name = forms.CharField(label='Course Name')
	input_title = forms.CharField(label='Lesson Title')
	input_grade = forms.ChoiceField(label='Grade', choices=GRADE_CHOICES)
	lesson_outline = forms.CharField(label='Lesson Outline', widget=forms.Textarea)


# Form for Uploading a Lesson Plan [Can inherit from GenerateLessonPlan 
# but need to resolve file issue]
class UploadLessonPlanForm(forms.Form):
	GRADE_CHOICES = (
        ('Undergraduate', 'Undergraduate'),
        ('Graduate', 'Graduate'),
    )
	subject_name = forms.CharField(label='Subject Name')
	course_name = forms.CharField(label='Course Name')
	input_title = forms.CharField(label='Lesson Title')
	input_grade = forms.ChoiceField(label='Grade', choices=GRADE_CHOICES)
	lesson_outline = forms.CharField(label='Lesson Outline', widget=forms.Textarea)

# Form for Searching a Lesson Plan
class SearchResultsForm(forms.Form):
	GRADE_CHOICES = (
        ('Undergraduate', 'Undergraduate'),
        ('Graduate', 'Graduate'),
    )
	subject_name = forms.CharField(label='Subject Name')
	course_name = forms.CharField(label='Course Name', required=False)
	input_title = forms.CharField(label='Lesson Title', required=False)
	input_grade = forms.ChoiceField(label='Grade', choices=GRADE_CHOICES, required=False)