import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

"""
    The purpose of the CleanDataPipeline class is to group all functions related to 
    the processing and cleaning of data handled by the matchmaking algorithm
    and all its auxiliary functions
"""
class CleanDataPipeline():

    def __init__(self):
        pass

    # # round the score parameter to its closest multiple of 5, i.e. round_to_closest(63) = 65   
    # def roundGPA(self, gpa):
    #     # extract the unitary and decimal digit
    #     unitary, decimal = int(gpa) % 10, int(gpa)//10

    #     # round up or down based on the unitary digit
    #     if unitary < 5: 
    #         return decimal * 10
    #     elif unitary == 5: 
    #         return gpa
    #     else: 
    #         return (decimal + 1) * 10


    # def clean(self, program):
    #     program = program.split("-")
    #     study_mode, study_pattern = program[0], program[1]
        
    #     if study_mode == "N/A" and study_pattern == "N/A":
    #         # assume student is campus, fulltime
    #         return "Campus-FT"
        
    #     if study_mode == "N/A":
    #         # assume student in on-campus
    #         return f"Campus-{study_pattern}"
        
    #     if study_pattern == "N/A":
    #         # assume student is fulltime
    #         return f"{study_mode.capitalize()}-FT"
        
    #     # both entries are specified
    #     return f"{study_mode.capitalize()}-{study_pattern}"


    # def process_data():
    #     # Load jobs and candidates data
    #     jobs = pd.read_csv('data/jobs.csv')
    #     candidates = pd.read_csv('data/candidates.csv')

    #     # Display matplotlib plots inline
    #     plt.show()
    #     print("Original 'candidates' dataframe:")
    #     print(candidates.head())

    #     # Handle missing values in the "Experience" column
    #     candidates["Experience"].fillna("None", inplace=True)
    #     candidates.fillna("N/A", inplace=True)

    #     # Create the "StudyProgram" column by concatenating "StudyMode" and "StudyPattern"
    #     candidates['StudyProgram'] = candidates[["StudyMode", "StudyPattern"]].agg('-'.join, axis=1)

    #     # Drop the unified columns
    #     candidates.drop(["StudyMode", "StudyPattern"], axis=1, inplace=True)

    #     # Handle null-values in the StudyProgram column
    #     candidates["CleanedStudyProgram"] = candidates["StudyProgram"].apply(clean)

    #     # Round the values in the MinScore column to the nearest 5%
    #     jobs['MinScore'] = jobs['MinScore'].apply(round_to_closest)
    #     print(jobs.head())

    #     print("\n'candidates' dataframe after cleaning:")

    #     print(candidates.head())
    # # Save the processed dataframes to CSV files
    # #jobs.to_csv('processed_jobs.csv', index=False)
    # #candidates.to_csv('processed_candidates.csv', index=False)

    # print("Processed data saved to 'processed_jobs.csv' and 'processed_candidates.csv'")

    # # Return the processed dataframes
    # return jobs, candidates