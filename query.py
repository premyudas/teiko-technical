import sqlite3
import pandas as pd

DB_PATH = 'cell_counts.db'

def get_connection():
    return sqlite3.connect(DB_PATH)

def part_2():
    '''
    Part 2: Initial Analysis - Data Overview
    
    Create summary table of the relative frequency of each cell population per sample.
    Each row represents one population from one sample and should have the following columns:
        sample: the sample id as in column sample in cell-count.csv
        total_count: total cell count of sample
        population: name of the immune cell population (e.g. b_cell, cd8_t_cell, etc.)
        count: cell count
        percentage: relative frequency in percentage
    '''

    query = '''
        SELECT
            samples.sample,
            SUM(cell_counts.count) OVER (PARTITION BY samples.sample) AS total_count,
            cell_counts.population,
            cell_counts.count,
            (cell_counts.count * 100.0) / SUM(cell_counts.count) OVER (PARTITION BY samples.sample) AS percentage
        FROM cell_counts
        JOIN samples ON cell_counts.sample = samples.sample
    '''
    with get_connection() as con:
        return pd.read_sql_query(query, con)

def part_3():
    '''
    Part 3: Statistical Analysis
    
    Subset melanoma patients receiving miraclib who respond (responders) versus 
    those who do not (non-responders); only include PBMC samples.
    Compare the differences in cell population relative frequencies of responders vs. non-responders.
    '''

    query = '''
        SELECT
            samples.sample,
            subjects.response,
            cell_counts.population,
            100.0 * cell_counts.count / SUM(cell_counts.count) OVER (PARTITION BY samples.sample) AS percentage
        FROM cell_counts
        JOIN samples ON cell_counts.sample = samples.sample
        JOIN subjects ON samples.subject = subjects.subject
        WHERE subjects.condition = 'melanoma'
            AND subjects.treatment = 'miraclib'
            AND samples.sample_type = 'PBMC'
    '''
    with get_connection() as con:
        return pd.read_sql_query(query, con)

def part_4():
    '''
    Part 4: Data Subset Analysis.

    1. Identify all melanoma PBMC samples at baseline (time_from_treatment_start is 0) 
    from patients who have been treated with miraclib. 
    '''

    query = '''
        SELECT 
            subjects.subject, 
            subjects.project, 
            subjects.age,
            subjects.sex, 
            subjects.response, 
            samples.sample
        FROM samples
        JOIN subjects ON samples.subject = subjects.subject
        WHERE subjects.condition = 'melanoma'
            AND subjects.treatment = 'miraclib'
            AND samples.sample_type = 'PBMC'
            AND samples.time_from_treatment_start = 0
    '''
    with get_connection() as con:
        return pd.read_sql_query(query, con)

def avg_bcells_melanoma_male_responders_t0():
    query = """
        SELECT cell_counts.count
        FROM cell_counts
        JOIN samples ON cell_counts.sample = samples.sample
        JOIN subjects ON samples.subject = subjects.subject
        WHERE subjects.condition = 'melanoma'
          AND subjects.sex = 'M'
          AND subjects.response = 'yes'
          AND samples.time_from_treatment_start = 0
          AND cell_counts.population = 'b_cell'
    """
    with get_connection() as conn:
        df = pd.read_sql_query(query, conn)
    return df["count"].mean()