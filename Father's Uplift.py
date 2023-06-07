import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd



# incorporate data into app

#read csv
sample_data = pd.read_csv('HC_Sample.csv')

#rename cols
sample_data.columns = ['ID', 'referral', 'facilitator',
                       'HighestGrade', 'Gender', 'BirthDate',
                       'Sp,His,Lat?', 'PrimaryEth', 'FirstSubstance',
                       'numberODs', 'SecondarySubstance', 'PrimarySubstance',
                       'SecondSubstance', 'stateAgency', 'referralSource',
                       'ThirdSubstance', 'GamblingStart', 'Tertiary Substance',
                       'ArrestedInMonth', 'daysAfterInitialContact', 'AddressType',
                       'ClinicianInitials', 'PhoneifIncarc', 'everOD', 'LastNeedle',
                       'IsCitizen', 'SSN', 'SelectAddress', 'PhoneNumber', 'City',
                       'State', 'ZipCode', 'AdminRoute', 'UseFreq', 'LastTimeUsing',
                       'Gambles', 'SmokesCigs', 'MultSubst', 'PriorTreatment', 'AgeFirstUse',
                       'Alcohol', 'Cocaine', 'Crack', 'Marijuana', 'Heroine', 'PrescOpiates',
                       'Opiates', 'PCP', 'otherHallucinogen', 'Meth', 'otherAmphetamines',
                       'otherStimulants', 'Benz', 'otherTranq', 'Barbituates', 'otherSedatives',
                       'inhalants', 'overCounter', 'clubDrugs', 'Other', 'Nic/Tobacco', 'Gambling',
                       'K2spiceorSynth', 'living', 'InsuranceStatus', 'Comments', 'ifnorace',
                       'Race', 'Language', 'AdultsinHouse', 'ChildrenLiving', 'Income', 'MaritalStatus',
                       'OwnaRoom', 'ChronicHomeless', 'ZipofLast', 'WhereSleep', 'Sexuality', 'attendance',
                       'ClientType', 'HasKids', 'ChildrenUnder6', 'Children6-18', 'ChildrenOver18', 'IsPrimaryCare',
                       'Employment', 'DaysWorkedinMonth', 'UsuallyLive', 'LiveWith', 'MobilityAid', 'visionImpairment',
                       'hearingImpairment', 'SelfCareImpairment', 'DevelopmentalDisability', 'PriorMentalTreat',
                       'hadPrescription', 'MedAssist', 'Methadone', 'Subox', 'SuboxForAlc', 'StateAgentService',
                       'packsSmoked', 'StoppingSmoke', 'AgeofFirst', 'NumArrests', 'NumPriorConvict', 'TimeServed',
                       'OnProbation', 'OnParole', 'toGetHealthcare', 'toGetJob', 'toLearnSkills', 'GettingPlaces',
                       'ParentingTime', 'PayingChildSupport', 'toBuyFood', 'DCF']

#replace Unknown with N/A to make it more understandable
pattern = r"Unknown.*"
for col in sample_data.columns:
    if type(sample_data[col][0]) == str:
        sample_data[col] = sample_data[col].str.replace(pattern,"N/A", regex = True)

# functions to make binary 1 or 0 variable for whether they have kids or whether they
# took a drug
def has_kid(string):
    if string == 'Yes - 1':
        return 1
    else:
        return 0

def taken_drug(string):
    if string == 'No, I have not used':
        return 0
    else:
        return 1

# map creates new column in the dataframe with the 1 or 0 variable
sample_data['binHasKids'] = sample_data['HasKids'].map(has_kid)

# same thing for the drug variables
drugs = ['Marijuana', 'Alcohol', 'Cocaine', 'Meth', 'Heroine', 'Nic/Tobacco',
         'Other']
for drug in drugs:
    new_col = 'bin'+drug
    sample_data[new_col] = sample_data[drug].map(taken_drug)

# new child categories and drug category names
child_cats = ['binHasKids','ChildrenUnder6', 'ChildrenOver18',
                          'Children6-18']
