Run the following commands in the terminal.
<!-- 1. Set up for web app (run once):
    - Create a virtual environment `python3 -m venv .venv`
    - Download libraries from requirements.txt `pip install -r requirements.txt` 
    (alternatively, run `pip install pandas dash dash-ag-grid plotly scipy`)
2. Activate virtual environment: `source .venv/bin/activate`
2. Create the database: `python load_data.py`
3. To run the web app which displays results of parts 1-4:
    - Run `python app.py`
    - Plotly Dash app will launch locally at `http://127.0.0.1:8050/` -->
1. `make setup`
2. `make pipeline`
3. `make dashboard`
4. A Plotly Dash app will launch locally at `http://127.0.0.1:8050/`
5. To delete the database file cell_counts.db and virtual environment .venv, run `clean`