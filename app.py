import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px

# ===== LOAD DATA =====
df = pd.read_csv("data.csv")
df["date"] = pd.to_datetime(df["date"])

print("Data Loaded Successfully")
print(df.head())

# ===== CREATE WEIGHT LINE CHART =====
weight_fig = px.line(
    df, x="date", y="weight", title="Weight Progress Over Time", markers=True
)

weight_fig.update_layout(
    template="plotly_dark", xaxis_title="Date", yaxis_title="Weight (kg)"
)

# ===== CREATE BODY FAT LINE CHART =====
bodyfat_fig = px.line(
    df, x="date", y="body_fat", title="Body Fat Percentage Over Time", markers=True
)

bodyfat_fig.update_layout(
    template="plotly_dark", xaxis_title="Date", yaxis_title="Body Fat (%)"
)

app = dash.Dash(__name__)
app.title = "Fitness Dashboard"

app.layout = html.Div(
    [
        # ===== HEADER =====
        html.Div(
            [
                html.H1("💪 Fitness & Body Tracking Dashboard"),
                html.P("Track your health and workout progress"),
            ],
            style={
                "textAlign": "center",
                "padding": "20px",
                "backgroundColor": "#111",
                "color": "white",
            },
        ),
        # ===== KPI SECTION =====
        html.Div(
            [
                html.Div("Weight KPI"),
                html.Div("Body Fat KPI"),
                html.Div("Workout KPI"),
            ],
            style={
                "display": "flex",
                "justifyContent": "space-around",
                "padding": "20px",
            },
        ),
        # ===== GRAPH SECTION =====
        html.Div(
            [
                dcc.Graph(figure=weight_fig),
                dcc.Graph(figure=bodyfat_fig),
                html.Div("Graph 3 Placeholder"),
            ],
            style={"padding": "20px"},
        ),
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
