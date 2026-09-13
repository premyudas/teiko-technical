import sqlite3
import pandas as pd

def load_cell_count(file):
    '''
    Table summary
        project: prj + int
        subject: sbj + int
        condition: carcinoma, healthy, melanoma
        age: 50-79
        sex: M, F
        treatment: miraclib, phauximab, none
        response: yes, no
        sample: sample + int
        sample_type: PBMC, WB
        time_from_treatment_start: 0, 7, 14
        b_cell: int
        cd8_t_cell: int
        cd4_t_cell: int
        nk_cell: int
        monocyte: int
    '''
    df = pd.read_csv(file)
    return df

def create_database(df):
    '''
    Creates a SQLite database file (`.db` extension) in the repository root.

    Schema (where * indicates primary key and FK indicates foreign key):
        subjects: subject*, project, condition, age, sex, treatment, response
        samples: sample*, subject(FK), sample type, time_from_treatment_start
        cell counts: id*, sample(FK), cell_population, cell_count
    '''
    conn = sqlite3.connect('cell_counts.db')
    cur = conn.cursor()
    
    # create tables from schema.sql
    with open('schema.sql', 'r') as schema_file:
        cur.executescript(schema_file.read())

    # populate tables using df
    # 1. subjects table
    subject_cols = ['subject', 'project', 'condition', 'age', 'sex', 'treatment', 'response']
    subjects = df[subject_cols].drop_duplicates(subset='subject')
    subjects.to_sql('subjects', conn, if_exists='replace', index=False)

    # 2. samples table
    sample_cols = ['sample', 'subject', 'sample_type', 'time_from_treatment_start']
    samples = df[sample_cols].drop_duplicates(subset='sample')
    samples.to_sql('samples', conn, if_exists='replace', index=False)

    # 3. cell_counts table
    population_cols = ['b_cell', 'cd8_t_cell', 'cd4_t_cell', 'nk_cell', 'monocyte']
    populations = df.melt(
        id_vars=['sample'],
        value_vars=population_cols,
        var_name='population',
        value_name='count'
    )
    populations.to_sql('cell_counts', conn, if_exists='replace', index=False)

    conn.commit()
    conn.close()

def main():
    '''
    Initializes the database with your schema.
    Loads all rows from cell-count.csv.
    '''
    df = load_cell_count('cell-count.csv')
    create_database(df)

if __name__ == '__main__':
    main()