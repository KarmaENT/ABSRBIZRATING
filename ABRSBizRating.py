import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import random

# Initialize Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
server = app.server

# Default weights for factors
weights = {
    "Potential Profitability": 0.3,
    "Market Growth": 0.2,
    "Market Saturation": 0.2,
    "Scalability": 0.15,
    "Ease of Entry": 0.15,
}

# Function to generate scores from business idea (dummy implementation)
def generate_scores_from_idea(idea):
    return {factor: random.randint(40, 100) for factor in weights.keys()}

# Function to calculate ABRS score
def calculate_abrs_score(scores):
    weighted_scores = [score * weights[factor] for factor, score in scores.items()]
    return sum(weighted_scores)

# Function to generate Text Summary
def generate_text_summary(scores, abrs_score):
    high_factors = [factor for factor, score in scores.items() if score > 75]
    low_factors = [factor for factor, score in scores.items() if score < 50]

    summary = f"The business idea scores {abrs_score:.2f}/100, excelling in {', '.join(high_factors)}."
    if low_factors:
        summary += f" However, it faces challenges in {', '.join(low_factors)}."
    summary += " Recommendations include focusing on differentiation strategies and reducing entry barriers."

    return summary

# Layout Setup
app.layout = dbc.Container(
    [
        html.H1("ABSR: Advanced Business Scoring and Rating System", className="mt-4 text-center"),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Textarea(
                        id="business-idea-input",
                        placeholder="Enter your business idea here...",
                        style={"width": "100%", "height": 150},
                        className="mb-3"
                    ),
                    width=12
                ),
                dbc.Col(
                    dbc.Button("Analyze", id="analyze-button", color="primary", className="mt-3 w-100"),
                    width=12
                ),
            ]
        ),
        html.Div(id="abrs-score-output", className="mt-4 text-primary", style={"fontSize": "24px"}),

        # Interactive Graph Section
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id="overall-abrs-score", className="mt-4"),
                    width=6
                ),
                dbc.Col(
                    dcc.Graph(id="individual-factor-scores", className="mt-4"),
                    width=6
                ),
            ]
        ),

        # Trend Analysis and Risk-Reward Matrix
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id="trend-analysis", className="mt-4"),
                    width=6
                ),
                dbc.Col(
                    dcc.Graph(id="risk-reward-matrix", className="mt-4"),
                    width=6
                ),
            ]
        ),

        # Text Summary
        html.Div(id="text-summary-output", className="text-secondary mt-4", style={"fontSize": "18px"}),

        # Download Data Button
        dbc.Button("Download Data (CSV)", id="download-button", color="info", className="mt-3"),
        dcc.Download(id="download-datafile"),
    ],
    fluid=True,
    className="p-4"
)

# Callback to analyze and generate output
@app.callback(
    [
        Output("abrs-score-output", "children"),
        Output("overall-abrs-score", "figure"),
        Output("individual-factor-scores", "figure"),
        Output("trend-analysis", "figure"),
        Output("risk-reward-matrix", "figure"),
        Output("text-summary-output", "children"),
    ],
    [Input("analyze-button", "n_clicks")],
    [State("business-idea-input", "value")],
)
def analyze_business_idea(n_clicks, idea):
    if not idea:
        return "Please enter a business idea to analyze.", {}, {}, {}, {}, ""

    # Generate scores and calculate ABRS score
    scores = generate_scores_from_idea(idea)
    abrs_score = calculate_abrs_score(scores)

    # Generate text summary
    text_summary = generate_text_summary(scores, abrs_score)

    # Create visualizations

    # 1. Overall ABRS Score as a Gauge (Speedometer style)
    abrs_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=abrs_score,
        title={'text': "Overall ABRS Score"},
        gauge={'axis': {'range': [None, 100]},
               'steps': [{'range': [0, 50], 'color': "red"},
                         {'range': [50, 75], 'color': "yellow"},
                         {'range': [75, 100], 'color': "green"}]},
        domain={'x': [0, 1], 'y': [0, 1]},
    ))

    # 2. Individual Factor Scores as Bar Chart
    df = pd.DataFrame(
        {
            "Factor": list(scores.keys()),
            "Score": list(scores.values()),
            "Weight": [weights[factor] * 100 for factor in scores],
        }
    )

    factor_scores_chart = go.Figure(data=[
        go.Bar(
            x=df['Factor'],
            y=df['Score'],
            text=df['Score'],
            textposition='auto',
            marker=dict(color=df['Score'], colorscale='Blues', line=dict(width=1, color='black')),
            name='Scores'
        ),
        go.Scatter(
            x=df['Factor'],
            y=df['Weight'],
            mode='lines+markers',
            name='Weights',
            line=dict(color='rgba(255, 0, 0, 0.6)', width=2)
        )
    ])
    factor_scores_chart.update_layout(
        title="Business Idea Factors with Weights",
        xaxis_title="Factors",
        yaxis_title="Scores",
        template="plotly_dark",
        showlegend=True,
        margin=dict(l=20, r=20, t=40, b=40),
        height=400
    )

    # 3. Trend Analysis (Simulated Line Graph for the idea's trend)
    trend_x = [1, 2, 3, 4, 5]
    trend_y = [abrs_score + random.randint(-10, 10) for _ in trend_x]  # Simulated random trend data
    trend_chart = go.Figure(data=[go.Scatter(x=trend_x, y=trend_y, mode='lines+markers', name='Trend')])
    trend_chart.update_layout(title="Trend Analysis", template="plotly_dark", height=400)

    # 4. Risk vs. Reward Matrix (Scatter plot based on scores and weights)
    risk = [score * 0.5 for score in scores.values()]  # Simulate risk based on score
    reward = [score * 0.8 for score in scores.values()]  # Simulate reward based on score
    risk_reward_chart = go.Figure(data=[go.Scatter(
        x=risk, y=reward, mode='markers+text',
        text=list(scores.keys()), textposition='top center',
        marker=dict(size=12, color='rgb(204, 204, 255)', line=dict(width=1))
    )])
    risk_reward_chart.update_layout(title="Risk vs. Reward Matrix", xaxis_title="Risk", yaxis_title="Reward", template="plotly_dark", height=400)

    return f"Calculated ABRS Score: {abrs_score:.2f}/100", abrs_gauge, factor_scores_chart, trend_chart, risk_reward_chart, text_summary

# Callback for data export
@app.callback(
    Output("download-datafile", "data"),
    [Input("download-button", "n_clicks")],
    [State("business-idea-input", "value")],
)
def download_raw_data(n_clicks, idea):
    if not idea:
        return None

    # Generate scores
    scores = generate_scores_from_idea(idea)
    abrs_score = calculate_abrs_score(scores)

    # Prepare data for download
    df = pd.DataFrame(
        {
            "Factor": list(scores.keys()),
            "Score": list(scores.values()),
            "Weight": [weights[factor] * 100 for factor in scores],
        }
    )
    df["ABRS Score"] = abrs_score

    return dcc.send_data_frame(df.to_csv, "business_analysis.csv")

if __name__ == "__main__":
    app.run_server(debug=True)
