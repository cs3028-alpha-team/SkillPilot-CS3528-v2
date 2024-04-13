import sys
import random
import pandas as pd
from time import time
import csv
from . models import *

"""
    The purpose of the GaleShapley class is to group all functions related to 
    the process of matching students to internships and it groups all the functions required 
    during this operation
"""

def compute_compatibility(student, internship):

    compatibility_score = 0

    # Check if students field of study matches with the internship field
    if student['prevProgramme'].iloc[0] == internship['field'].iloc[0]: compatibility_score += 1
    else: compatibility_score += 0.5

    if student['studyPattern'].iloc[0] == internship['contractPattern'].iloc[0]: compatibility_score += 1
    else: compatibility_score += 0.5

    # Assign a reduced factor based on how far off the MinGPA the student's GPA is
    student_gpa = student['GPA'].iloc[0]
    internship_min_gpa = internship['minGPA'].iloc[0]

    # Candidate will prefer job whose minGPA is closer to their achieved grade
    if student_gpa <= 0.9 * internship_min_gpa or student_gpa >= 1.1 * internship_min_gpa: compatibility_score += 1
    elif student_gpa <= 0.75 * internship_min_gpa or student_gpa >= 1.25 * internship_min_gpa: compatibility_score += 0.5
    else: compatibility_score += 0.25

    # Account for other factors such as location, pay, company title, etc.
    compatibility_score += random.random()

    return round(compatibility_score, 2)



def suitable_candidates(internshipID, matrix):
    # Retrieve the column with the key of company_index from the compatibility matrix
    company_column = matrix[internshipID]

    # Create a list of tuples where each tuple contains the candidate index and their compatibility score
    suit_cands = [ (studentID, matrix.loc[(studentID, internshipID)]) for studentID in matrix.index.tolist() ]

    # Sort the candidates by their compatibility score descending, so the company makes offers to the most relevant candidates first
    suit_cands.sort(key=lambda x: x[1], reverse=True)

    return suit_cands


def gale_shapley(offers, matrix, available_positions, max_iterations=10000):

    fulfillments = []  # Keep track of the number of fulfilled companies at each iteration
    iterations = 0
    
    while iterations < max_iterations:

        internshipID = None
        # find an internship with available_positions > 0
        for id, positions in available_positions.items():
            if positions > 0:
                internshipID = id 

        if internshipID is None: break

        # get a list of all candidates for this internship
        candidates = suitable_candidates(internshipID, matrix)
        all_reject = True
        

        for student in candidates:

            studentID = student[0]

            # if student has no offer yet
            if offers[studentID][0] is None:

                offers[studentID][0] = internshipID
                all_reject = False
                available_positions[internshipID] -= 1
                
                # add the internshipID which has been offered to the student into the student's 'do not consider' internship list, so 
                # we dont make the same offer again
                offers[studentID][1].append(internshipID)
                break
                
            else:
                # get index of current student offer
                k = offers[studentID][0]

                # obtain the compatibility score of proposed offer vs current offer
                prev_offer_score = matrix.loc[(studentID, k)]
                curr_offer_score = matrix.loc[(studentID, internshipID)]
                
                # if current offer is more compatible
                if curr_offer_score > prev_offer_score:

                    # make the swap
                    offers[studentID][0] = internshipID
                    all_reject = False
                    available_positions[k] += 1
                    available_positions[internshipID] = max(available_positions[internshipID]-1, 0)
              
                else:
                    # proposed offer is worse than current one, so add to 'do not consider ' list
                    offers[studentID][1].append(internshipID)
                    
        # all students rejected this company, so remove it from next iterations
        if all_reject:
            available_positions[internshipID] = 0
            
        # compute number of offers made at each iteration
        f = sum(1 for value in available_positions.values() if value == 0)
        fulfillments.append(f)
        iterations += 1
        
    if iterations >= max_iterations:
        print("Termination due to time-out")

    return [offers, fulfillments, available_positions]

