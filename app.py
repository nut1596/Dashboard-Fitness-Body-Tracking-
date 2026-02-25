import dash
from dash import html, dcc
from dash import Input, Output
import pandas as pd
import plotly.express as px

# ===== LOAD DATA =====
df = pd.read_csv("data.csv")
df["date"] = pd.to_datetime(df["date"])

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
                html.Div(id="kpi-weight", className="kpi-card"),
                html.Div(id="kpi-bodyfat", className="kpi-card"),
                html.Div(id="kpi-workout", className="kpi-card"),
            ],
            className="kpi-container",
        ),
        # ===== DATE FILTER =====
        html.Div(
            [
                html.Label("Select Date Range:"),
                dcc.DatePickerRange(
                    id="date-picker",
                    min_date_allowed=pd.to_datetime("2025-01-01"),
                    max_date_allowed=pd.to_datetime("2027-12-31"),
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
        # ===== SUMMARY TYPE FILTER =====
        html.Div(
            [
                html.Label("Select Summary View:"),
                dcc.Dropdown(
                    id="summary-type",
                    options=[
                        {"label": "Weekly", "value": "W"},
                        {"label": "Monthly", "value": "M"},
                    ],
                    value="W",
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
                dcc.Graph(id="summary-chart"),
            ],
            style={"padding": "20px"},
        ),
    ]
)


# ===== CALLBACK =====
@app.callback(
    Output("weight-chart", "figure"),
    Output("bodyfat-chart", "figure"),
    Output("workout-chart", "figure"),
    Output("summary-chart", "figure"),
    Output("kpi-weight", "children"),
    Output("kpi-bodyfat", "children"),
    Output("kpi-workout", "children"),
    Input("date-picker", "start_date"),
    Input("date-picker", "end_date"),
    Input("workout-filter", "value"),
    Input("summary-type", "value"),
)
def update_charts(start_date, end_date, workout_type, summary_type):

    # 🔥 แปลง string เป็น datetime ก่อน
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # ===== FILTER BY DATE =====
    filtered_df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]

    # ===== FILTER BY WORKOUT TYPE =====
    if workout_type == "cardio":
        filtered_df = filtered_df[filtered_df["cardio_min"] > 0]
    elif workout_type == "weight":
        filtered_df = filtered_df[filtered_df["weight_min"] > 0]

    # ===== SUMMARY (WEEKLY / MONTHLY) =====
    if filtered_df.empty:
        summary_fig = px.bar(title="No Data Available")
        summary_fig.update_layout(template="plotly_dark")
    else:
        summary_df = filtered_df.copy()
        summary_df = summary_df.set_index("date")

        aggregated = summary_df.resample(summary_type).sum(numeric_only=True)

        if aggregated.empty:
            summary_fig = px.bar(title="No Aggregated Data")
            summary_fig.update_layout(template="plotly_dark")
        else:
            aggregated["total_workout"] = (
                aggregated["cardio_min"] + aggregated["weight_min"]
            )

            aggregated = aggregated.reset_index()

            summary_fig = px.bar(
                aggregated,
                x="date",
                y="total_workout",
                title=f"{'Weekly' if summary_type=='W' else 'Monthly'} Total Workout Minutes",
            )

            summary_fig.update_layout(template="plotly_dark")

    # ===== WEIGHT CHART WITH ROLLING AVERAGE =====
    if filtered_df.empty:
        weight_fig = px.line(title="No Weight Data Available")
        weight_fig.update_layout(template="plotly_dark")
    else:
        weight_df = filtered_df.copy().sort_values("date")

        # 🔥 Rolling average 3 จุด
        weight_df["rolling_avg"] = weight_df["weight"].rolling(window=3).mean()

        weight_fig = px.line(
            weight_df,
            x="date",
            y="weight",
            title="Weight Progress Over Time",
            markers=True,
        )

        # เพิ่มเส้น Rolling
        weight_fig.add_scatter(
            x=weight_df["date"],
            y=weight_df["rolling_avg"],
            mode="lines",
            name="3-Point Rolling Avg",
            line=dict(width=3),
        )

        weight_fig.update_layout(template="plotly_dark")

    # ===== BODY FAT CHART =====
    if filtered_df.empty:
        bodyfat_fig = px.line(title="No Body Fat Data Available")
        bodyfat_fig.update_layout(template="plotly_dark")
    else:
        bodyfat_fig = px.line(
            filtered_df,
            x="date",
            y="body_fat",
            title="Body Fat Percentage Over Time",
            markers=True,
        )
        bodyfat_fig.update_layout(template="plotly_dark")

    # ===== WORKOUT PIE =====
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

    # ===== KPI =====
    if not filtered_df.empty:
        latest_weight = filtered_df.iloc[-1]["weight"]
        latest_bodyfat = filtered_df.iloc[-1]["body_fat"]
        total_workout = total_cardio + total_weight_training

        # 🔥 คำนวณ Delta
        if len(filtered_df) > 1:
            previous_weight = filtered_df.iloc[-2]["weight"]
            delta = latest_weight - previous_weight
        else:
            delta = 0

        # เลือกสัญลักษณ์ + สี
        if delta < 0:
            arrow = "↓"
            color = "#00FF88"  # เขียว
        elif delta > 0:
            arrow = "↑"
            color = "#FF4C4C"  # แดง
        else:
            arrow = "→"
            color = "white"

        weight_kpi = html.Div(
            [
                html.Div(f"🏋️ {latest_weight} kg"),
                html.Div(
                    f"{arrow} {delta:.2f} kg from previous",
                    style={"color": color, "fontSize": "14px"},
                ),
            ]
        )

    else:
        latest_weight = 0
        latest_bodyfat = 0
        total_workout = 0
        weight_kpi = "🏋️ 0 kg"

    kpi_weight_text = weight_kpi
    kpi_bodyfat_text = f"🔥 Latest Body Fat: {latest_bodyfat}%"
    kpi_workout_text = f"⏱ Total Workout: {total_workout} mins"

    return (
        weight_fig,
        bodyfat_fig,
        workout_fig,
        summary_fig,
        kpi_weight_text,
        kpi_bodyfat_text,
        kpi_workout_text,
    )


if __name__ == "__main__":
    app.run(debug=True)
