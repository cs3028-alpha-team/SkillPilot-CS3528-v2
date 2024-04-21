from django.db import models
from django.utils.translation import gettext_lazy as _ # library used to create enums
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import pandas as pd
from django.core.validators import MinValueValidator
import numpy as np

# students table
class Student(models.Model):

    # string representation of student class
    def __str__(self):
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
    GPA = models.IntegerField(validators=[MinValueValidator(0)])
    desiredContractLength = models.CharField(max_length=25, choices=contractLength.choices)
    willingRelocate = models.BooleanField()
    aspirations = models.CharField(max_length = 200)
 
# internship table  
class Internship(models.Model):

    # string representation for the Internship class
    def __str__(self):
        return f"{self.internshipID}, {self.companyID.companyID}, {self.recruiterID.recruiterID}, {self.numberPositions}, {self.field}, {self.minGPA}"

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
    numberPositions = models.SmallIntegerField(validators=[MinValueValidator(0)]) 
    field = models.CharField(max_length = 20)
    title = models.CharField(max_length = 50)
    minGPA = models.SmallIntegerField(validators=[MinValueValidator(0)])

# companies table
class Company(models.Model):

    # string representation of Company model
    def __str__(self):
        return f"{self.companyID}, {self.companyName}, {self.industrySector}"

    #attributes for company table
    companyID = models.CharField(max_length = 10, primary_key = True)
    companyName = models.CharField(max_length = 50)
    industrySector = models.CharField(max_length = 30)
    websiteURL = models.CharField(max_length = 300)


# recruiter table
class Recruiter(models.Model):

    # string representation of Recruiter model
    def __str__(self):
        return f"{self.recruiterID}, {self.fullName}, {self.companyID.companyID}"

    # attributes for recruiter table
    recruiterID = models.CharField(max_length = 10, primary_key = True)
    fullName = models.CharField(max_length=50)
    email = models.EmailField()
    companyID = models.ForeignKey('core.Company', on_delete = models.CASCADE)
    jobTitle = models.CharField(max_length = 40)
    

# interviews table
class Interview(models.Model):

    # string representation of Interview model
    def __str__(self):
        return f"{self.interviewID}, {self.companyID.companyID}, {self.studentID.studentID}, {self.recruiterID.recruiterID}, {self.outcome}"

    #enum for interview outcomes
    class outcomes(models.TextChoices):

        ACCEPTED = 'accepted', _('Accepted')
        REJECTED = 'rejected', _('Rejected')
        PENDING = 'pending', _('Pending') 

    # interviews attributes 
    interviewID = models.CharField(max_length = 20, primary_key = True)
    companyID = models.ForeignKey('core.Company', on_delete = models.CASCADE)
    studentID = models.ForeignKey('core.Student', on_delete = models.CASCADE)
    recruiterID = models.ForeignKey('core.Recruiter', on_delete = models.CASCADE)
    internshipID = models.ForeignKey('core.Internship', on_delete = models.CASCADE, default=None)
    outcome = models.CharField(max_length = 15, choices = outcomes.choices)


# computedMatch Table
class ComputedMatch(models.Model):

    # string representation of Computed Match model
    def __str__(self):
        return f"{self.computedMatchID}, {self.internshipID.internshipID}, {self.studentID.studentID}, {self.interviewID.interviewID}"

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


"""
class definition for the KNN classifier used during the matchmaking process
"""
class Classifier:

    def __init__(self, dataframe, target_column, centroid_limit=50):
        self.df = dataframe
        self.target_column = target_column
        self.scaler = StandardScaler()
        self.centroid_limit = centroid_limit # limit of centroids to be used during elbow method

        self.__train()

    def __train(self):

        # fit the scaler object to the dataframe
        self.scaler.fit(self.df.drop(self.target_column, axis=1))

        # transform the dataframe using the trained scaler 
        self.scaled_features = self.scaler.transform(self.df.drop(self.target_column, axis=1))

        # create a new dataframe using the scaled features from the original one, minus the target column
        self.scaled_df = pd.DataFrame(data=self.scaled_features, columns=self.df.columns[:-1])

        # split the datasets into 70% training data and 30% testing data
        self.X, self.y = self.scaled_df, self.df[self.target_column]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.3, random_state=42)

        # perform a search using the Elbow method to find the number of centroids which yields the minimum error rate during classification
        error_rate = []

        for i in range(1, self.centroid_limit):
            knn = KNeighborsClassifier(n_neighbors=i)
            knn.fit(self.X_train, self.y_train)
            predictions_i = knn.predict(self.X_test)
            # average error rate, where predicitons where not equal to actual test values 
            error_rate.append(np.mean(predictions_i != self.y_test))

        # instantiate the KNNClassifier with k = min_error_k, i.e. the number of centroids which yields the least error
        min_error_k = error_rate.index(min(error_rate))
        self.knn = KNeighborsClassifier(min_error_k)
        self.knn.fit(self.X_train, self.y_train)


    def assess(self):

        # display the confusion matrix and classfication report for this model
        self.predictions = self.knn.predict(self.X_test)
        print(confusion_matrix(self.y_test, self.predictions))
        print('\n')
        print(classification_report(self.y_test, self.predictions))
        
    # given an input dataframe, without the target column, return a list of predictions 
    def predict(self, offers):
        return [ self.knn.predict(offers.iloc[i].to_frame().T)[0] for i in offers.index ]