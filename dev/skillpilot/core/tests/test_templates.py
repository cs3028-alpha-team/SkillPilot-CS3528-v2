from django.test import TestCase, Client
from core.models import Student, Internship, Company, Recruiter
from django.contrib.auth.models import User

#below the code tests url for templates
#verifying by checking the page displays code from the corresponding html file 
#in some cases data had to be created to gain access to templates that require it
class TemplateRenderingTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_template_rendering_template(self):
   
        response = self.client.get('/contacts')

        self.assertEqual(response.status_code, 200)


        self.assertTemplateUsed(response, 'contacts.html')

        self.assertContains(response, '<h1 class="display-2 mt-5">Contacts</h1>')

    def test_template_rendering_template1(self):
    
        response = self.client.get('/home')

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'home.html')

        self.assertContains(response, '<h1 class="display-2 mt-5">Welcome to Skillpilot</h1>')
    
    def test_template_rendering_template2(self):
     
        response = self.client.get('/student-login')

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'auth/student_login.html')

      
        self.assertContains(response, '<h1 class="display-4 m-3"> Student Login Page </h1>')
    
    def test_template_rendering_template3(self):
     
        response = self.client.get('/student-signup')

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'auth/student_signup.html')

        self.assertContains(response, '<h1 class="display-4 m-3"> Student Registration Page </h1>')

    def test_template_rendering_template4(self):
   
        response = self.client.get('/recruiter-signup')


        self.assertEqual(response.status_code, 200)


        self.assertTemplateUsed(response, 'auth/recruiter_signup.html')

        self.assertContains(response, '<h1 class="display-4 m-3"> Recruiter Registration Page </h1>')
    
    def test_template_rendering_template5(self):
    
        response = self.client.get('/recruiter-login')

    
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'auth/recruiter_login.html')

        self.assertContains(response, '<h1 class="display-4 m-3"> Recruiter Login Page </h1>')

    def test_template_rendering_template6(self):
    
        student_user = User.objects.create_user(username='mattia2', email= 'mattia2@mattia2.com', password='12435687abdn')
        student_user.groups.create(name='Students')  

        self.client.login(username='mattia2', password='12435687abdn')
        
    
        response = self.client.get('/student')

        self.assertEqual(response.status_code, 200)


        self.assertTemplateUsed(response, 'student_dashboard.html')

      
        self.assertContains(response, '<h1> Student dashboard</h1>')

    def test_template_rendering_template7(self):

        recruiter_user = User.objects.create_user(username='tesco', email= 'tesco@fskdgskhdfsjf.com', password='12435687abdn')
        recruiter_user.groups.create(name='Companies')  

        company = Company.objects.create(
            companyID = 'tesco',
            companyName = 'tesco',
            industrySector = 'retail',
            websiteURL = 'www',
        )
        recruiter = Recruiter.objects.create(
            fullName='tesco',
            recruiterID='tesco4', 
            companyID=company,
            jobTitle='tesco LD',
            email='tesco@fskdgskhdfsjf.com',
 
        )
        self.client.login(username='tesco', password='12435687abdn')
        
      
        response = self.client.get('/recruiter')

     
        self.assertEqual(response.status_code, 200)


        self.assertTemplateUsed(response, 'recruiter_dashboard.html')

   
        self.assertContains(response, '<h3 class="display-6 mt-5 mb-4">Upload new opportunities</h3>')

    def test_template_rendering_template8(self):

        Admin_user = User.objects.create_superuser('admin', 'admin@example.com', '12435687abdn')
        Admin_user.groups.create(name='Admin')

        logged_in = self.client.login(username='admin', password='12435687abdn')
        self.assertTrue(logged_in)

        response = self.client.get('/admin_page')

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'admin.html')

        self.assertContains(response, 'Welcome back, admin')

    
    def test_template_rendering_template9(self):

        Admin_user = User.objects.create_superuser('admin', 'admin@example.com', '12435687abdn')
        Admin_user.groups.create(name='Admin')
   
        logged_in = self.client.login(username='admin', password='12435687abdn')
        self.assertTrue(logged_in)

        response = self.client.get('/analytics-dashboard')

        self.assertEqual(response.status_code, 200)


        self.assertTemplateUsed(response, 'analytics_dashboard.html')

        self.assertContains(response, '<h3 class="display-4 ms-5">Analytics Dashboard</h3>')
    
    def test_template_rendering_template10(self):

        Admin_user = User.objects.create_superuser('admin', 'admin@example.com', '12435687abdn')
        Admin_user.groups.create(name='Admin')
        
   
        logged_in = self.client.login(username='admin', password='12435687abdn')
        self.assertTrue(logged_in)

        response = self.client.get('/algorithm-dahshboard')

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'algorithm_dashboard.html')

        self.assertContains(response, '<h1 class="display-6">Algorithm Dashboard</h1>')

    def test_template_rendering_template11(self):
   
        Admin_user = User.objects.create_superuser('admin', 'admin@example.com', '12435687abdn')
        Admin_user.groups.create(name='Admin')
        
 
        logged_in = self.client.login(username='admin', password='12435687abdn')
        self.assertTrue(logged_in)

        response = self.client.get('/query-recruiters')

        self.assertEqual(response.status_code, 200)


        self.assertTemplateUsed(response, 'admin_search_feature/recruiters_db_query.html')

        self.assertContains(response, '<h3 class="display-6 mb-2">Search recruiters</h3>')


    def test_template_rendering_template12(self):
     
        Admin_user = User.objects.create_superuser('admin', 'admin@example.com', '12435687abdn')
        Admin_user.groups.create(name='Admin')
        
    
        logged_in = self.client.login(username='admin', password='12435687abdn')
        self.assertTrue(logged_in)

        response = self.client.get('/query-students')

     
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'admin_search_feature/students_db_query.html')

        self.assertContains(response, '<h3 class="display-6 mb-2">Search students</h3>')

    def test_template_rendering_template13(self):

        Admin_user = User.objects.create_superuser('admin', 'admin@example.com', '12435687abdn')
        Admin_user.groups.create(name='Admin')
    
        logged_in = self.client.login(username='admin', password='12435687abdn')
        self.assertTrue(logged_in)

        response = self.client.get('/query-internships')

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'admin_search_feature/internships_db_query.html')

       
        self.assertContains(response, '<h3 class="display-6 mb-2">Search live internships</h3>')

    def test_template_rendering_template14(self):
      
        Admin_user = User.objects.create_superuser('admin', 'admin@example.com', '12435687abdn')
        Admin_user.groups.create(name='Admin')
        
       
        logged_in = self.client.login(username='admin', password='12435687abdn')
        self.assertTrue(logged_in)

        response = self.client.get('/manage-companies')

        self.assertEqual(response.status_code, 200)

    
        self.assertTemplateUsed(response, 'companies_management_tool.html')

        
        self.assertContains(response, '<h3 class="display-6 mb-2">Register New Company</h3>')

    def test_template_rendering_template15(self):
      
        recruiter_user = User.objects.create_user(username='tesco', email= 'tesco@fskdgskhdfsjf.com', password='12435687abdn')
        recruiter_user.groups.create(name='Companies')  

        company = Company.objects.create(
            companyID = 'tesco',
            companyName = 'tesco',
            industrySector = 'retail',
            websiteURL = 'www',
        )
        recruiter = Recruiter.objects.create(
            fullName='tesco',
            recruiterID='tesco4', 
            companyID=company,
            jobTitle='tesco LD',
            email='tesco@fskdgskhdfsjf.com',
     
        )

        internship  = Internship.objects.create(
            internshipID = '123',
            companyID=company,
            recruiterID=recruiter,
            contractMode = 'Online',
            contractPattern = 'Full-Time',
            numberPositions = 2,
            field = 'tesco',
            title = 'tesco',
            minGPA = 66,
        )
        self.client.login(username='tesco', password='12435687abdn')
        
      
        internshipID = '123'  
        url = f'/recruiter-update/{internshipID}/'
        
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'recruiter_update.html')

       
        self.assertContains(response, '<h1>Internship Details</h1>')

    def test_template_rendering_template16(self):
 
        Admin_user = User.objects.create_superuser('admin', 'admin@example.com', '12435687abdn')
        Admin_user.groups.create(name='Admin')
        
        student = Student.objects.create(
            studentID = 800,
            fullName = 'homer',
            email = 'email@email.com',
            currProgramme = 'english',
            prevProgramme = 'english',
            studyMode= 'In-Person',
            studyPattern = 'Full-Time',
            GPA = 79,
            desiredContractLength = '12-weeks',
            willingRelocate = True,
            aspirations = 'Doughnuts'
            )
    
        logged_in = self.client.login(username='admin', password='12435687abdn')
        self.assertTrue(logged_in)

   
        studentID = '800'
        response = self.client.get(f'/student-details/{studentID}/')

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'student_details.html')

        self.assertContains(response, '<h1>Student Details</h1>')

    def test_template_rendering_template17(self):
       
        Admin_user = User.objects.create_superuser('admin', 'admin@example.com', '12435687abdn')
        Admin_user.groups.create(name='Admin')
        
        company = Company.objects.create(
            companyID = 'tesco',
            companyName = 'tesco',
            industrySector = 'retail',
            websiteURL = 'www',
        )
        recruiter = Recruiter.objects.create(
            fullName='tesco',
            recruiterID='tesco4',  
            companyID=company,
            jobTitle='tesco LD',
            email='tesco@fskdgskhdfsjf.com',
       
        )
        internship  = Internship.objects.create(
            internshipID = '123',
            companyID=company,
            recruiterID=recruiter,
            contractMode = 'Online',
            contractPattern = 'Full-Time',
            numberPositions = 2,
            field = 'tesco',
            title = 'tesco',
            minGPA = 66,
        )
       
        logged_in = self.client.login(username='admin', password='12435687abdn')
        self.assertTrue(logged_in)

     
        internshipID = '123'
        response = self.client.get(f'/internship-details/{internshipID}/')

    
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'internship_details.html')

        self.assertContains(response, '<h1>Internship Details</h1>')

    def test_template_rendering_template18(self):
        
        Admin_user = User.objects.create_superuser('admin', 'admin@example.com', '12435687abdn')
        Admin_user.groups.create(name='Admin')
        
        company = Company.objects.create(
            companyID = 'tesco',
            companyName = 'tesco',
            industrySector = 'retail',
            websiteURL = 'www',
        )
        recruiter = Recruiter.objects.create(
            fullName='tesco',
            recruiterID='tesco4',
            companyID=company,
            jobTitle='tesco LD',
            email='tesco@fskdgskhdfsjf.com',
          
        )

        logged_in = self.client.login(username='admin', password='12435687abdn')
        self.assertTrue(logged_in)

     
        recruiterID = 'tesco4'
        response = self.client.get(f'/recruiter-details/{recruiterID}/')

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'recruiter_details.html')

        self.assertContains(response, '<h1>Recruiters Details</h1>')
