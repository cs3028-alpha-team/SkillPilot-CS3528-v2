from django.db import models
from django.utils.translation import gettext_lazy as _ # library used to create enums

# students table
class Student(models.Model):

    # string representation of student class
    def str(self):
        return f"{self.studentID}, {self.fullName}, {self.currProgramme}, {self.prevProgramme}, {self.GPA}"

    # enum for the study-pattern
    class pattern(models.TextChoices):
        FULL_TIME = 'FT', _('Full-Time')
        PART_TIME = 'PT', _('Part-Time')

    # enum for the study-mode 
    class mode(models.TextChoices): 
        ONLINE = 'online', _('Online')
        IN_PERSON = 'in-person', _('In-Person')
        HYBRID = 'hybrid', _('Hybrid')

    # enum for contract length
    class contractLength(models.TextChoices):
        SIX_WEEKS = '6-W', _("6-weeks")
        TWELVE_WEEKS = '12-W', _("12-weeks")
        SIX_MONTHS = '6-M', _("6-months")
        NINE_MONTHS = '9-M', _("9-months")
        ONE_YEAR = '1-Y', _("1-year")

    studentID = models.BigAutoField(primary_key=True)
    fullName = models.CharField(max_length=50)
    email = models.EmailField()
    currProgramme = models.CharField(max_length=50) # program they are currently studying
    prevProgramme = models.CharField(max_length=50) # program they previously studies and now graduated from
    studyMode= models.CharField(max_length=10, choices= mode.choices)
    studyPattern = models.CharField(max_length = 2, choices= pattern.choices)
    GPA = models.IntegerField()
    desiredContractLength = models.CharField(max_length=25, choices=contractLength.choices)
    willingRelocate = models.BooleanField()
    aspirations = models.CharField(max_length = 200)
 
# internship table  
class Internship(models.Model):

    # string representation for the Internship class
    def str(self):
        return f"{self.internshipID}, {self.companyID}, {self.recruiterID}, {self.numberPositions}, {self.field}, {self.minGPA}"

    # enum for pattern
    class pattern(models.TextChoices):
        FULL_TIME = 'FT', _('Full-Time')
        PART_TIME = 'PT', _('Part-Time')

    # enum for mode
    class mode(models.TextChoices):  
        ONLINE = 'online', _('Online')
        IN_PERSON = 'in-person', _('In-Person')
        HYBRID = 'hybrid', _('Hybrid')

    # attributes for internship table
    internshipID = models.CharField(max_length = 10, primary_key= True)
    companyID = models.ForeignKey('core.Company', on_delete = models.CASCADE)
    recruiterID = models.ForeignKey('core.Recruiter', on_delete = models.CASCADE)
    contractMode = models.CharField(max_length=10, choices= mode.choices)
    contractPattern = models.CharField(max_length = 2, choices= pattern.choices)
    # number of internships availables in the company for that internship type
    numberPositions = models.SmallIntegerField() 
    field = models.CharField(max_length = 20)
    title = models.CharField(max_length = 50)
    minGPA = models.SmallIntegerField()

# companies table
class Company(models.Model):

    # string representation of Company model
    def str(self):
        return f"{self.companyID}, {self.companyName}, {self.industrySector}"

    #attributes for company table
    companyID = models.CharField(max_length = 10, primary_key = True)
    companyName = models.CharField(max_length = 50)
    industrySector = models.CharField(max_length = 30)
    websiteURL = models.CharField(max_length = 300)


# recruiter table
class Recruiter(models.Model):

    # string representation of Recruiter model
    def str(self):
        return f"{self.recruiterID}, {self.fullName}, {self.companyID}"

    # attributes for recruiter table
    recruiterID = models.CharField(max_length = 10, primary_key = True)
    fullName = models.CharField(max_length=50)
    email = models.EmailField()
    companyID = models.ForeignKey('core.Company', on_delete = models.CASCADE)
    jobTitle = models.CharField(max_length = 40)
    
# interviews table
class Interview(models.Model):

    # string representation of Interview model
    def str(self):
        return f"{self.interviewID}, {self.companyID}, {self.studentID}, {self.recruiterID}, {self.outcome}"

    #enum for interview outcomes
    class outcomes(models.TextChoices):

        ACCEPTED = 'accepted', _('Accepted')
        REJECTED = 'rejected', _('Rejected')
        PENDING = 'pending', _('Pending') 

    # interviews attributes 
    interviewID = models.CharField(max_length = 10, primary_key = True)
    companyID = models.ForeignKey('core.Company', on_delete = models.CASCADE)
    studentID = models.ForeignKey('core.Student', on_delete = models.CASCADE)
    recruiterID = models.ForeignKey('core.Recruiter', on_delete = models.CASCADE)
    outcome = models.CharField(max_length = 15, choices = outcomes.choices)


# computedMatch Table
class ComputedMatch(models.Model):

    # string representation of Computed Match model
    def str(self):
        return f"{self.computedMatch}, {self.internshipID}, {self.studentID}, {self.interviewID}"

    # table attributes
    computedMatchID = models.CharField(max_length = 20, primary_key = True)
    internshipID = models.ForeignKey('core.Internship', on_delete = models.CASCADE)
    studentID = models.ForeignKey('core.Student', on_delete = models.CASCADE)
    interviewID = models.ForeignKey('core.Interview', on_delete = models.CASCADE, null=True)


# superUser table 
class SuperUser(models.Model):

    # enum for privilege
    class privileges(models.TextChoices):

        READ = 'r', _('Read')
        WRITE = 'w', _('Write')
        MAINTAIN = 'm', _('Maintain')
        ADMIN = 'a', _('Admin')

    # attributes
    superUserID = models.CharField(max_length = 10, primary_key = True)
    fullName = models.CharField(max_length=50)
    privileges = models.CharField(max_length = 1, choices = privileges.choices)