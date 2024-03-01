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
            'willingRelocate': forms.Select(attrs={'class': 'form-select', 'id': 'willingRelocation'}, choices=[(True, 'Yes'), (False, 'No')]),
            'aspirations': forms.Textarea(attrs={'class': 'form-control', 'id': 'aspirations', 'rows': 2}),
        }

# create form for the Internship model
class InternshipForm(ModelForm):
    class Meta:
        model = Internship
        exclude = [ 'internshipID', 'companyID', 'recruiterID', ]

    # internshipID = models.CharField(max_length = 10, primary_key= True)
    # companyID = models.ForeignKey('core.Company', on_delete = models.CASCADE)
    # recruiterID = models.ForeignKey('core.Recruiter', on_delete = models.CASCADE)
    # contractMode = models.CharField(max_length=10, choices= mode.choices)
    # contractPattern = models.CharField(max_length = 2, choices= pattern.choices)
    # # number of internships availables in the company for that internship type
    # numberPositions = models.SmallIntegerField() 
    # field = models.CharField(max_length = 20)
    # title = models.CharField(max_length = 30)
    # minGPA = models.SmallIntegerField()