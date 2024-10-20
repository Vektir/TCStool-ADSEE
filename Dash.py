import dash
from dash import dash_table
from dash import dcc, html
from dash.dependencies import Input, Output, State
#import dash_table
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
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        editable=True
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

# Callback to add a new column to the DataTable
@app.callback(
    Output('editable-table', 'columns'),
    Output('editable-table', 'data'),
    Output('add-column-message', 'children'),
    Input('add-column-button', 'n_clicks'),
    State('editable-table', 'columns'),
    State('new-column-name', 'value'),
    State('editable-table', 'data')
)
def add_column(n_clicks, columns, new_column_name, current_data):
    if n_clicks > 0 and new_column_name:
        # Check if the column already exists
        if any(col['name'] == new_column_name for col in columns):
            return columns, current_data, "Column already exists."
        
        # Add new column to columns list
        columns.append({'name': new_column_name, 'id': new_column_name})
        
        # Add new data to each row for the new column
        for row in current_data:
            row[new_column_name] = ""  # Initialize with empty string or a default value

        return columns, current_data, f"Column '{new_column_name}' added successfully!"

    return columns, current_data, ""

# Callback to update 'Better TCS data.csv', run calculations, and update orbiters data
@app.callback(
    [Output('output-message', 'children'),
     Output('orbiters-data-table', 'columns'),
     Output('orbiters-data-table', 'data')],
    [Input('save-button', 'n_clicks')],
    [State('editable-table', 'data')]
)
def update_csv(n_clicks, edited_data):
    if n_clicks > 0:
        # Convert the edited data back into a DataFrame
        df_updated = pd.DataFrame(edited_data)

        # Save the updated DataFrame back to the CSV file
        df_updated.to_csv('Better TCS data.csv', index=False)

        # Run calculations that update 'orbiters_data.csv'
        calculate_orbiters.RunCalculations()

        # Load the latest 'orbiters_data.csv' with error handling for encoding
        try:
            df_orbiters = pd.read_csv('orbiters_data.csv', encoding='ISO-8859-1')  # Specify the encoding here
        except UnicodeDecodeError:
            return "Error reading 'orbiters_data.csv' due to encoding issues.", [], []

        # Prepare the table columns and data
        columns = [{"name": i, "id": i} for i in df_orbiters.columns]
        data = df_orbiters.to_dict('records')

        return "CSV file and calculations updated successfully!", columns, data

    return "", [], []

# Run the app
if __name__ == '__main__':
    #webbrowser.open("http://127.0.0.1:8050/")
    app.run_server(debug=True) 
