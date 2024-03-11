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
def __init__(self):

    pass

internships = Internship.objects.all()
students = Student.objects.all()

def populate_compatibility_matrix(matrix, candidates, jobs):
    for i in range(len(candidates)):
        for j in range(len(jobs)):
            print(f"i: {i}, j: {j}")
            matrix.loc[(i, j)] = compute_compatibility(candidates[i], jobs[j])

#for run algorithm
def populate_compatibility_matrix2(matrix, candidates, jobs):
    for i in range(len(candidates)):
        for j in range(len(jobs)):
            matrix.loc[(i, j)] = compute_compatibility2(candidates.loc[i], jobs.loc[j])
            

def compute_compatibility_matrix(students, internships):
    student_indices = [i for i in range(len(students))]
    internship_indices = [i for i in range(len(internships))]

    print("Student Indices:", student_indices)
    print("Internship Indices:", internship_indices)

    compatibility = pd.DataFrame(0.0, index=student_indices, columns=internship_indices)
    compatibility = compatibility.rename_axis(index='Student IDs', columns='Internship IDs')

    print("Populating the Compatibility matrix...")
    populate_compatibility_matrix(compatibility, students, internships)
    print("Population operation completed.")

    return compatibility

#for run algorithm 
def compute_compatibility_matrix2(students, internships):
    student_indices = [i for i in range(len(students))]
    internship_indices = [i for i in range(len(internships))]

    print("Student Indices:", student_indices)
    print("Internship Indices:", internship_indices)

    compatibility = pd.DataFrame(0.0, index=student_indices, columns=internship_indices)
    compatibility = compatibility.rename_axis(index='Student IDs', columns='Internship IDs')

    print("Populating the Compatibility matrix...")
    populate_compatibility_matrix2(compatibility, students, internships)
    print("Population operation completed.")

    return compatibility

def compute_compatibility(student, internship):
    compatibility_score = 0

    print("Student Data:")
    print(student)

    print("Internship Data:")
    print(internship)

    # Check if student's field of study matches with the internship field
    if student.currProgramme == internship.field:
        compatibility_score += 1
    else:
        compatibility_score += 0.5

    if student.studyPattern == internship.contractPattern:
        compatibility_score += 1
    else:
         compatibility_score += 0.5

    # Assign a reduced factor based on how far off the MinGPA the student's GPA is
    student_gpa = student.GPA
    internship_min_gpa = internship.minGPA

    if student_gpa <= 0.9 * internship_min_gpa or student_gpa >= 1.1 * internship_min_gpa:
        compatibility_score += 1
    elif student_gpa <= 0.75 * internship_min_gpa or student_gpa >= 1.25 * internship_min_gpa:
        compatibility_score += 0.5
    else:
        compatibility_score += 0.25

    # Account for other factors such as location, pay, company title, etc.
    compatibility_score += random.random()

    return round(compatibility_score, 2)

#for run algorithm 
def compute_compatibility2(candidate, job):
    compatibility_score = 0

    # Check if student has similar experience
    if candidate["currProgramme"] == job["field"]:
        compatibility_score += 1
    else:
        compatibility_score += 0.5

    # Assign a reduced factor based on how far off the MinScore the candidate's score is
    candidate_score = candidate["GPA"]
    job_minscore = job["minGPA"]

    # Candidate will prefer job whose MinScore is closer to their achieved grade
    if candidate_score <= 0.9 * job_minscore or candidate_score >= 1.1 * job_minscore:
        compatibility_score += 1
    elif candidate_score <= 0.75 * job_minscore or candidate_score >= 1.25 * job_minscore:
        compatibility_score += 0.5
    else:
        compatibility_score += 0.25

    # Account for a candidate preferring location, pay, company title etc.
    compatibility_score += random.random()

    return round(compatibility_score, 2)


# display all the offers made in a user-readable format
def format_pairings(offers, candidates, jobs, display=False):
    pairings = []
    for i in range(len(offers.keys()) - 1):
        candidate_id = i
        candidate_name = candidates.loc[candidate_id, "fullName"]
        job_title = "N/A" if offers[candidate_id][0] == None else jobs.loc[offers[candidate_id][0], "title"]

        # display parameter default to False
        if display:
            print(f'{candidate_name} -> {job_title}')

        pairing = (candidate_name, job_title)
        pairings.append(pairing)
    return pairings

