import sys
import random
import pandas as pd
from time import time
import csv

"""
    The purpose of the GaleShapley class is to group all functions related to 
    the process of matching students to internships and it groups all the functions required 
    during this operation
"""
class GaleShapley():

    def __init__(self):

        pass

# # =========================================================================== GALE_SHAPLEY_UTIL_FUNCTIONS.PY FUNCTIONS =======================================================================================
# # Read CSV files (ADDED)
# candidates = pd.read_csv('data/candidates.csv')
# jobs = pd.read_csv('data/jobs.csv')

# # Populate the compatibility matrix using the jobs and candidates dataframe
# def populate_compatibility_matrix(matrix, candidates, jobs):
#     for i in range(len(candidates)):
#         for j in range(len(jobs)):
#             matrix.loc[(i, j)] = compute_compatibility(candidates.loc[i], jobs.loc[j])
            
# # Compute the compatibility matrix for the given dataframes
# def compute_compatibility_matrix(candidates, jobs): #NOTE need to change to compatibility_matrix
#     # use jobs and candidates indices instead of fullname and company as it guarantees uniqueness
#     jobs_indices = [i for i in range(len(jobs))]
#     candidate_indices = [i for i in range(len(candidates))]

#     # create the compatibility dataframe/matrix
#     compatibility = pd.DataFrame(0.0, index=candidate_indices, columns=jobs_indices)
#     compatibility = compatibility.rename_axis(index='Candidate IDs', columns='Job IDs')

#     # populate the compatibility matrix
#     print("Populating the Compatibility matrix...")
#     populate_compatibility_matrix(compatibility, candidates, jobs)
#     print("Population operation completed.")

#     return compatibility

# # Return a score to classify the compatibility of a candidate to a job
# def compute_compatibility(candidate, job):
#     compatibility_score = 0

#     # Check if student has similar experience
#     if candidate["Experience"] == job["Field"]:
#         compatibility_score += 1
#     else:
#         compatibility_score += 0.5

#     # Assign a reduced factor based on how far off the MinScore the candidate's score is
#     candidate_score = candidate["Score"]
#     job_minscore = job["MinScore"]

#     # Candidate will prefer job whose MinScore is closer to their achieved grade
#     if candidate_score <= 0.9 * job_minscore or candidate_score >= 1.1 * job_minscore:
#         compatibility_score += 1
#     elif candidate_score <= 0.75 * job_minscore or candidate_score >= 1.25 * job_minscore:
#         compatibility_score += 0.5
#     else:
#         compatibility_score += 0.25

#     # Account for a candidate preferring location, pay, company title etc.
#     compatibility_score += random.random()

#     return round(compatibility_score, 2)

# # display all the offers made in a user-readable format
# def format_pairings(offers, candidates, jobs, display=False):
#     pairings = []
#     for i in range(len(offers.keys()) - 1):
#         candidate_id = i
#         candidate_name = candidates.loc[candidate_id, "Fullname"]
#         job_title = "N/A" if offers[candidate_id][0] == None else jobs.loc[offers[candidate_id][0], "Title"]

#         # display parameter default to False
#         if display:
#             print(f'{candidate_name} -> {job_title}')

#         pairing = (candidate_name, job_title)
#         pairings.append(pairing)
#     return pairings

# # Save final prodecced ata to the offers csv
# def save_results_to_csv(pairings, path):
#     with open(path, 'w', newline='') as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(['Candidate', 'Job']) 
#         for pairing in pairings:
#             writer.writerow(pairing) 
#     print('Matching algorithm executed successfully. Results saved to CSV file.')
    

# # =========================================================================== GALE_SHAPLEY.PY FUNCTIONS =======================================================================================

# # given a list of jobs, return the index of a job with offers to still give out, or -1 if none are found
# def find_job(company_ids):
#     for i in range(len(company_ids)):
#         if company_ids[i] >= 0: return i
#     return -1  

# def suitable_candidates(company_index, compatibility_matrix):
#     # retrieve the column with key of company_index from the compatibility matrix
#     # print("Company index:", company_index)
#     # print("Compatibility matrix shape:", compatibility_matrix.shape)
#     suit_cands = [(i, compatibility_matrix[company_index][i]) for i in range(len(compatibility_matrix[company_index]))]
#     # print("Suitable candidates:", suit_cands)
    
#     # sort the candidates by their compatibility score descending, so company makes offer to most relevant candidates first
#     suit_cands.sort(key = lambda x: x[1])
    
