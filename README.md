# CS3528 Team Alpha - SkillPilot
Welcome to the GitHub repository for SkillPilot, an automated internship match-making software commissioned to Team Alpha by the university's school of medicine, medical sciences and nutrition. In this document you will find an explanation of what the application does and how to run it on your own machine, if you so wish. A [video](https://www.youtube.com/watch?v=YOUR_VIDEO_ID) demostration of the application in action can be found. 

### Running the application
In order to run the application you will need to have the following softwares installed and set-up on your computer
1. An IDE (i.e. Visual Studio Code)
2. Python 3.1 or above
3. Up-to-date Django Software

Once your development environment has been configured, travel to the project folder e.g. (SkillPilot-CS3528-v2\dev\skillpilot) and run the command ```python manage.py runserver``` the terminal. Download all needed imports, the command line will tell you how to download them (if any are missed). 

![image](https://github.com/cs3028-alpha-team/SkillPilot-CS3528-v2/assets/114080696/7a1a22f1-4423-405d-8325-924def412414)
   
### Skillpilot navigation
On the navigation bar you should see "help", click on this and it should navigate you to a page explaining steps for each type of user.

### Login Credentials
1. The login for the admin account will be provided to you upon request 
2. A student account can be created from sign-up. A premade student login: username = mattia, password = 12435687abdn
3. A recruiter account can be created from sign-up. The recruiter accounts needs a recruiter token, so login as an admin first and navigate to the company management tool here create a new company. Take note of the "recruiter Token" as this is needed for a recruiter account sign-up. After taken note of the recruiter token logout by clicking logout on the navigation bar, and try sign up as a recruiter using the new recruiter token. A premade recruiter login: username = tesco, password = 12435687abdn, recruiter token = tesco123.

### Commands to run tests
To run the tests navigate to the project folder and run the command ```python manage.py test > test_log.txt 2>&1```. After running the command a test_log.txt should be created navigate to see the result. 

### Folder explanations 
1. The project folder is dev/skillpilot
2. The folder "core" contains files created by Team alpha used to run the application
3. The templates folder contains the html for the pages, they are seperated by meaning such as the login pages are withing the auth folder
4. The static folder contains folder for stylign and images used
5. The tests folder shows all the test files that contain test code used to ensure the application is working correctly
6. There are also python files that contain code to run the application such as views.py holds functions used to sign up, delete accounts, etc...
7. Outside the core file there is a skillpilot file that is created by django when the application was created. This contains files django files for the project, such as settings.py contains django settings for the skillpilot project. 
9. There are also files outside the skillpilot and core, such as the database called 'dp.sqlite3'.




