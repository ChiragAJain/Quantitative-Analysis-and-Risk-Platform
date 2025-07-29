import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from stock_analyzer import StockAnalyzer
import pandas as pd

# Initialize the stock analyzer
analyzer = StockAnalyzer()

# Initialize Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Stock Market Analysis Dashboard"

# Fetch data on startup
print("Initializing dashboard...")
if analyzer.fetch_stock_data():
    print("✓ Data loaded successfully!")
else:
    print("✗ Failed to load data")

# Define the layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("📈 Stock Market Analysis Dashboard", 
                   className="text-center mb-4",
                   style={'color': '#2c3e50', 'fontWeight': 'bold'})
        ])
    ]),
    
    # Control Panel
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Dashboard Controls", className="card-title"),
                    dbc.Row([
                        dbc.Col([
                            html.Label("Chart Type:", className="fw-bold"),
                            dcc.Dropdown(
                                id='chart-type-dropdown',
                                options=[
                                    {'label': 'Normalized Prices', 'value': 'normalized'},
                                    {'label': 'Actual Prices', 'value': 'actual'}
                                ],
                                value='normalized',
                                clearable=False
                            )
                        ], width=6),
                        dbc.Col([
                            html.Label("Select Stocks:", className="fw-bold"),
                            dcc.Dropdown(
                                id='stock-selector',
                                options=[{'label': name, 'value': name} 
                                        for name in analyzer.major_stocks.keys()],
                                value=list(analyzer.major_stocks.keys()),
                                multi=True
                            )
                        ], width=6)
                    ])
                ])
            ], className="mb-4")
        ])
    ]),
    
    # Main Charts Row
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='time-series-chart')
        ], width=12)
    ], className="mb-4"),
    
    # Secondary Charts Row
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='correlation-heatmap')
        ], width=6),
        dbc.Col([
            dcc.Graph(id='volatility-chart')
        ], width=6)
    ], className="mb-4"),
    
    # Performance Metrics Row
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='performance-metrics-chart')
        ], width=12)
    ], className="mb-4"),
    
    # Portfolio Summary Row
    dbc.Row([
        dbc.Col([
            html.Div(id='portfolio-summary')
        ], width=12)
    ], className="mb-4"),
    
    # Summary Statistics
    dbc.Row([
        dbc.Col([
            html.Div(id='summary-stats')
        ])
    ])
    
], fluid=True)

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
    
    # Filter data for selected stocks
    filtered_data = {name: data for name, data in analyzer.stock_data.items() 
                    if name in selected_stocks}
    
    # Temporarily update analyzer data
    original_data = analyzer.stock_data
    analyzer.stock_data = filtered_data
    
    # Create chart
    normalize = chart_type == 'normalized'
    fig = analyzer.create_time_series_chart(normalize=normalize)
    
    # Restore original data
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
    
    # Filter data for selected stocks
    filtered_data = {name: data for name, data in analyzer.stock_data.items() 
                    if name in selected_stocks}
    
    # Temporarily update analyzer data
    original_data = analyzer.stock_data
    analyzer.stock_data = filtered_data
    
    # Create heatmap
    fig = analyzer.create_correlation_heatmap()
    
    # Restore original data
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
    
    # Filter data for selected stocks
    filtered_data = {name: data for name, data in analyzer.stock_data.items() 
                    if name in selected_stocks}
    
    # Temporarily update analyzer data
    original_data = analyzer.stock_data
    analyzer.stock_data = filtered_data
    
    # Create volatility chart
    fig = analyzer.create_volatility_chart()
    
    # Restore original data
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
    
    # Filter data for selected stocks
    filtered_data = {name: data for name, data in analyzer.stock_data.items() 
                    if name in selected_stocks}
    
    # Temporarily update analyzer data
    original_data = analyzer.stock_data
    analyzer.stock_data = filtered_data
    
    # Create performance metrics chart
    fig = analyzer.create_performance_metrics_chart()
    
    # Restore original data
    analyzer.stock_data = original_data
    
    return fig

@app.callback(
    Output('portfolio-summary', 'children'),
    [Input('stock-selector', 'value')]
)
def update_portfolio_summary(selected_stocks):
    if not selected_stocks or len(selected_stocks) < 2:
        return html.Div()
    
    # Filter data for selected stocks
    filtered_data = {name: data for name, data in analyzer.stock_data.items() 
                    if name in selected_stocks}
    
    # Temporarily update analyzer data
    original_data = analyzer.stock_data
    analyzer.stock_data = filtered_data
    
    # Get portfolio summary
    portfolio_summary = analyzer.get_portfolio_summary()
    pm = portfolio_summary['portfolio_metrics']
    
    # Restore original data
    analyzer.stock_data = original_data
    
    return dbc.Card([
        dbc.CardHeader([
            html.H5("🏦 Portfolio-Level Analysis (Equal-Weighted)", className="mb-0")
        ]),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.H6("Return Metrics", className="text-primary"),
                    html.P(f"Portfolio Return: {pm['portfolio_return']:.1f}% (annualized)"),
                    html.P(f"Portfolio Volatility: {pm['portfolio_volatility']:.1f}%"),
                    html.P(f"Sharpe Ratio: {pm['portfolio_sharpe']:.2f}"),
                ], width=3),
                dbc.Col([
                    html.H6("Risk Metrics", className="text-danger"),
                    html.P(f"Value at Risk (95%): {pm['portfolio_var']:.1f}%"),
                    html.P(f"Maximum Drawdown: {pm['portfolio_max_drawdown']:.1f}%"),
                    html.P(f"Diversification Ratio: {pm['diversification_ratio']:.2f}"),
                ], width=3),
                dbc.Col([
                    html.H6("Portfolio Composition", className="text-info"),
                    html.P(f"Number of Securities: {portfolio_summary['portfolio_size']}"),
                    html.P(f"Average Correlation: {portfolio_summary['avg_correlation']:.3f}"),
                    html.P(f"Total Data Points: {portfolio_summary['total_observations']:,}"),
                ], width=3),
                dbc.Col([
                    html.H6("Analysis Parameters", className="text-success"),
                    html.P(f"Trading Days: {portfolio_summary['data_points']:,}"),
                    html.P(f"Time Period: {portfolio_summary['data_points']/252:.1f} years"),
                    html.P(f"Risk-Free Rate: {analyzer.get_current_risk_free_rate():.2%}"),
                ], width=3)
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
    
    # Create cards for each selected stock
    cards = []
    for stock in selected_stocks:
        if stock in summary:
            data = summary[stock]
            
            # Determine color based on return
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
            ], width=12//min(len(selected_stocks), 3))
            
            cards.append(card)
    
    return dbc.Card([
        dbc.CardHeader([
            html.H5("📊 Advanced Risk Metrics & Performance Statistics", className="mb-0")
        ]),
        dbc.CardBody([
            dbc.Row(cards)
        ])
    ])

# Expose server for deployment
server = app.server

if __name__ == '__main__':
    import os
    
    print("\n🚀 Starting Stock Market Analysis Dashboard...")
    
    # Get port from environment variable (for deployment) or use default
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
            # In production, try to start with basic configuration
            app.run_server(debug=False, host='0.0.0.0', port=port)