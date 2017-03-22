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

class ManualLinkAddition(forms.Form):
	LINK_CHOICES = (
		('Engage', 'Engage'),
		('Evaluate', 'Evaluate'),
	)
	link = forms.CharField(label='Paste URL', required=True)
	link_type = forms.ChoiceField(label='Select Phase', choices=LINK_CHOICES, required=True)
	link_title = forms.CharField(label='Title of the page')
	link_desc = forms.CharField(label='Short Description', widget=forms.Textarea)

