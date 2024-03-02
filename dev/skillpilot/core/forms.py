from django import forms
from . models import *
from django.forms import ModelForm

# create form for the Student model
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

        # use Widgets to apply bootstrap styles to dynamically loaded form
        widgets = {
            'fullName': forms.TextInput(attrs={'class': 'form-control', 'id': 'fullnameInput', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'emailInput', 'required': True}),
            'currProgramme': forms.TextInput(attrs={'class': 'form-control', 'id': 'currProgrammeInput', 'required': True}),
            'prevProgramme': forms.TextInput(attrs={'class': 'form-control', 'id': 'prevProgrammeInput', 'required': True}),
            'studyMode': forms.Select(attrs={'class': 'form-select', 'id': 'studymodeInput'}),
            'studyPattern': forms.Select(attrs={'class': 'form-select', 'id': 'studypatternInput'}),
            'GPA': forms.NumberInput(attrs={'class': 'form-control', 'id': 'studentGPAInput', 'min': 40, 'max': 100, 'required': True}),
            'desiredContractLength': forms.Select(attrs={'class': 'form-select', 'id': 'contractLengthInput'}),
            'willingRelocate': forms.Select(attrs={'class': 'form-select', 'id': 'willingRelocation', 'required': True}, choices=[(True, 'Yes'), (False, 'No')]),
            'aspirations': forms.Textarea(attrs={'class': 'form-control', 'id': 'aspirations', 'rows': 2}),
        }

# create form for the Internship model
class InternshipForm(ModelForm):
    class Meta:
        model = Internship
        fields = '__all__'

        # use Widgets to apply bootstrap styles to dynamically loaded form
        widgets = {
            'internshipID': forms.TextInput(attrs={'class': 'form-control', 'id': 'internshipIDInput', 'required': True}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'id': 'titleInput', 'required': True}),
            'field': forms.TextInput(attrs={'class': 'form-control', 'id': 'fieldInput', 'required': True}),
            'contractMode': forms.Select(attrs={'class': 'form-select', 'id': 'contractmodeInput'}),
            'contractPattern': forms.Select(attrs={'class': 'form-select', 'id': 'contractpatternInput'}),
            'minGPA': forms.NumberInput(attrs={'class': 'form-control', 'id': 'minGPAInput', 'min': 40, 'max': 100, 'required': True}),
            'numberPositions': forms.NumberInput(attrs={'class': 'form-control', 'id': 'numberPositionsInput', 'min': 1, 'max': 10, 'required': True}),
        }