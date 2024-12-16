from dash import html, dcc, Dash, callback, Input, Output, State
import plotly.express as px
from sklearn import datasets
import pandas as pd
import dash_bootstrap_components as dbc

############################ DATASET ###############################
def load_dataset():
    wine = datasets.load_wine()
    wine_df = pd.DataFrame(wine.data, columns=wine.feature_names)
    wine_df["WineType"] = [wine.target_names[typ] for typ in wine.target]
    return wine, wine_df

wine, wine_df = load_dataset()

######################## CHARTS ##################################
def create_histogram(col_name):
    fig = px.histogram(wine_df, x=col_name, color="WineType", nbins=50, height=400)
    fig.update_traces(marker={"line":{"width": 2, "color": "black"}})
    fig.update_layout(paper_bgcolor="#e5ecf6", margin={"t":0})
    return fig

def create_scatter_chart(x_axis, y_axis):
    fig = px.scatter(wine_df, x=x_axis, y=y_axis, color='WineType', height=400)
    fig.update_traces(marker={"size":12, "line":{"width": 2, "color": "black"}})
    fig.update_layout(paper_bgcolor="#e5ecf6", margin={"t":0})
    return fig

def create_pie_chart():
    wine_cnt = wine_df.groupby("WineType").count()[["alcohol"]]\
        .rename(columns={"alcohol": "Count"}).reset_index()
    fig = px.pie(wine_cnt, values=wine_cnt.Count, names=wine_cnt.WineType, hole=0.5, height=400)
    fig.update_traces(marker={"line":{"width": 2, "color": "black"}})
    fig.update_layout(paper_bgcolor="#e5ecf6", margin={"t":0})
    return fig

def create_bar_chart(col_name):
    fig = px.histogram(wine_df, x="WineType", y=col_name, color="WineType", histfunc="avg", height=400)
    fig.update_traces(marker={"line":{"width": 2, "color": "black"}})
    fig.update_layout(paper_bgcolor="#e5ecf6", margin={"t":0})
    return fig

####################### WIDGETS ##########################
hist_drop = dcc.Dropdown(id="hist_column", options=wine.feature_names, value="alcohol",
                          clearable=False, className="text-dark p-2")
x_axis = dcc.Dropdown(id="x_axis", options=wine.feature_names, value="alcohol",
                          clearable=False, className="text-dark p-2")
y_axis = dcc.Dropdown(id="y_axis", options=wine.feature_names, value="malic_acid",
                          clearable=False, className="text-dark p-2")
avg_drop = dcc.Dropdown(id="avg_drop", options=wine.feature_names, value="malic_acid",
                          clearable=False, className="text-dark p-2")

####################### LAYOUT #############################
external_css = ["https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css", ]
app = Dash(__name__, external_stylesheets=external_css)

sidebar = html.Div([
    html.Br(),
    html.H3("Sidebar", className="text-center fw-bold fs-2"),
    html.Br(),
    html.H3("Histogram Dropdown", className="fs-4"),
    hist_drop,
    html.Br(),
    html.H3("Scatter Chart Dropdowns", className="fs-4"),
    x_axis, y_axis,
    html.Br(),
    html.H3("Bar Chart Dropdown", className="fs-4"),
    avg_drop
    ], className="col-2 bg-dark text-white", style={"height": "100vh"}
)

modal_body = html.Div([
    html.Div([html.Img(src="assets/dev.jpg", width=250, className="rounded-circle mx-auto d-flex img-thumbnail")]),
    html.Br(),
    html.B("Intro: "), "Software Developer",
    html.Br(),html.Br(),
    html.B("About: "), "I am a passionate developer with a strong foundation in web, app and game development, backend systems, and blockchain technology. I specialize in creating efficient, scalable, and visually appealing applications using a wide range of tools and technologies.",
    html.Br(), html.Br(),
    "Proficient in modern JavaScript frameworks and libraries, including Bootstrap and Tailwind CSS for responsive design. TypeScript: Skilled in building scalable and maintainable codebases with TypeScript. MERN Stack: Comprehensive understanding of MongoDB, Express.js, React.js, and Node.js for full-stack application development. Experienced in building robust backend systems, REST APIs, and server-side applications. SQL Databases: Proficient in designing and managing relational databases such as PostgreSQL and MySQL, including query optimization and schema design.",
    html.Br(),html.Br(),
    html.B("Email: "), "karelh2207@gmail.com",
    html.Br(),html.Br(),
    html.Div([
        html.A([html.Img(src="assets/linkedin.png", className="rounded m-1")], href="https://www.linkedin.com/in/karel95/", target="_blank"),
        html.A([html.Img(src="assets/twitter.png", className="rounded m-1")], href="https://twitter.com/", target="_blank"),
        html.A([html.Img(src="assets/github.png", className="rounded m-1")], href="https://github.com/Karel95", target="_blank"),
    ])
])

main_content = html.Div([
    html.Br(),
    html.H2("Wine Dataset Analysis", className="text-center fw-bold fs-1"),
    html.Div([
        dcc.Graph(id="histogram", className="col-5"),
        dcc.Graph(id="scatter_chart", className="col-5")
        ], className="row"),
    html.Div([
        dcc.Graph(id="bar_chart", className="col-5"),
        dcc.Graph(id="heatmap", figure=create_pie_chart(), className="col-5"),
        ],className="row"),
    "Dashboard Designed By :  ", dbc.Button("Karel Hernandez", id="open", n_clicks=0),
    dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle("Karel Hernandez")),
                dbc.ModalBody([modal_body]),
                dbc.ModalFooter(dbc.Button("Close", id="close", className="ms-auto", n_clicks=0)),
            ],
            id="modal",
            is_open=False,
    ),
    ], className="col", style={"height": "100vh", "background-color": "#e5ecf6"}
)

app.layout = html.Div([
    html.Div([sidebar, main_content], className="row")
], className="container-fluid", style={"height": "100vh"})

######################## CALLBACKS #######################################
@callback(Output("histogram", "figure"), [Input("hist_column", "value"), ])
def update_histogram(hist_column):
    return create_histogram(hist_column)

@callback(Output("scatter_chart", "figure"), [Input("x_axis", "value"), Input("y_axis", "value"),])
def update_scatter(x_axis, y_axis):
    return create_scatter_chart(x_axis, y_axis)

@callback(Output("bar_chart", "figure"), [Input("avg_drop", "value"), ])
def update_bar(avg_drop):
    return create_bar_chart(avg_drop)

@app.callback(Output("modal", "is_open"), [Input("open", "n_clicks"), Input("close", "n_clicks")], [State("modal", "is_open")])
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

 ################################# RUN APP ##############################
if __name__ == "__main__":
    app.run()