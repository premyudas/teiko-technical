from dash import Dash, dcc, html
import dash_ag_grid as dag
import plotly.express as px
from query import part_2, part_3, part_4, avg_bcells_melanoma_male_responders_t0
from analysis import compare_responders, summarize_part_4

app = Dash(__name__)

def make_table(df, table_id, paginated=False):
    grid_options = {
        'autoSizeStrategy': {
                'type': 'fitCellContents',
                'scaleUpToFitGridWidth': True,
        },
        'domLayout': 'autoHeight',
        'suppressFieldDotNotation': True,
    }
    if paginated:
        grid_options['pagination'] = True
        grid_options['paginationPageSize'] = 10

    return dag.AgGrid(
        id=table_id,
        rowData=df.to_dict('records'),
        columnDefs=[{'field': col, 'headerName': col} for col in df.columns],
        defaultColDef={'sortable': True, 'filter': True, 'resizable': True},
        columnSize='sizeToFit',
        dashGridOptions=grid_options,
        style={'marginBottom': '16px'},
    )

frequency_df = part_2()

responder_df = part_3()
box_plot = px.box(responder_df, x='population', y='percentage', color='response')
box_plot.update_traces(boxmean=True) 
responder_stats_df = compare_responders(responder_df)

subset_df = part_4()
subset_df_summarized = summarize_part_4(subset_df)
avg_bcells = avg_bcells_melanoma_male_responders_t0()

app.layout = html.Div([
    html.H1('Teiko Technical'),

    html.H2('Part 2: Initial Analysis - Data Overview'),
        html.Div('Relative frequency of each cell population per sample'),
        make_table(frequency_df.round(2), 'frequency-table', paginated=True),

    html.H2('Part 3: Statistical Analysis'),
        html.Div('Cell population relative frequencies of melanoma patients receiving miraclib (responders vs. non-responders)'),
        dcc.Graph(figure=box_plot),

        html.Div('Mann-Whitney U test to determine which cell populations have a significant difference in relative frequencies between responders and non-responders'),
        make_table(responder_stats_df.round(2), 'statistics-table'),

    html.H2('Part 4: Data Subset Analysis'),
        html.Div('Melanoma PBMC samples at baseline (t=0) from patients who have been treated with miraclib.'),
        make_table(subset_df, 'project-counts-grid', paginated=True),

        html.Div('Number of samples from each project'),
        make_table(subset_df_summarized['samples_per_project'], 'samples-per-project-table'),
        
        html.Div('Number of responders vs. non-responders'),
        make_table(subset_df_summarized['response_counts'], 'response-counts-table'),
        
        html.Div('Number of male vs. female subjects'),
        make_table(subset_df_summarized['sex_counts'], 'sex-counts-table'),
        
        html.Div(f'''The average number of B cells for responders at time=0 of 
                Melanoma males of all sample and treatment types is: {round(avg_bcells, 2)}.''')
])

if __name__ == '__main__':
    app.run(debug=True)