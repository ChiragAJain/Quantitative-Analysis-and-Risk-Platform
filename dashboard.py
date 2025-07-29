import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from stock_analyzer import StockAnalyzer
import pandas as pd


analyzer = StockAnalyzer()


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Stock Market Analysis Dashboard"


app.index_string =
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <meta name="mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            /* Mobile-first responsive styles */
            @media (max-width: 768px) {
                .container-fluid { padding: 0.75rem !important; }
                .card { margin-bottom: 1.5rem !important; }
                .card-body { padding: 1rem !important; }
                h1 { font-size: 1.5rem !important; margin-bottom: 1.5rem !important; }
                h5 { font-size: 1rem !important; }
                h6 { font-size: 0.9rem !important; }
                .btn { font-size: 0.875rem !important; padding: 0.375rem 0.75rem !important; }
                .form-control, .form-select { font-size: 0.875rem !important; }
                /* Chart containers with proper spacing */
                .js-plotly-plot {
                    margin: 1rem 0 !important;
                    min-height: 400px !important;
                }
                /* Row spacing for mobile */
                .row { margin-bottom: 1.5rem !important; }
                /* Responsive text */
                p { font-size: 0.875rem !important; margin-bottom: 0.5rem !important; }
                /* Hide less critical elements on very small screens */
                @media (max-width: 480px) {
                    .d-none-xs { display: none !important; }
                    .js-plotly-plot { min-height: 350px !important; }
                }
            }
            /* Touch-friendly interactions */
            .dropdown-menu { font-size: 0.9rem; }
            .dropdown-item { padding: 0.5rem 1rem; }
            /* Plotly mobile optimizations */
            .modebar { display: none !important; }
            .plotly .modebar { display: none !important; }
            
            /* Mobile dashboard wrapper */
            .mobile-dashboard {
                min-height: 100vh;
                background-color:
            }
            
            @media (max-width: 768px) {
                .mobile-dashboard {
                    padding: 0;
                    background-color:
                }
                
                /* Better chart spacing on mobile */
                .js-plotly-plot .plotly {
                    margin: 1rem 0 2rem 0 !important;
                }
                
                /* Improve card spacing */
                .card + .card {
                    margin-top: 1.5rem !important;
                }
                
                /* Better row spacing */
                .container-fluid > .row {
                    margin-bottom: 2rem !important;
                }
                
                .container-fluid > .row:last-child {
                    margin-bottom: 1rem !important;
                }
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>



print("Initializing dashboard...")
if analyzer.fetch_stock_data(period='2y'):
    print("✓ Data loaded successfully!")
else:
    print("✗ Failed to load data")


app.layout = html.Div([
    dbc.Container([

    dbc.Row([
        dbc.Col([
            html.H1("📈 Stock Market Analysis",
                   className="text-center mb-3 mb-md-4",
                   style={'color': '#2c3e50', 'fontWeight': 'bold', 'fontSize': 'clamp(1.25rem, 4vw, 2rem)'})
        ])
    ], className="mb-2 mb-md-3"),
    

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Dashboard Controls", className="card-title mb-3"),
                    dbc.Row([
                        dbc.Col([
                            html.Label("Chart Type:", className="fw-bold mb-2"),
                            dcc.Dropdown(
                                id='chart-type-dropdown',
                                options=[
                                    {'label': 'Normalized Prices', 'value': 'normalized'},
                                    {'label': 'Actual Prices', 'value': 'actual'}
                                ],
                                value='normalized',
                                clearable=False,
                                style={'fontSize': '0.9rem'}
                            )
                        ], width=12, md=6, className="mb-3 mb-md-0"),
                        dbc.Col([
                            html.Label("Select Stocks:", className="fw-bold mb-2"),
                            dcc.Dropdown(
                                id='stock-selector',
                                options=[{'label': name, 'value': name}
                                        for name in analyzer.major_stocks.keys()],
                                value=list(analyzer.major_stocks.keys()),
                                multi=True,
                                style={'fontSize': '0.9rem'}
                            )
                        ], width=12, md=6)
                    ])
                ])
            ], className="mb-3 mb-md-4")
        ])
    ]),
    

    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='time-series-chart',
                config={
                    'displayModeBar': False,
                    'responsive': True,
                    'toImageButtonOptions': {'format': 'png', 'filename': 'stock_analysis'},
                    'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d']
                }
            )
        ], width=12)
    ], className="mb-4 mb-md-5"),
    

    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='correlation-heatmap',
                config={
                    'displayModeBar': False,
                    'responsive': True
                }
            )
        ], width=12, lg=6, className="mb-4 mb-lg-0"),
        dbc.Col([
            dcc.Graph(
                id='volatility-chart',
                config={
                    'displayModeBar': False,
                    'responsive': True
                }
            )
        ], width=12, lg=6)
    ], className="mb-4 mb-md-5"),
    

    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='performance-metrics-chart',
                config={
                    'displayModeBar': False,
                    'responsive': True
                }
            )
        ], width=12)
    ], className="mb-4 mb-md-5"),
    

    dbc.Row([
        dbc.Col([
            html.Div(id='portfolio-summary')
        ], width=12)
    ], className="mb-3 mb-md-4"),
    

    dbc.Row([
        dbc.Col([
            html.Div(id='summary-stats')
        ])
    ])
    
], fluid=True)
], className="mobile-dashboard")