# # Save final prodecced data to the offers csv
def save_results_to_csv(pairings, path):
    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Student', 'Internship'])
        writer.writerows(pairings)
    print('Matching algorithm executed successfully. Results saved to CSV file.')

# # =========================================================================== GALE_SHAPLEY.PY FUNCTIONS =======================================================================================
def find_job(company_ids):
    for i in range(len(company_ids)):
         if company_ids[i] >= 0: return i
    return -1 

def suitable_candidates(company_index, compatibility_matrix):
    # Retrieve the column with the key of company_index from the compatibility matrix
    company_column = compatibility_matrix[company_index]
    
    # Create a list of tuples where each tuple contains the candidate index and their compatibility score
    suit_cands = [(i, company_column[i]) for i in range(len(company_column))]
    
    # Sort the candidates by their compatibility score descending, so the company makes offers to the most relevant candidates first
    suit_cands.sort(key=lambda x: x[1], reverse=True)
    
    return suit_cands



def run_gale_shapley(candidates, jobs, number_of_candidates, number_of_jobs):
    
    print(f"\nRunning Gale-Shapley for {number_of_candidates} candidates and {number_of_jobs} jobs...")

    # reduce size of candidates and jobs dataframes 
    candidates_dataframe = candidates.loc[:number_of_candidates]
    print(candidates_dataframe)
    jobs_dataframe = jobs.loc[:number_of_jobs]
    print(jobs_dataframe)
    
    # compute the compatibility matrix
    compatibility_matrix = compute_compatibility_matrix2(candidates_dataframe, jobs_dataframe)
    print("jaskdgshldfhaljfihdsijlefioodslihoajufjohusl")
    print(compatibility_matrix)
    # keeps track of companies with job offers to still give out 
    company_ids = compatibility_matrix.columns.tolist()

    # keeps track of the offers made so far, candidate_id : (current_offer_company_id, [refusing_company_id1, ...])
    offers = { candidate_id : [None, []] for candidate_id in range(number_of_candidates + 1) }

    # keeps track of the number of positions left per job
    available_positions = [ jobs_dataframe.loc[job_id, "numberPositions"] for job_id in range(len(jobs_dataframe)) ]
    
    # compute the total number of positions across number_of_jobs jobs
    total_jobs = sum(available_positions)
    
    # run the Gale-Shapley algorithm between the jobs and candidates dataset
    offers, fulfillments = gale_shapley(company_ids, offers, compatibility_matrix, available_positions)

    return offers

def gale_shapley(company_ids, offers, compatibility_matrix, available_positions, max_iterations=10000):
    fulfillments = []  # Keep track of the number of fulfilled companies at each iteration
    iterations = 0
    
    while iterations < max_iterations:
        company_id = find_job(company_ids)
        
        if company_id == -1:
            break
            
        j = company_ids[company_id]
        comps = suitable_candidates(j, compatibility_matrix)
        all_reject = True
        
        for candidate in comps:
            candidate_id = candidate[0]
            
            if j not in offers[candidate_id][1]:
                
                if offers[candidate_id][0] is None:
                    offers[candidate_id][0] = j
                    all_reject = False
                    available_positions[j] -= 1
                    
                    if available_positions[j] == 0:
                        company_ids[j] = -1
                        break
                        
                    offers[candidate_id][1].append(company_id)
                    break
                    
                else:
                    k = offers[candidate_id][0]
                    prev_offer_score = compatibility_matrix.loc[candidate_id, k]
                    curr_offer_score = compatibility_matrix.loc[candidate_id, j]
                    
                    if curr_offer_score > prev_offer_score:
                        offers[candidate_id][0] = j
                        all_reject = False
                        available_positions[k] += 1
                        available_positions[j] -= 1
                        
                        if available_positions[k] == 1:
                            company_ids[k] = k    
                            
                        if available_positions[j] == 0:
                            company_ids[j] = -1  
                            
                    else:
                        offers[candidate_id][1].append(company_id)
                    break
                    
        if all_reject:
            company_ids[j] = -1
            
        fulfillments.append(company_ids.count(-1))
        iterations += 1
        
    if iterations >= max_iterations:
        print("Termination due to time-out")
    print(offers)
    print(fulfillments)
    return [offers, fulfillments]

