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

# ===== CREATE WORKOUT DISTRIBUTION PIE CHART =====
total_cardio = df["cardio_min"].sum()
total_weight_training = df["weight_min"].sum()

workout_data = pd.DataFrame(
    {
        "Workout Type": ["Cardio", "Weight Training"],
        "Total Minutes": [total_cardio, total_weight_training],
    }
)

workout_fig = px.pie(
    workout_data,
    names="Workout Type",
    values="Total Minutes",
    title="Workout Distribution",
)

workout_fig.update_layout(template="plotly_dark")

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
                dcc.Graph(figure=workout_fig),
            ],
            style={"padding": "20px"},
        ),
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