@app.callback(
    Output('time-series-chart', 'figure'),
    [Input('chart-type-dropdown', 'value'),
     Input('stock-selector', 'value')]
)
def update_time_series(chart_type, selected_stocks):
    if not selected_stocks:
        return go.Figure().add_annotation(
            text="Please select at least one stock",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    

    filtered_data = {name: data for name, data in analyzer.stock_data.items()
                    if name in selected_stocks}
    

    original_data = analyzer.stock_data
    analyzer.stock_data = filtered_data
    

    normalize = chart_type == 'normalized'
    fig = analyzer.create_time_series_chart(normalize=normalize)
    

    analyzer.stock_data = original_data
    
    return fig

@app.callback(
    Output('correlation-heatmap', 'figure'),
    [Input('stock-selector', 'value')]
)
def update_correlation_heatmap(selected_stocks):
    if not selected_stocks or len(selected_stocks) < 2:
        return go.Figure().add_annotation(
            text="Select at least 2 stocks for correlation analysis",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    

    filtered_data = {name: data for name, data in analyzer.stock_data.items()
                    if name in selected_stocks}
    

    original_data = analyzer.stock_data
    analyzer.stock_data = filtered_data
    

    fig = analyzer.create_correlation_heatmap()
    

    analyzer.stock_data = original_data
    
    return fig

@app.callback(
    Output('volatility-chart', 'figure'),
    [Input('stock-selector', 'value')]
)
def update_volatility_chart(selected_stocks):
    if not selected_stocks:
        return go.Figure().add_annotation(
            text="Please select at least one stock",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    

    filtered_data = {name: data for name, data in analyzer.stock_data.items()
                    if name in selected_stocks}
    

    original_data = analyzer.stock_data
    analyzer.stock_data = filtered_data
    

    fig = analyzer.create_volatility_chart()
    

    analyzer.stock_data = original_data
    
    return fig

@app.callback(
    Output('performance-metrics-chart', 'figure'),
    [Input('stock-selector', 'value')]
)
def update_performance_metrics(selected_stocks):
    if not selected_stocks:
        return go.Figure().add_annotation(
            text="Please select stocks to view performance metrics",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    

    filtered_data = {name: data for name, data in analyzer.stock_data.items()
                    if name in selected_stocks}
    

    original_data = analyzer.stock_data
    analyzer.stock_data = filtered_data
    

    fig = analyzer.create_performance_metrics_chart()
    

    analyzer.stock_data = original_data
    
    return fig

@app.callback(
    Output('portfolio-summary', 'children'),
    [Input('stock-selector', 'value')]
)
def update_portfolio_summary(selected_stocks):
    if not selected_stocks or len(selected_stocks) < 2:
        return html.Div()

    filtered_data = {name: data for name, data in analyzer.stock_data.items()
                    if name in selected_stocks}
    original_data = analyzer.stock_data
    analyzer.stock_data = filtered_data
    portfolio_summary = analyzer.get_portfolio_summary()
    pm = portfolio_summary['portfolio_metrics']
    

    analyzer.stock_data = original_data
    
    return dbc.Card([
        dbc.CardHeader([
            html.H5("🏦 Portfolio-Level Analysis (Equal-Weighted)", className="mb-0")
        ]),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.H6("Return Metrics", className="text-primary mb-2"),
                    html.P(f"Portfolio Return: {pm['portfolio_return']:.1f}%", className="mb-1"),
                    html.P(f"Portfolio Volatility: {pm['portfolio_volatility']:.1f}%", className="mb-1"),
                    html.P(f"Sharpe Ratio: {pm['portfolio_sharpe']:.2f}", className="mb-2 mb-md-0"),
                ], width=12, md=6, lg=3, className="mb-3 mb-lg-0"),
                dbc.Col([
                    html.H6("Risk Metrics", className="text-danger mb-2"),
                    html.P(f"VaR (95%): {pm['portfolio_var']:.1f}%", className="mb-1"),
                    html.P(f"Max Drawdown: {pm['portfolio_max_drawdown']:.1f}%", className="mb-1"),
                    html.P(f"Diversification: {pm['diversification_ratio']:.2f}", className="mb-2 mb-md-0"),
                ], width=12, md=6, lg=3, className="mb-3 mb-lg-0"),
                dbc.Col([
                    html.H6("Portfolio Info", className="text-info mb-2"),
                    html.P(f"Securities: {portfolio_summary['portfolio_size']}", className="mb-1"),
                    html.P(f"Avg Correlation: {portfolio_summary['avg_correlation']:.3f}", className="mb-1"),
                    html.P(f"Data Points: {portfolio_summary['total_observations']:,}", className="mb-2 mb-md-0"),
                ], width=12, md=6, lg=3, className="mb-3 mb-lg-0"),
                dbc.Col([
                    html.H6("Analysis Period", className="text-success mb-2"),
                    html.P(f"Trading Days: {portfolio_summary['data_points']:,}", className="mb-1"),
                    html.P(f"Time Period: {portfolio_summary['data_points']/252:.1f} years", className="mb-1"),
                    html.P(f"Risk-Free Rate: {analyzer.get_current_risk_free_rate():.2%}", className="mb-0"),
                ], width=12, md=6, lg=3)
            ])
        ])
    ])