binDrugs = ['binMarijuana', 'binAlcohol', 'binCocaine', 'binMeth', 'binHeroine', 'binNic/Tobacco',
         'binOther']

# averages we'll use for the y-axis of the child and drug plots
drugs_props = []
for cat in binDrugs:
    drugs_props.append(sample_data[cat].mean())

child_catmeans = []
for c in child_cats:
    child_catmeans.append(sample_data[c].mean())

# child category names we'll use for the plot x-axis
children_axis = ['Proportion of Patients with Kids','Avg # of Children Under 6', 'Avg # Children Over 18',
                          'Avg # of Children 6-18']



# Build your components
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN], meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])

server = app.server
app.layout = dbc.Container([
    dbc.Row(


        dbc.Col(html.H1("Fathers' UpLift Dashboard",
                        className='text-center text-primary mb-4'),
                width=10)
    ),

    dbc.Row([

        dbc.Col([
            html.H2("PART ONE: PATIENT DEMOGRAPHICS", className="text-black-50 m-0 bg-light border"),
            html.Br(),
            html.P("Select Category:",
                       style={"textDecoration": "underline"}, className="text-warning p-0 bg-light border m-0 bg-light border"),
            dcc.Dropdown(id='my-dpd1', multi = False, options=['HighestGrade', 'ZipCode',
                                                              'Gender', 'ClientType',
                                                               'referral', 'Race',
                                                               'Substance Use', 'Children'],
                         value='ZipCode',  # initial value displayed when page first loads
                         clearable=False),
            dcc.Graph(id = 'barfig1', figure={})
        ], width={'size':11, 'offset':1},
           xs=12, sm=12, md=12, lg=11, xl=11
        ),
    ], justify='start'),

    dbc.Row([
            dbc.Col([
                html.H2("PART TWO: SERVICE OUTCOMES", className="text-black-50 m-0 bg-light border"),
                html.Br(),
                html.P("Select Category:",
                       style={"textDecoration": "underline"}, className="text-warning p-0 bg-light border m-0 bg-light border"),
                #dcc.Dropdown(id='my-dpdn3', multi=False, value='',
                             #options=[],
                             #clearable=False),
                #dcc.Graph(id='barfig3', figure={}),
            ], #width={'size':8, 'offset':1},
               #xs=12, sm=12, md=12, lg=8, xl=8
            ),
        ])

])

# Callback allows components to interact
@app.callback(
    Output('barfig1', component_property='figure'),
    Input('my-dpd1', component_property='value')
)
def update_graph(category):  # function arguments come from the component property of the Input
    if (category != 'Substance Use') & (category != 'Children'):
        cat_grouped = sample_data.groupby(category).size().to_frame().reset_index()

        cat_grouped1 = cat_grouped.rename(columns={0: 'Number of Patients'})
        #teams_cvg1 = teams_cvg[teams_cvg['defensiveTeam'].isin(teamnames)]

        catsbar1 = px.bar(
            data_frame=cat_grouped1,
            x=category,
            y="Number of Patients",
            opacity=0.9,  # set opacity of markers (from 0 to 1)
            orientation="v",  # 'v','h': orientation of the marks
            #barmode='group',
            template='seaborn')
        return catsbar1
    else:
        if category == 'Substance Use':


            catsbar2 = px.bar(

                x=drugs,
                y=drugs_props,
                opacity=0.9,  # set opacity of markers (from 0 to 1)
                orientation="v",  # 'v','h': orientation of the marks
                labels={
                    "x": "Substances",
                    "y": "Proportion of Patients Who've Used",

                },
                # barmode='group',
                template='seaborn')

            return catsbar2

        if category == 'Children':

            catsbar3 = px.bar(

                x=children_axis,
                y=child_catmeans,
                opacity=0.9,  # set opacity of markers (from 0 to 1)
                orientation="v",  # 'v','h': orientation of the marks
                labels={
                    "x": "",
                    "y": "",

                },
                # barmode='group',
                template='seaborn')

            return catsbar3


# Run app
if __name__=='__main__':
    app.run_server(port=8053)
