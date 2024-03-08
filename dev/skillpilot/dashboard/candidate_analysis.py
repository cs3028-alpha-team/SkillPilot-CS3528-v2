import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('agg')

# Code to show the candidate histogram, called in views.py by def candidate_histogram function
def candidate_histogram_code(candidates):

    sns.set_theme(style="ticks")
    sns.color_palette("PuOr", as_cmap=True)
    plt.figure(figsize=(10, 4))
    
    chart = sns.histplot(
        data=candidates, 
        x="Score", 
        multiple="stack", 
        hue='StudyProgram',
        edgecolor=".3", 
        bins=50, 
        linewidth=.5, 
        kde=True

    )
    return chart
    

# Integrate chat to display job count

def course_count(candidates):
    plt.figure(figsize=(9, 3))
    
    # histogram plot of scores split between different study-programs
    chart = sns.countplot(
        data=candidates, 
        x='Course', 
        palette='RdBu', 
        orient="v"
    )
    
    # configure labels along the x-axis
    chart.set_xticklabels(
        chart.get_xticklabels(),
        rotation=60,
        ha="right",
        rotation_mode='anchor'
    )
    
    return chart



#============== Jobs Analysis ================

def job_min_score_count(jobs):
    # countplot of companies grouped according to the minimum scored required for their positions
    chart = sns.countplot(
        data=jobs, 
        x='MinScore', 
        palette='Set2',
        orient="v"
    )

    # Return the seaborn countplot object
    return chart



def jobs_remaining_vs_iterations_call(request):
    # Load data from CSV files
    # For example, assuming you have CSV files named candidates.csv and jobs.csv
    candidates_df = pd.read_csv('data/processed_candidates.csv')
    jobs_df = pd.read_csv('data/processed_jobs.csv')
    
    
    number_of_candidates = len(candidates_df)
    number_of_jobs = len(jobs_df)
    
    performance_data = [run_gale_shapley(number_of_candidates, number_of_jobs, candidates_df, jobs_df) 
                        for _ in range(25, 125, 25) 
                        for _ in range(100, 1100, 100)]
    
  
    plot_jobs_remaining_vs_iterations(performance_data)

    # NEED  CODE TO OUPUT TO CSV 
    
    return HttpResponse("Plot generated successfully.")


def plot_jobs_remaining_vs_iterations(performance_data):
    plt.figure(figsize=(21, 10))
    sns.set(style="whitegrid")

    iterations_outer_index = [i for i in range(100, 1100, 100)]
    iterations_inner_index = [i for i in range(25, 125, 25)]
    iterations_multi_index = pd.MultiIndex.from_product([iterations_outer_index, iterations_inner_index], names=['Candidates', 'Jobs Advertised'])

    iterations_data = {
        'Iterations': [data_tuple[1] for data_tuple in performance_data],
        'Jobs Remaining': [data_tuple[0] for data_tuple in performance_data],
    }

    iterations_df = pd.DataFrame(data=iterations_data, index=iterations_multi_index)

    for i in range(len(iterations_df)):
        curr_row = iterations_df.iloc[i]
        
        jobs_remaining_list = curr_row['Jobs Remaining']

        df_curr_row = pd.DataFrame(
            {'Iterations': range(1, len(jobs_remaining_list) + 1), 
             'Jobs Remaining': jobs_remaining_list}
        )

        sns.lineplot(data=df_curr_row, x='Iterations', y='Jobs Remaining')

    plt.title('Jobs Remaining vs Iterations')
    plt.xlabel('Iterations')
    plt.ylabel('Jobs Remaining')
    plt.show()