@app.callback(
    Output('summary-stats', 'children'),
    [Input('stock-selector', 'value')]
)
def update_summary_stats(selected_stocks):
    if not selected_stocks:
        return html.Div("Please select stocks to view summary statistics")
    
    summary = analyzer.get_stock_summary()
    cards = []
    for stock in selected_stocks:
        if stock in summary:
            data = summary[stock]
            return_color = "success" if data['total_return'] > 0 else "danger"
            sharpe_color = "success" if data['sharpe_ratio'] > 1 else "warning" if data['sharpe_ratio'] > 0.5 else "danger"
            
            card = dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5(f"{stock} ({data['symbol']})",
                               className="card-title text-center"),
                        html.Hr(),
                        html.P([
                            html.Strong("Current Price: "),
                            f"${data['current_price']:.2f}"
                        ], className="mb-1"),
                        html.P([
                            html.Strong("Total Return: "),
                            html.Span(f"{data['total_return']:.1f}%",
                                    className=f"text-{return_color}")
                        ], className="mb-1"),
                        html.P([
                            html.Strong("Annualized Return: "),
                            f"{data['annualized_return']:.1f}%"
                        ], className="mb-1"),
                        html.P([
                            html.Strong("Volatility: "),
                            f"{data['volatility']:.1f}%"
                        ], className="mb-1"),
                        html.P([
                            html.Strong("Sharpe Ratio: "),
                            html.Span(f"{data['sharpe_ratio']:.2f}",
                                    className=f"text-{sharpe_color}")
                        ], className="mb-1"),
                        html.P([
                            html.Strong("Max Drawdown: "),
                            f"{data['max_drawdown']:.1f}%"
                        ], className="mb-1"),
                        html.P([
                            html.Strong("VaR (95%): "),
                            f"{data['var_95']:.1f}%"
                        ], className="mb-1"),
                        html.P([
                            html.Strong("Win Rate: "),
                            f"{data['win_rate']:.1f}%"
                        ], className="mb-1"),
                        html.P([
                            html.Strong("Beta: "),
                            f"{data['beta']:.2f}" if data['beta'] else "N/A"
                        ], className="mb-0")
                    ])
                ], className="h-100")
            ], width=12, md=6, lg=4, xl=12//min(len(selected_stocks), 4), className="mb-3 mb-lg-0")
            
            cards.append(card)
    
    return dbc.Card([
        dbc.CardHeader([
            html.H5("📊 Advanced Risk Metrics & Performance Statistics", className="mb-0")
        ]),
        dbc.CardBody([
            dbc.Row(cards)
        ])
    ])
server = app.server

if __name__ == '__main__':
    import os
    
    print("\n🚀 Starting Stock Market Analysis Dashboard...")
    port = int(os.environ.get('PORT', 8050))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    if not debug:
        print(f"📊 Dashboard will be available at: http://{host}:{port}")
        print("\nFeatures available:")
        print("• Interactive time series charts with zoom/pan")
        print("• Stock correlation analysis")
        print("• Risk vs return visualization")
        print("• Real-time stock filtering")
        print("• Multiple time period views")
        print("• Advanced portfolio analytics")
    
    try:
        app.run_server(debug=debug, host=host, port=port)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        if not debug:

            app.run_server(debug=False, host='0.0.0.0', port=port)