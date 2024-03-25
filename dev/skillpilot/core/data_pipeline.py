import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from . models import *

"""
    The purpose of the CleanDataPipeline class is to group all functions related to 
    the processing and cleaning of data handled by the matchmaking algorithm
    and all its auxiliary functions
"""


def __init__(self):
    pass

# #round the score parameter to its closest multiple of 5, i.e. round_to_closest(63) = 65   
def roundGPA(gpa):
    # extract the unitary and decimal digit
    unitary, decimal = int(gpa) % 10, int(gpa)//10

    # round up or down based on the unitary digit
    if unitary < 5: 
        return decimal * 10
    elif unitary == 5: 
        return gpa
    else: 
        return (decimal + 1) * 10

def clean(program):
    program = program.split("-")
    study_mode, study_pattern = program[0], program[1]
    
    if study_mode == "N/A" and study_pattern == "N/A":
        # assume student is campus, fulltime
        return "Campus-FT"
    
    if study_mode == "N/A":
        # assume student in on-campus
        return f"Campus-{study_pattern}"
    
    if study_pattern == "N/A":
        # assume student is fulltime
        return f"{study_mode.capitalize()}-FT"
    
    # both entries are specified
    return f"{study_mode.capitalize()}-{study_pattern}"


def process_data():
    # Load internships and students data from the database
    internships = Internship.objects.all()
    students = Student.objects.all()
    
    #remove approved matches from queryset
    approved_matches = pd.read_csv('data/approved_offers.csv')

    for index, row in approved_matches.iterrows():
        if row['Candidate_id'] == id:
            student_id = row['Candidate_id']
            internship_id = row['Internship_id']
            students = students.exclude(pk=student_id)
            internship = internships.filter(pk=internship_id).first()
            if internship:
                internship.numberPositions -= 1
                if internship.numberPositions <= 0:
                    internships = internships.exclude(pk=internship_id)
    
    # Create DataFrames from the queryset data
    jobs = pd.DataFrame(list(internships.values()))
    candidates = pd.DataFrame(list(students.values()))

    # Display matplotlib plots inline
    plt.show()
    print("Original 'candidates' dataframe:")
    print(candidates.head())

    # Handle missing values in the "Experience" column
    candidates["currProgramme"].fillna("None", inplace=True)
    candidates.fillna("N/A", inplace=True)

    # Create the "StudyProgram" column by concatenating "StudyMode" and "StudyPattern"
    #candidates['StudyProgram'] = candidates[["studyMode", "studyPattern"]].agg('-'.join, axis=1)

    # Drop the unified columns
    #candidates.drop(["studyMode", "studyPattern"], axis=1, inplace=True)

    # Handle null-values in the StudyProgram column
    #candidates["CleanedStudyProgram"] = candidates["StudyProgram"].apply(clean)

    # Round the values in the MinScore column to the nearest 5%
    jobs['minGPA'] = jobs['minGPA'].apply(roundGPA)
    print(jobs.head())

    print("\n'candidates' dataframe after cleaning:")

    print(candidates.head())

    print("Processed data saved to 'processed_jobs.csv' and 'processed_candidates.csv'")

    # Return the processed dataframes
    return jobs, candidates
