#!pip install --quiet jupyter-dash pyngrok

#import dash 
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from pyngrok import ngrok
import pandas as pd
import dash
from dash.dependencies import Input, Output
from datetime import datetime
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime

def download_data(begin_year, begin_month, begin_day, begin_hr, begin_min, end_year, end_month, end_day, end_hr, end_min):
  cred = credentials.Certificate("./serviceAccountKey.json")
  firebase_admin.initialize_app(cred, {"databaseURL": "https://three-buddy-default-rtdb.firebaseio.com/"})

  # begin = datetime(year=2021, month=9, day=7, hour=7, minute=1, second=0)
  begin = datetime(year=begin_year, month=begin_month, day=begin_day, hour=begin_hr, minute=begin_min, second=0)
  beginTimestamp = datetime.timestamp(begin)

  # end = datetime(year=2021, month=9, day=7, hour=7, minute=10, second=0)
  end = datetime(year=end_year, month=end_month, day=end_day, hour=end_hr, minute=end_min, second=0)
  endTimestamp = datetime.timestamp(end)

  ref = db.reference('test')
  # ref = db.reference('project')
  # print(ref.get())
  snapshot = ref.order_by_child('timestamp').start_at(beginTimestamp).end_at(endTimestamp).get()
  # print(snapshot)
  dict1 = {'timestamp':[],'temp':[],'humid':[],'light':[]}
  # dict1 = {'timestamp':[],'temp':[],'humid':[]}
  for key in snapshot:
    dict1['timestamp'].append(snapshot[key]['timestamp'])
    dict1['temp'].append(snapshot[key]['temp'])
    dict1['humid'].append(snapshot[key]['humid'])
    dict1['light'].append(snapshot[key]['light'])
  df = pd.DataFrame(dict1)
  print(df)
  return df


# prepare Dash runtime
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = JupyterDash(__name__, external_stylesheets=external_stylesheets)
server = app.server
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# สร้างข้อมูล
df = download_data(2021, 9, 7, 7, 1, 2021, 9, 7, 7, 10)


# create graph component
fig = px.line(df['timestamp'], x=len(df['timestamp']), y= df['temp'])

# create table
def generate_table(df, rows):
  head = html.Thead(html.Tr([html.Th(col) for col in df.columns]))
  body = html.Tbody([
            html.Tr([
                html.Td(df.iloc[i][col]) for col in df.columns
            ]) for i in range(min(len(df), rows))
        ])
  table = html.Table([head, body])
  return table

