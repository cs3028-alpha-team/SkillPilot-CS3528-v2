import pandas as pd

"""
    The purpose of the DataPipeline class is to group all functions related to 
    the processing and cleaning of data handled by the matchmaking algorithm
    and all its auxiliary functions
"""

class DataPipeline:

    # instantiate the class with students and internships dataframes
    def __init__(self, students, internships):
        self.students = students
        self.internships = internships


    # encapsulate the cleaning operations in one method 
    def clean(self):        

        # handle cases where student's studyMode or studyPatter are null
        for i in self.students.index.tolist():

            if not self.__check_studymode(self.students.loc[(i, 'studyMode')]):
                self.students.loc[(i, 'studyMode')] = 'in-person'
            if not self.__check_studypattern(self.students.loc[(i, 'studyPattern')]):
                self.students.loc[(i, 'studyPattern')] = 'FT'

            # round student GPA to closest multiple of 5
            self.students.loc[(i, 'GPA')] = self.__round(self.students.loc[(i, 'GPA')])

        # round internship min GPA to closest multiple of 5
        for i in self.internships.index.tolist():
            self.internships.loc[(i, 'minGPA')] = self.__round(self.internships.loc[(i, 'minGPA')])

        return [ self.students, self.internships ]


    def __round(self, n):
        # extract the unitary digit
        unitary, decimal = int(n) % 10, int(n)//10
        
        # round up or down based on unitary digit
        if unitary < 5: return decimal * 10
        if unitary == 5: return n
        else: return (decimal + 1) * 10

    def __check_studymode(self, mode):
        return mode in ['in-person', 'online', 'hybrid']

    def __check_studypattern(self, pattern):
        return pattern == 'PT' or pattern == 'FT'