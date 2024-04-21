from django.test import TestCase
from core.models import Student, Internship, Company, Recruiter, Interview, ComputedMatch
from django.core.exceptions import ValidationError
import pickle
import pandas as pd
import numpy as np

class TestModels(TestCase):
    def setUp(self):
        # Create test data
        self.company = Company.objects.create(companyID='C001', companyName='Test Company', industrySector='IT')
        self.recruiter = Recruiter.objects.create(recruiterID='R001', fullName='Test Recruiter', email='test@example.com', companyID=self.company, jobTitle='HR Manager')
        self.student = Student.objects.create(studentID=1, fullName='Test Student', email='teststudent@example.com', currProgramme='Test Program', prevProgramme='Previous Program', studyMode='online', studyPattern='FT', GPA=4, desiredContractLength='6-W', willingRelocate=True, aspirations='To excel in the field')
        self.internship = Internship.objects.create(internshipID='I001', companyID=self.company, recruiterID=self.recruiter, contractMode='online', contractPattern='FT', numberPositions=5, field='IT', title='Test Internship', minGPA=3)
        self.interview = Interview.objects.create(interviewID='IV001', companyID=self.company, studentID=self.student, recruiterID=self.recruiter, internshipID=Internship.objects.get(internshipID='I001'), outcome='accepted')

    def test_str_methods(self):
        self.assertEqual(str(self.company), "C001, Test Company, IT")
        self.assertEqual(str(self.recruiter), "R001, Test Recruiter, C001")
        self.assertEqual(str(self.student), "1, Test Student, Test Program, Previous Program, 4")
        self.assertEqual(str(self.internship), "I001, C001, R001, 5, IT, 3")
        self.assertEqual(str(self.interview), "IV001, C001, 1, R001, accepted")

    def test_relationship_integrity(self):
        self.assertEqual(self.internship.companyID, self.company)
        self.assertEqual(self.internship.recruiterID, self.recruiter)
        self.assertEqual(self.interview.studentID, self.student)
        self.assertEqual(self.interview.companyID, self.company)
        self.assertEqual(self.interview.recruiterID, self.recruiter)

    def test_delete_cascades(self):
        self.company.delete()
        self.assertIsNone(Recruiter.objects.filter(recruiterID='R001').first())

# test model str methods
class TestStrMethods(TestCase):
    def test_student_str_method(self):
        student = Student.objects.create(fullName='Test Student', email='teststudent@example.com', currProgramme='Test Program', prevProgramme='Previous Program', studyMode='online', studyPattern='FT', GPA=4, desiredContractLength='6-W', willingRelocate=True, aspirations='To excel in the field')
        self.assertEqual(str(student), "1, Test Student, Test Program, Previous Program, 4")

    def test_internship_str_method(self):
        internship = Internship.objects.create(internshipID='I001', companyID=Company.objects.create(companyID='C001', companyName='Test Company', industrySector='IT'), recruiterID=Recruiter.objects.create(recruiterID='R001', fullName='Test Recruiter', email='test@example.com', companyID=Company.objects.get(companyID='C001'), jobTitle='HR Manager'), contractMode='online', contractPattern='FT', numberPositions=5, field='IT', title='Test Internship', minGPA=3)
        self.assertEqual(str(internship), "I001, C001, R001, 5, IT, 3")

    def test_company_str_method(self):
        company = Company.objects.create(companyID='C001', companyName='Test Company', industrySector='IT')
        self.assertEqual(str(company), "C001, Test Company, IT")

    def test_recruiter_str_method(self):
        recruiter = Recruiter.objects.create(recruiterID='R001', fullName='Test Recruiter', email='test@example.com', companyID=Company.objects.create(companyID='C001', companyName='Test Company', industrySector='IT'), jobTitle='HR Manager')
        self.assertEqual(str(recruiter), "R001, Test Recruiter, C001")

    def test_interview_str_method(self):
        # Create required objects
        company = Company.objects.create(companyID='C001', companyName='Test Company', industrySector='IT')
        recruiter = Recruiter.objects.create(recruiterID='R001', fullName='Test Recruiter', email='test@example.com', companyID=company, jobTitle='HR Manager')
        student = Student.objects.create(studentID=1, fullName='Test Student', email='teststudent@example.com', currProgramme='Test Program', prevProgramme='Previous Program', studyMode='online', studyPattern='FT', GPA=4, desiredContractLength='6-W', willingRelocate=True, aspirations='To excel in the field')
        internship = Internship.objects.create(internshipID='I001', companyID=company, recruiterID=recruiter, contractMode='online', contractPattern='FT', numberPositions=5, field='IT', title='Test Internship', minGPA=3)
        
        interview = Interview.objects.create(interviewID='IV001', companyID=company, studentID=student, recruiterID=recruiter, internshipID=internship, outcome='accepted')

        self.assertEqual(str(interview), "IV001, C001, 1, R001, accepted")
        

    def test_computedmatch_str_method(self):
        # create required objects
        company = Company.objects.create(companyID='C001', companyName='Test Company', industrySector='IT')
        recruiter = Recruiter.objects.create(recruiterID='R001', fullName='Test Recruiter', email='test@example.com', companyID=company, jobTitle='HR Manager')
        student = Student.objects.create(studentID=1, fullName='Test Student', email='teststudent@example.com', currProgramme='Test Program', prevProgramme='Previous Program', studyMode='online', studyPattern='FT', GPA=4, desiredContractLength='6-W', willingRelocate=True, aspirations='To excel in the field')
        internship = Internship.objects.create(internshipID='I001', companyID=company, recruiterID=recruiter, contractMode='online', contractPattern='FT', numberPositions=5, field='IT', title='Test Internship', minGPA=3)
        interview = Interview.objects.create(interviewID='IV001', companyID=company, studentID=student, recruiterID=recruiter, internshipID=internship, outcome='accepted')
        computed_match = ComputedMatch.objects.create(computedMatchID='CM001', internshipID=internship, studentID=student, interviewID=interview)
        
        self.assertEqual(str(computed_match), "CM001, I001, 1, IV001")

