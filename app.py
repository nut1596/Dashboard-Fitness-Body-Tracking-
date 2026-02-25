import dash
from dash import html
import pandas as pd

# ===== LOAD DATA =====
df = pd.read_csv("data.csv")
df["date"] = pd.to_datetime(df["date"])

print("Data Loaded Successfully")
print(df.head())

app = dash.Dash(__name__)
app.title = "Fitness Dashboard"

app.layout = html.Div(
    [
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
        html.Div(
            [
                html.Div("Graph 1 Placeholder"),
                html.Div("Graph 2 Placeholder"),
                html.Div("Graph 3 Placeholder"),
            ],
            style={"padding": "20px"},
        ),
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
