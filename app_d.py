from dash import Dash, dcc, html, Input, Output,dash_table
import pandas as pd
import numpy as np
import re

df = pd.read_csv('./text_segment2.csv')
df['child_category_score'] = df['child_category_score']*100
df = df.rename(columns={'text':'Text', 'pagenum': 'Pagenum', 'doc_name': 'Doc_name' })
l = sorted(df.parent_category.unique())
df['breakdown_by'] = df['breakdown_by'].apply(lambda x: x.capitalize())
df['breakdown_by'] = df['breakdown_by'].apply(lambda x: re.sub('[^a-zA-Z]',' ',x))

app = Dash(__name__)
server = app.server

dropdown= html.Div([
    html.H1("Taxonomic Breakdown of Texts", style={'textAlign': 'center'}),
    html.H3('Parent Category:',style={'textAlign':'centre'}),

    dcc.Dropdown(id='First', options=l, clearable=False,style={'padding': 5}),

    html.H3('Child Category:'),

    html.Div([
        dcc.Dropdown(id='Second', options=[],style={'padding': 5},clearable=False),
    ]),
    html.H3('Breakdown By:'),

    html.Div([
        dcc.Dropdown(id='Third', options=[],style={'padding': 5},clearable=False),
    ]),

    html.Div([html.H3('Select Range',style={'textAlign': 'center'}),
    dcc.RangeSlider(
                min = 20,
                max = 100,
                tooltip = {'placement': 'bottom', 'always_visible':True},
                step = 5,
                value=[20,100],
                updatemode='drag',
                id='my-slider'
    )])        
    
],style={"margin": 30}
)

final_table = html.Div([dash_table.DataTable(id="final_table",
style_data={
        'whiteSpace': 'normal',
        'height': 'auto',
        'border': '1px solid brown'
    },fill_width=False,
    style_header={'textAlign': 'left', "fontWeight": "bold",'border': '1px solid brown','backgroundColor': 'rgb(210, 210, 210)'},
    style_cell={'textAlign': 'left','padding':'5px'},
    style_table={'height': '500px','overflowY': 'auto'},
    )],style={"margin": 30}
    )

app.layout = html.Div([dropdown, final_table])


@app.callback(
    Output('Second', 'options'),
    Input('First', 'value')
)

def set_child_category_option(choose_parent_category):
    l1 = df[df['parent_category']==choose_parent_category]
    return [{'label':c, 'value':c}for c in np.unique(list(l1['child_category']))]

@app.callback(
    Output('Third', 'options'),
    Input('Second', 'value')
)

def set_child_category_option(choose_child_category):
    l2 = df[df['child_category']==choose_child_category]
    return [{'label':c, 'value':c}for c in l2['breakdown_by'].unique()]

@app.callback(
    Output('final_table', 'data'),
    [Input('Second', 'value'),
    Input('First','value'),
    Input('my-slider','value')]

)

def set_table_data(b,a,slider_range):
    
    dff = df[(df['parent_category']== a)]
    dff = dff[dff['child_category_score'].between(slider_range[0],slider_range[1])]
    dff = dff[(dff['child_category']==b)]
    dff = dff.sort_values(by=['child_category_score'],ascending=False)
    dff = dff[['Text','Pagenum','Doc_name']]
    dff = dff.to_dict('records')
    return dff



if __name__ == '__main__':
    app.run_server(debug=True)