app.layout = html.Div(children=[
  html.H1(children='Hello Dash'),
  html.H4(children='Start Date'),
  dcc.Dropdown(
    id='begin_day',
    options=[
        {'label': '1', 'value': '1'},
        {'label': '2', 'value': '2'},
        {'label': '3', 'value': '3'},
        {'label': '4', 'value': '4'},
        {'label': '5', 'value': '5'},
        {'label': '6', 'value': '6'},
        {'label': '7', 'value': '6'},
        {'label': '8', 'value': '8'},
        {'label': '9', 'value': '9'},
        {'label': '10', 'value': '10'},
        {'label': '11', 'value': '11'},
        {'label': '12', 'value': '12'},
        {'label': '13', 'value': '13'},
        {'label': '14', 'value': '14'},
        {'label': '15', 'value': '15'},
        {'label': '16', 'value': '16'},
        {'label': '17', 'value': '17'},
        {'label': '18', 'value': '18'},
        {'label': '19', 'value': '19'},
        {'label': '20', 'value': '20'},
        {'label': '21', 'value': '21'},
        {'label': '22', 'value': '22'},
        {'label': '23', 'value': '23'},
        {'label': '24', 'value': '24'},
        {'label': '25', 'value': '25'},
        {'label': '26', 'value': '26'},
        {'label': '27', 'value': '27'},
        {'label': '28', 'value': '28'},
        {'label': '29', 'value': '29'},
        {'label': '30', 'value': '30'},
        {'label': '31', 'value': '31'},
    ],
    value = datetime.today().strftime('%d'),
    searchable=False
  ),
  dcc.Dropdown(
    id='begin_month',
    options=[
        {'label': 'ม.ค.', 'value': '1'},
        {'label': 'ก.พ.', 'value': '2'},
        {'label': 'มี.ค.', 'value': '3'},
        {'label': 'เม.ษ.', 'value': '4'},
        {'label': 'พ.ค.', 'value': '5'},
        {'label': 'มิ.ย.', 'value': '6'},
        {'label': 'ก.ค.', 'value': '7'},
        {'label': 'ส.ค.', 'value': '8'},
        {'label': 'ก.ย.', 'value': '9'},
        {'label': 'ต.ค.', 'value': '10'},
        {'label': 'พ.ย.', 'value': '11'},
        {'label': 'ธ.ค.', 'value': '12'},
    ],
    value = datetime.today().strftime('%m'),
    searchable=False
  ),
  dcc.Dropdown(
    id='begin_year',
    options=[
        {'label': '2564', 'value': '2021'},
        {'label': '2563', 'value': '2020'},
        {'label': '2564', 'value': '2019'},
        {'label': '2561', 'value': '2018'},
        {'label': '2560', 'value': '2017'},
    ],
    value = datetime.today().strftime('%Y'),
    searchable=False
  ),
  dcc.Dropdown(
    id='begin_hr',
    options=[
       {'label': '00', 'value': '00'},
        {'label': '01', 'value': '01'},
        {'label': '02', 'value': '02'},
        {'label': '03', 'value': '03'},
        {'label': '04', 'value': '04'},
        {'label': '05', 'value': '05'},
        {'label': '06', 'value': '06'},
        {'label': '07', 'value': '07'},
        {'label': '08', 'value': '08'},
        {'label': '09', 'value': '09'},
        {'label': '10', 'value': '10'},
        {'label': '11', 'value': '11'},
        {'label': '12', 'value': '12'},
        {'label': '13', 'value': '13'},
        {'label': '14', 'value': '14'},
        {'label': '15', 'value': '15'},
        {'label': '16', 'value': '16'},
        {'label': '17', 'value': '17'},
        {'label': '18', 'value': '18'},
        {'label': '19', 'value': '19'},
        {'label': '20', 'value': '20'},
        {'label': '21', 'value': '21'},
        {'label': '22', 'value': '22'},
        {'label': '23', 'value': '23'},
    ],
    value = datetime.today().strftime('%Y'),
    searchable=False
  ),
  dcc.Dropdown(
    id='begin_min',
    options=[
        {'label': '00', 'value': '00'},
        {'label': '01', 'value': '01'},
        {'label': '02', 'value': '02'},
        {'label': '03', 'value': '03'},
        {'label': '04', 'value': '04'},
        {'label': '05', 'value': '05'},
        {'label': '06', 'value': '06'},
        {'label': '07', 'value': '07'},
        {'label': '08', 'value': '08'},
        {'label': '09', 'value': '09'},
        {'label': '10', 'value': '10'},
        {'label': '11', 'value': '11'},
        {'label': '12', 'value': '12'},
        {'label': '13', 'value': '13'},
        {'label': '14', 'value': '14'},
        {'label': '15', 'value': '15'},
        {'label': '16', 'value': '16'},
        {'label': '17', 'value': '17'},
        {'label': '18', 'value': '18'},
        {'label': '19', 'value': '19'},
        {'label': '20', 'value': '20'},
        {'label': '21', 'value': '21'},
        {'label': '22', 'value': '22'},
        {'label': '23', 'value': '23'},
        {'label': '24', 'value': '24'},
        {'label': '25', 'value': '25'},
        {'label': '26', 'value': '26'},
        {'label': '27', 'value': '27'},
        {'label': '28', 'value': '28'},
        {'label': '29', 'value': '29'},
        {'label': '30', 'value': '30'},
        {'label': '31', 'value': '31'},
        {'label': '32', 'value': '32'},
        {'label': '33', 'value': '33'},
        {'label': '34', 'value': '34'},
        {'label': '35', 'value': '35'},
        {'label': '36', 'value': '36'},
        {'label': '37', 'value': '37'},
        {'label': '38', 'value': '38'},
        {'label': '39', 'value': '39'},
        {'label': '40', 'value': '40'},
        {'label': '41', 'value': '41'},
        {'label': '42', 'value': '42'},
        {'label': '43', 'value': '43'},
        {'label': '44', 'value': '44'},
        {'label': '45', 'value': '45'},
        {'label': '46', 'value': '46'},
        {'label': '47', 'value': '47'},
        {'label': '48', 'value': '48'},
        {'label': '49', 'value': '49'},
        {'label': '50', 'value': '50'},
        {'label': '51', 'value': '51'},
        {'label': '52', 'value': '52'},
        {'label': '53', 'value': '53'},
        {'label': '54', 'value': '54'},
        {'label': '55', 'value': '55'},
        {'label': '56', 'value': '56'},
        {'label': '57', 'value': '57'},
        {'label': '58', 'value': '58'},
        {'label': '59', 'value': '59'},
    ],
    value = datetime.today().strftime('%M'),
    searchable=False
  ),

  html.H4(children='End Date'),
  dcc.Dropdown(
    id='end_day',
    options=[
        {'label': '1', 'value': '1'},
        {'label': '2', 'value': '2'},
        {'label': '3', 'value': '3'},
        {'label': '4', 'value': '4'},
        {'label': '5', 'value': '5'},
        {'label': '6', 'value': '6'},
        {'label': '7', 'value': '6'},
        {'label': '8', 'value': '8'},
        {'label': '9', 'value': '9'},
        {'label': '10', 'value': '10'},
        {'label': '11', 'value': '11'},
        {'label': '12', 'value': '12'},
        {'label': '13', 'value': '13'},
        {'label': '14', 'value': '14'},
        {'label': '15', 'value': '15'},
        {'label': '16', 'value': '16'},
        {'label': '17', 'value': '17'},
        {'label': '18', 'value': '18'},
        {'label': '19', 'value': '19'},
        {'label': '20', 'value': '20'},
        {'label': '21', 'value': '21'},
        {'label': '22', 'value': '22'},
        {'label': '23', 'value': '23'},
        {'label': '24', 'value': '24'},
        {'label': '25', 'value': '25'},
        {'label': '26', 'value': '26'},
        {'label': '27', 'value': '27'},
        {'label': '28', 'value': '28'},
        {'label': '29', 'value': '29'},
        {'label': '30', 'value': '30'},
        {'label': '31', 'value': '31'},
    ],
    value = datetime.today().strftime('%d'),
    searchable=False
  ),
  dcc.Dropdown(
    id='end_month',
    options=[
        {'label': 'ม.ค.', 'value': '1'},
        {'label': 'ก.พ.', 'value': '2'},
        {'label': 'มี.ค.', 'value': '3'},
        {'label': 'เม.ษ.', 'value': '4'},
        {'label': 'พ.ค.', 'value': '5'},
        {'label': 'มิ.ย.', 'value': '6'},
        {'label': 'ก.ค.', 'value': '7'},
        {'label': 'ส.ค.', 'value': '8'},
        {'label': 'ก.ย.', 'value': '9'},
        {'label': 'ต.ค.', 'value': '10'},
        {'label': 'พ.ย.', 'value': '11'},
        {'label': 'ธ.ค.', 'value': '12'},
    ],
    value = datetime.today().strftime('%m'),
    searchable=False
  ),
  dcc.Dropdown(
    id='end_year',
    options=[
        {'label': '2564', 'value': '2021'},
        {'label': '2563', 'value': '2020'},
        {'label': '2564', 'value': '2019'},
        {'label': '2561', 'value': '2018'},
        {'label': '2560', 'value': '2017'},
    ],
    value = datetime.today().strftime('%Y'),
    searchable=False
  ),
  dcc.Dropdown(
    id='end_hr',
    options=[
       {'label': '00', 'value': '00'},
        {'label': '01', 'value': '01'},
        {'label': '02', 'value': '02'},
        {'label': '03', 'value': '03'},
        {'label': '04', 'value': '04'},
        {'label': '05', 'value': '05'},
        {'label': '06', 'value': '06'},
        {'label': '07', 'value': '07'},
        {'label': '08', 'value': '08'},
        {'label': '09', 'value': '09'},
        {'label': '10', 'value': '10'},
        {'label': '11', 'value': '11'},
        {'label': '12', 'value': '12'},
        {'label': '13', 'value': '13'},
        {'label': '14', 'value': '14'},
        {'label': '15', 'value': '15'},
        {'label': '16', 'value': '16'},
        {'label': '17', 'value': '17'},
        {'label': '18', 'value': '18'},
        {'label': '19', 'value': '19'},
        {'label': '20', 'value': '20'},
        {'label': '21', 'value': '21'},
        {'label': '22', 'value': '22'},
        {'label': '23', 'value': '23'},
    ],
    value = datetime.today().strftime('%Y'),
    searchable=False
  ),
  dcc.Dropdown(
    id='end_min',
    options=[
        {'label': '00', 'value': '00'},
        {'label': '01', 'value': '01'},
        {'label': '02', 'value': '02'},
        {'label': '03', 'value': '03'},
        {'label': '04', 'value': '04'},
        {'label': '05', 'value': '05'},
        {'label': '06', 'value': '06'},
        {'label': '07', 'value': '07'},
        {'label': '08', 'value': '08'},
        {'label': '09', 'value': '09'},
        {'label': '10', 'value': '10'},
        {'label': '11', 'value': '11'},
        {'label': '12', 'value': '12'},
        {'label': '13', 'value': '13'},
        {'label': '14', 'value': '14'},
        {'label': '15', 'value': '15'},
        {'label': '16', 'value': '16'},
        {'label': '17', 'value': '17'},
        {'label': '18', 'value': '18'},
        {'label': '19', 'value': '19'},
        {'label': '20', 'value': '20'},
        {'label': '21', 'value': '21'},
        {'label': '22', 'value': '22'},
        {'label': '23', 'value': '23'},
        {'label': '24', 'value': '24'},
        {'label': '25', 'value': '25'},
        {'label': '26', 'value': '26'},
        {'label': '27', 'value': '27'},
        {'label': '28', 'value': '28'},
        {'label': '29', 'value': '29'},
        {'label': '30', 'value': '30'},
        {'label': '31', 'value': '31'},
        {'label': '32', 'value': '32'},
        {'label': '33', 'value': '33'},
        {'label': '34', 'value': '34'},
        {'label': '35', 'value': '35'},
        {'label': '36', 'value': '36'},
        {'label': '37', 'value': '37'},
        {'label': '38', 'value': '38'},
        {'label': '39', 'value': '39'},
        {'label': '40', 'value': '40'},
        {'label': '41', 'value': '41'},
        {'label': '42', 'value': '42'},
        {'label': '43', 'value': '43'},
        {'label': '44', 'value': '44'},
        {'label': '45', 'value': '45'},
        {'label': '46', 'value': '46'},
        {'label': '47', 'value': '47'},
        {'label': '48', 'value': '48'},
        {'label': '49', 'value': '49'},
        {'label': '50', 'value': '50'},
        {'label': '51', 'value': '51'},
        {'label': '52', 'value': '52'},
        {'label': '53', 'value': '53'},
        {'label': '54', 'value': '54'},
        {'label': '55', 'value': '55'},
        {'label': '56', 'value': '56'},
        {'label': '57', 'value': '57'},
        {'label': '58', 'value': '58'},
        {'label': '59', 'value': '59'},
    ],
    value = datetime.today().strftime('%M'),
    searchable=False
  ),


  
  dcc.Dropdown(
    id='daytype',
    options=[
        {'label': 'temp', 'value': 'temp'},
        {'label': 'light', 'value': 'light'},
        {'label': 'humid', 'value': 'humid'}
    ],
        value='temp',
    searchable=False
  ),

  html.Div(
      children='Demo line plot.',
      style={'textAlign': 'center', 'color': '#23A223'}
  ),
  dcc.Graph(
      id='graph',
      figure=fig
  ),
  html.Div(
      children='Demo table.',
      style={'textAlign': 'left', 'color': '#2323A2'}
  ),
  html.Div(id='my-output'),
  generate_table(df, 4)
])

@app.callback(
    Output('graph','figure'),
    Input(component_id='begin_year', component_property='value'),
    Input(component_id='begin_month', component_property='value'),
    Input(component_id='begin_day', component_property='value'),
    Input(component_id='begin_hr', component_property='value'),
    Input(component_id='begin_min', component_property='value'),

    Input(component_id='end_year', component_property='value'),
    Input(component_id='end_month', component_property='value'),
    Input(component_id='end_day', component_property='value'),
    Input(component_id='end_hr', component_property='value'),
    Input(component_id='end_min', component_property='value'),

    Input(component_id='daytype', component_property='value')

)
def update_figure(begin_year, begin_month, begin_day, begin_hr, begin_min, end_year, end_month, end_day, end_hr, end_min, daytype):
    # ctx = dash.callback_context
    # print(ctx)
    print('hello')
    df = download_data(begin_year, begin_month, begin_day, begin_hr, begin_min, end_year, end_month, end_day, end_hr, end_min)
 
    # create graph component
    fig = px.line(df['timestamp'], x=len(df['timestamp']), y=df[daytype])

    return fig
  
if __name__ == '__main__':
  
  app.run_server(debug=True)
