from django import forms
from . models import *
from django.forms import ModelForm

# create form for the Student model
class StudentForm(ModelForm):
    class Meta:
        model = Student 
        fields = '__all__'

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