import dash
from dash import html, dcc
from dash import Input, Output
import pandas as pd
import plotly.express as px

# ===== LOAD DATA =====
df = pd.read_csv("data.csv")
df["date"] = pd.to_datetime(df["date"])

print("Data Loaded Successfully")
print(df.head())


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
        # ===== KPI SECTION =====
        html.Div(
            [
                html.Div(id="kpi-weight", className="kpi-card"),
                html.Div(id="kpi-bodyfat", className="kpi-card"),
                html.Div(id="kpi-workout", className="kpi-card"),
            ],
            className="kpi-container",
        ),
        # ===== DATE RANGE FILTER =====
        html.Div(
            [
                html.Label("Select Date Range:"),
                dcc.DatePickerRange(
                    id="date-picker",
                    min_date_allowed=df["date"].min(),
                    max_date_allowed=df["date"].max(),
                    start_date=df["date"].min(),
                    end_date=df["date"].max(),
                    display_format="YYYY-MM-DD",
                ),
            ],
            style={"textAlign": "center", "padding": "20px"},
        ),
        # ===== WORKOUT TYPE FILTER =====
        html.Div(
            [
                html.Label("Select Workout Type:"),
                dcc.Dropdown(
                    id="workout-filter",
                    options=[
                        {"label": "All", "value": "all"},
                        {"label": "Cardio Only", "value": "cardio"},
                        {"label": "Weight Training Only", "value": "weight"},
                    ],
                    value="all",
                    clearable=False,
                    style={"width": "300px", "margin": "0 auto"},
                ),
            ],
            style={"textAlign": "center", "padding": "20px"},
        ),
        # ===== GRAPH SECTION =====
        html.Div(
            [
                dcc.Graph(id="weight-chart"),
                dcc.Graph(id="bodyfat-chart"),
                dcc.Graph(id="workout-chart"),
            ],
            style={"padding": "20px"},
        ),
    ]
)


# ===== CALLBACK FOR DATE FILTER =====
@app.callback(
    Output("weight-chart", "figure"),
    Output("bodyfat-chart", "figure"),
    Output("workout-chart", "figure"),
    Output("kpi-weight", "children"),
    Output("kpi-bodyfat", "children"),
    Output("kpi-workout", "children"),
    Input("date-picker", "start_date"),
    Input("date-picker", "end_date"),
    Input("workout-filter", "value"),
)
def update_charts(start_date, end_date, workout_type):

    # Filter dataframe
    filtered_df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]

    # ===== FILTER BY WORKOUT TYPE =====
    if workout_type == "cardio":
        filtered_df = filtered_df[filtered_df["cardio_min"] > 0]
    elif workout_type == "weight":
        filtered_df = filtered_df[filtered_df["weight_min"] > 0]

    # ===== Weight Chart =====
    weight_fig = px.line(
        filtered_df,
        x="date",
        y="weight",
        title="Weight Progress Over Time",
        markers=True,
    )
    weight_fig.update_layout(template="plotly_dark")

    # ===== Body Fat Chart =====
    bodyfat_fig = px.line(
        filtered_df,
        x="date",
        y="body_fat",
        title="Body Fat Percentage Over Time",
        markers=True,
    )
    bodyfat_fig.update_layout(template="plotly_dark")

    # ===== Workout Pie Chart =====
    total_cardio = filtered_df["cardio_min"].sum()
    total_weight_training = filtered_df["weight_min"].sum()

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

    # ===== KPI CALCULATIONS =====
    if not filtered_df.empty:
        latest_weight = filtered_df.iloc[-1]["weight"]
        latest_bodyfat = filtered_df.iloc[-1]["body_fat"]
        total_workout = (
            filtered_df["cardio_min"].sum() + filtered_df["weight_min"].sum()
        )
    else:
        latest_weight = 0
        latest_bodyfat = 0
        total_workout = 0

    kpi_weight_text = f"🏋️ Latest Weight: {latest_weight} kg"
    kpi_bodyfat_text = f"🔥 Latest Body Fat: {latest_bodyfat}%"
    kpi_workout_text = f"⏱ Total Workout: {total_workout} mins"

    return (
        weight_fig,
        bodyfat_fig,
        workout_fig,
        kpi_weight_text,
        kpi_bodyfat_text,
        kpi_workout_text,
    )


if __name__ == "__main__":
    app.run(debug=True)
