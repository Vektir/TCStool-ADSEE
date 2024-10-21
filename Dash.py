import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
#import dash_table
from dash import dash_table
import pandas as pd
import calculate_orbiters
import webbrowser

# Load the initial CSV file
df = pd.read_csv('Better TCS data.csv')

# Initialize the app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    # Title
    html.H1("Editable CSV Table and Updated Orbiter Data"),

    # Editable Table for 'Better TCS data.csv'
    dash_table.DataTable(
        id='editable-table',
        columns=[{"name": f"{i}  ", "id": i, "deletable": True} for i in df.columns],  # Add space for button
        data=df.to_dict('records'),
        editable=True,
        style_header={
            'whiteSpace': 'normal',
            'height': 'auto'
        },
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto'
        }
    ),

    # Input for new column name
    dcc.Input(id='new-column-name', type='text', placeholder='Enter new column name'),
    html.Button('Add New Column', id='add-column-button', n_clicks=0),
    html.Div(id='add-column-message'),

    # Button to save edits to 'Better TCS data.csv' and run calculations
    html.Button('Save and Run Calculations', id='save-button', n_clicks=0),
    html.Div(id='output-message'),

    # Live updating table for 'orbiters_data.csv'
    html.H3("Updated Orbiter Data"),
    dash_table.DataTable(
        id='orbiters-data-table',
        columns=[],  # Will be updated after button click
        data=[]
    )
])

# Combined callback to handle adding a new column, deleting a column, and saving the data
@app.callback(
    [Output('editable-table', 'columns'),
     Output('editable-table', 'data'),
     Output('add-column-message', 'children'),
     Output('output-message', 'children'),
     Output('orbiters-data-table', 'columns'),
     Output('orbiters-data-table', 'data')],
    [Input('add-column-button', 'n_clicks'),
     Input('save-button', 'n_clicks')],
    [State('new-column-name', 'value'),
     State('editable-table', 'columns'),
     State('editable-table', 'data')]
)
def handle_table_updates(add_column_n_clicks, save_button_n_clicks, new_column_name, current_columns, current_data):
    # Distinguish which button was clicked
    triggered_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    
    if triggered_id == 'add-column-button' and add_column_n_clicks > 0:
        # Adding a new column
        if new_column_name and not any(col['name'] == new_column_name for col in current_columns):
            current_columns.append({'name': new_column_name, 'id': new_column_name})
            for row in current_data:
                row[new_column_name] = ""  # Initialize new column data
            return current_columns, current_data, f"Column '{new_column_name}' added successfully!", "", [], []

        return current_columns, current_data, "Column already exists or no column name entered.", "", [], []

    elif triggered_id == 'save-button' and save_button_n_clicks > 0:
        # Saving the data and updating orbiter data
        df_updated = pd.DataFrame(current_data)
        df_updated.to_csv('Better TCS data.csv', index=False)

        # Run calculations that update 'orbiters_data.csv'
        calculate_orbiters.RunCalculations()

        # Load the latest 'orbiters_data.csv'
        try:
            df_orbiters = pd.read_csv('orbiters_data.csv', encoding='ISO-8859-1')
            orbiter_columns = [{"name": i, "id": i} for i in df_orbiters.columns]
            orbiter_data = df_orbiters.to_dict('records')
            return current_columns, current_data, "", "CSV file and calculations updated successfully!", orbiter_columns, orbiter_data
        except UnicodeDecodeError:
            return current_columns, current_data, "", "Error reading 'orbiters_data.csv' due to encoding issues.", [], []

    # Default return when no action is taken
    return current_columns, current_data, "", "", [], []


# Run the app
if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:8050/")
    app.run_server(debug=True)
