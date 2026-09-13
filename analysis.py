from scipy.stats import mannwhitneyu
import pandas as pd

def compare_responders(df):
    '''
    Report which cell populations have a significant difference in relative 
    frequencies between responders and non-responders. 
    Statistics are needed to support any conclusion to convince Yah of Bob's findings. 
    '''
    results = []
    for population, pop_df in df.groupby('population'):
        yes = pop_df.loc[pop_df.response == 'yes', 'percentage']
        no = pop_df.loc[pop_df.response == 'no', 'percentage']
        _, p_val = mannwhitneyu(yes, no, alternative='two-sided')
        results.append({'population': population, 
                        'p_value': p_val, 
                        'significant? (p < 0.05)': 'Yes' if p_val < 0.05 else 'No'})
    return pd.DataFrame(results)

def summarize_part_4(df):
    '''
    Determine:
        How many samples from each project
        How many subjects were responders/non-responders 
        How many subjects were males/females
    '''
    samples_per_project = (
        df.groupby('project')['sample']
        .nunique()
        .reset_index(name='sample_count')
    )

    subjects = df.drop_duplicates(subset='subject')

    response_counts = (
        subjects['response']
        .value_counts()
        .reset_index(name='subject_count')
        .rename(columns={'index': 'response'})
    )

    sex_counts = (
        subjects['sex']
        .value_counts()
        .reset_index(name='subject_count')
        .rename(columns={'index': 'sex'})
    )

    return {
        'samples_per_project': samples_per_project,
        'response_counts': response_counts,
        'sex_counts': sex_counts,
    }