#     return suit_cands


# #@benchmark
# # run the gale-shapley algorithm on the input candidates and jobs sets
# def gale_shapley(company_ids, offers, compatibility_matrix, available_positions, max_iterations=10000):
    
#     # keep track of number of companies fulfilled at each iteration
#     fulfillments = []
#     iterations = 0
    
#     # trigger time-out when algorithm reaches a stagnant point
#     while iterations < max_iterations:
        
#         # find a company with job offers to give out
#         company_id = find_job(company_ids)
        

#         # stop condition when all companies have given out jobs
#         if company_id == -1: break
            
#         # job J with positions still to fill-out
#         j = company_ids[company_id]
        
#         # find most compatible candidate who company j has not offered a job to yet
#         comps = suitable_candidates(j, compatibility_matrix)
        
#         # check whether all students reject this company
#         all_reject = True
        
#         for candidate in comps:
#             candidate_id = candidate[0]
            
#             # make an offer to this candidate
#             if j not in offers[candidate_id][1]:
                
#                 # check if candidate has no offer yet
#                 if offers[candidate_id][0] == None:
                    
#                     # make the offer 
#                     offers[candidate_id][0] = j
                    
#                     # change reject status
#                     all_reject = False
                    
#                     # reduce number of jobs available for job j
#                     available_positions[j] -= 1
                    
#                     # check number of positions 
#                     if available_positions[j] == 0:
                        
#                         # all positions have been filled
#                         company_ids[j] = -1
#                         break
                        
#                     # make sure this company cannot make another offer to the same candidate
#                     offers[candidate_id][1].append(company_id)
#                     break
                    
#                 else:
#                     # make offer, then candidate chooses the company they compare best with
#                     k = offers[candidate_id][0] # id of company candidate has an offer from
#                     prev_offer_score = compatibility_matrix.loc[candidate_id, k]
#                     curr_offer_score = compatibility_matrix.loc[candidate_id, j]
                    
#                     if curr_offer_score > prev_offer_score:
                        
#                         # candidate accepts new offer 
#                         offers[candidate_id][0] = j
                        
#                         # change reject status
#                         all_reject = False
                        
#                         # old offer now becomes free
#                         available_positions[k] += 1
                        
#                         # current job position is not available to other candidates, so decrement
#                         available_positions[j] -= 1
                        
#                         # check if old job has new positions free
#                         if available_positions[k] == 1: company_ids[k] = k    
                            
#                         # check if new job has been completely filled out
#                         if available_positions[j] == 0: company_ids[j] = -1  
                            
#                     else:
#                         # candidate rejects new offer - add this company to the banned list for this candidate
#                         offers[candidate_id][1].append(company_id)
#                     break
                    
#         # if company rejected by all students, then remove it from being considered next
#         if all_reject: company_ids[j] = -1
            
#         # save number of fulfilled companies after current iteration
#         fulfillments.append(company_ids.count(-1))
#         iterations += 1
        
#     if iterations >= max_iterations: print("Termination due to time-out")
        
#     return [offers, fulfillments]

# # run the Gale-Shapley algorithm for a range of candidates and jobs
# def run_gale_shapley(candidates, jobs, number_of_candidates, number_of_jobs):
    
#     print(f"\nRunning Gale-Shapley for {number_of_candidates} candidates and {number_of_jobs} jobs...")

#     # reduce size of candidates and jobs dataframes 
#     candidates_dataframe = candidates.loc[:number_of_candidates]
#     jobs_dataframe = jobs.loc[:number_of_jobs]
    
#     # compute the compatibility matrix
#     compatibility_matrix = compute_compatibility_matrix(candidates_dataframe, jobs_dataframe)

#     # keeps track of companies with job offers to still give out 
#     company_ids = compatibility_matrix.columns.tolist()

#     # keeps track of the offers made so far, candidate_id : (current_offer_company_id, [refusing_company_id1, ...])
#     offers = { candidate_id : [None, []] for candidate_id in range(number_of_candidates + 1) }

#     # keeps track of the number of positions left per job
#     available_positions = [ jobs_dataframe.loc[job_id, "Positions"] for job_id in range(len(jobs_dataframe)) ]
    
#     # compute the total number of positions across number_of_jobs jobs
#     total_jobs = sum(available_positions)
    
#     # run the Gale-Shapley algorithm between the jobs and candidates dataset
#     offers, fulfillments = gale_shapley(company_ids, offers, compatibility_matrix, available_positions)

#     return offers