class TestFieldValidation(TestCase):
    def test_student_field_validation(self):
        # Test invalid email
        with self.assertRaises(ValidationError):
            student = Student(fullName='Test Student', email='invalid_email', currProgramme='Test Program', prevProgramme='Previous Program', studyMode='online', studyPattern='FT', GPA=4, desiredContractLength='6-W', willingRelocate=True, aspirations='To excel in the field')
            student.full_clean()

        # Test invalid GPA
        with self.assertRaises(ValidationError):
            student = Student(fullName='Test Student', email='teststudent@example.com', currProgramme='Test Program', prevProgramme='Previous Program', studyMode='online', studyPattern='FT', GPA=-1, desiredContractLength='6-W', willingRelocate=True, aspirations='To excel in the field')
            student.full_clean()

        # Test invalid study mode
        with self.assertRaises(ValidationError):
            student = Student(fullName='Test Student', email='teststudent@example.com', currProgramme='Test Program', prevProgramme='Previous Program', studyMode='invalid', studyPattern='FT', GPA=4, desiredContractLength='6-W', willingRelocate=True, aspirations='To excel in the field')
            student.full_clean()

        # Test valid student
        valid_student = Student(fullName='Valid Student', email='validstudent@example.com', currProgramme='Test Program', prevProgramme='Previous Program', studyMode='online', studyPattern='FT', GPA=4, desiredContractLength='6-W', willingRelocate=True, aspirations='To excel in the field')
        valid_student.full_clean()  
        
    def test_internship_field_validation(self):
        # Test invalid contract mode
        with self.assertRaises(ValidationError):
            internship = Internship.objects.create(internshipID='I007', companyID=Company.objects.create(companyID='C004', companyName='Test Company', industrySector='IT'), recruiterID=Recruiter.objects.create(recruiterID='R009', fullName='Test Recruiter', email='test@example.com', companyID=Company.objects.get(companyID='C004'), jobTitle='HR Manager'), contractMode='invalid', contractPattern='FT', numberPositions=5, field='IT', title='Test Internship', minGPA=3)
            internship.full_clean()

        # Test invalid number of positions
        with self.assertRaises(ValidationError):
            internship = Internship.objects.create(internshipID='I001', companyID=Company.objects.create(companyID='C001', companyName='Test Company', industrySector='IT'), recruiterID=Recruiter.objects.create(recruiterID='R001', fullName='Test Recruiter', email='test@example.com', companyID=Company.objects.get(companyID='C001'), jobTitle='HR Manager'), contractMode='online', contractPattern='FT', numberPositions=-5, field='IT', title='Test Internship', minGPA=3)
            internship.full_clean()
            
        # Test valid internship
        valid_internship = Internship.objects.create(internshipID='I002', companyID=Company.objects.create(companyID='C002', companyName='Test Company 2', industrySector='IT'), recruiterID=Recruiter.objects.create(recruiterID='R002', fullName='Test Recruiter 2', email='test2@example.com', companyID=Company.objects.get(companyID='C002'), jobTitle='HR Manager'), contractMode='online', contractPattern='FT', numberPositions=5, field='IT', title='Test Internship 2', minGPA=3)
        valid_internship.full_clean()
        
    def test_interview_field_validation(self):
        # Create objects for testing
        company_c002, _ = Company.objects.get_or_create(companyID='C002', defaults={'companyName':'Test Company', 'industrySector':'IT'})
        company_c001, _ = Company.objects.get_or_create(companyID='C001', defaults={'companyName':'Test Company 2', 'industrySector':'IT'})
        recruiter_r002, _ = Recruiter.objects.get_or_create(recruiterID='R002', defaults={'fullName':'Test Recruiter 2', 'email':'test2@example.com', 'companyID':company_c002, 'jobTitle':'HR Manager'})
        recruiter_r001, _ = Recruiter.objects.get_or_create(recruiterID='R001', defaults={'fullName':'Test Recruiter', 'email':'test@example.com', 'companyID':company_c002, 'jobTitle':'HR Manager'})
        internship_i009 = Internship.objects.create(internshipID='I009', companyID=company_c002, recruiterID=recruiter_r002, contractMode='online', contractPattern='FT', numberPositions=5, field='IT', title='Test Internship 2', minGPA=3)
        student = Student.objects.create(studentID=1, fullName='Test Student', email='teststudent@example.com', currProgramme='Test Program', prevProgramme='Previous Program', studyMode='online', studyPattern='FT', GPA=4, desiredContractLength='6-W', willingRelocate=True, aspirations='To excel in the field')

        # Test invalid outcome
        with self.assertRaises(ValidationError):
            interview = Interview.objects.create(interviewID='IV001', companyID=company_c002, internshipID=internship_i009, studentID=student, recruiterID=recruiter_r001, outcome='invalid')
            interview.full_clean()

        # Test valid interview
        internship_i007 = Internship.objects.create(internshipID='I007', companyID=company_c001, recruiterID=recruiter_r001, contractMode='online', contractPattern='FT', numberPositions=5, field='IT', title='Test Internship 2', minGPA=3)
        valid_interview = Interview.objects.create(interviewID='IV002', companyID=company_c001, studentID=student, recruiterID=recruiter_r001, internshipID=internship_i007, outcome='accepted')
        valid_interview.full_clean()
        
    def test_company_field_validation(self):
        # Test invalid company ID length
        with self.assertRaises(ValidationError):
            company = Company.objects.create(companyID='InvalidIDddsfdssagragrt54e674', companyName='Test Company', industrySector='IT')
            company.full_clean()
            
        # Test valid company
        valid_company = Company.objects.create(companyID='C002', companyName='Test Company 2', industrySector='IT', websiteURL='www.bob.com')
        valid_company.full_clean()
        
    def test_recruiter_field_validation(self):
        # Test invalid recruiter ID length
        with self.assertRaises(ValidationError):
            recruiter = Recruiter.objects.create(recruiterID='InvalidIDdddddddddddd', fullName='Test Recruiter', email='test@example.com', companyID=Company.objects.create(companyID='C001', companyName='Test Company', industrySector='IT'), jobTitle='HR Manager')
            recruiter.full_clean()
        # Test valid recruiter
        valid_recruiter = Recruiter.objects.create(recruiterID='R002', fullName='Test Recruiter 2', email='test2@example.com', companyID=Company.objects.create(companyID='C002', companyName='Test Company 2', industrySector='IT'), jobTitle='HR Manager')
        valid_recruiter.full_clean()
        
    def test_computedmatch_field_validation(self):
        company = Company.objects.create(companyID='C001', companyName='Test Company', industrySector='IT')
        recruiter = Recruiter.objects.create(recruiterID='R001', fullName='Test Recruiter', email='test@example.com', companyID=company, jobTitle='HR Manager')
        student = Student.objects.create(studentID=1, fullName='Test Student', email='teststudent@example.com', currProgramme='Test Program', prevProgramme='Previous Program', studyMode='online', studyPattern='FT', GPA=4, desiredContractLength='6-W', willingRelocate=True, aspirations='To excel in the field')
        internship = Internship.objects.create(internshipID='I001', companyID=company, recruiterID=recruiter, contractMode='online', contractPattern='FT', numberPositions=5, field='IT', title='Test Internship', minGPA=3)
        interview = Interview.objects.create(interviewID='IV001', companyID=company, studentID=student, recruiterID=recruiter, internshipID=internship, outcome='accepted')

        # Test invalid computed match ID length
        with self.assertRaises(ValidationError):
            computed_match = ComputedMatch.objects.create(computedMatchID='InvalidIDfgsrsytrystryreyr', internshipID=internship, studentID=student, interviewID=interview)
            computed_match.full_clean()

        # Test valid computed match
        valid_computed_match = ComputedMatch.objects.create(computedMatchID='CM002', internshipID=internship, studentID=student, interviewID=interview)
        valid_computed_match.full_clean()   

class TestClassifier(TestCase):
    
    def setUp(self):   
        with open(r'C:\Users\hp\Computing\bbb\SkillPilot-CS3528-v2-2\dev\skillpilot\classifier.pkl', 'rb') as file:
            self.classifier = pickle.load(file)
        
        # Generate dummy data
        data = {
            'Feature1': np.random.randn(100),
            'Feature2': np.random.randn(100),
            'Target': np.random.randint(0, 2, size=100)
        }
        self.df = pd.DataFrame(data)
        #self.classifier = Classifier(self.df, 'Target')

    def test_train_sets_up_scaler_and_classifier(self):
        self.assertIsNotNone(self.classifier.scaler)
        self.assertIsNotNone(self.classifier.knn)
    """
    def test_accuracy_and_error_handling_of_predict_method(self):
        test_data = pd.DataFrame({
            'Feature1': np.random.randn(10),
            'Feature2': np.random.randn(10)
        })
        predictions = self.classifier.predict(test_data)
        self.assertEqual(len(predictions), 10)
    """
    def test_assess_produces_correct_output(self):
        self.classifier.assess()
        # Add assertions for the expected output of classification report and confusion matrix
        # not 100% sure what they should be 