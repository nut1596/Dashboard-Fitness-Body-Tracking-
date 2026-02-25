import dash
from dash import html

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
                html.Div("Weight KPI", className="kpi-card"),
                html.Div("Body Fat KPI", className="kpi-card"),
                html.Div("Workout KPI", className="kpi-card"),
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
