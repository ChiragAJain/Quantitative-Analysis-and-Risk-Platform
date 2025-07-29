import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from scipy.stats import pearsonr
import warnings
warnings.filterwarnings('ignore')

class StockAnalyzer:
    def __init__(self):
        self.major_stocks = {
            'Apple': 'AAPL',
            'Microsoft': 'MSFT', 
            'Google': 'GOOGL',
            'Amazon': 'AMZN',
            'Tesla': 'TSLA',
            'Meta': 'META',
            'Netflix': 'NFLX',
            'NVIDIA': 'NVDA',
            'JPMorgan': 'JPM',
            'Johnson & Johnson': 'JNJ'
        }
        self.stock_data = {}
    def fetch_stock_data(self, period='2y'):
        print("Fetching stock data...")
        for name, symbol in self.major_stocks.items():
            try:
                ticker = yf.Ticker(symbol)
                data = ticker.history(period=period)
                if not data.empty:
                    self.stock_data[name] = data
                    print(f"{name} ({symbol})")
                else:
                    print(f"No data for {name} ({symbol})")
            except Exception as e:
                print(f"Error fetching {name}: {e}")
        
        return len(self.stock_data) > 0
    
    def calculate_returns(self):
        returns_data = {}
        for name, data in self.stock_data.items():
            returns_data[name] = data['Close'].pct_change().dropna()
        return pd.DataFrame(returns_data)
    
    def calculate_correlation_matrix(self):
        returns_df = self.calculate_returns()
        return returns_df.corr()
    
    def get_current_risk_free_rate(self):
        try:
            treasury = yf.Ticker("^TNX")
            data = treasury.history(period="5d")
            if not data.empty:
                current_rate = data['Close'].iloc[-1] / 100 
                print(f"Using current 10Y Treasury rate: {current_rate:.2%}")
                return current_rate
        except Exception as e:
            print(f"Could not fetch Treasury rate: {e}")
        fallback_rate = 0.045 
        print(f"Using fallback risk-free rate: {fallback_rate:.2%}")
        return fallback_rate
    def calculate_sharpe_ratio(self, returns, risk_free_rate=None):
        if risk_free_rate is None:
            risk_free_rate = self.get_current_risk_free_rate()
        excess_returns = returns.mean() * 252 - risk_free_rate
        volatility = returns.std() * np.sqrt(252)
        return excess_returns / volatility if volatility != 0 else 0
    
    def calculate_max_drawdown(self, prices):
        cumulative = (1 + prices.pct_change()).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        return drawdown.min() * 100
    
    def calculate_var(self, returns, confidence=0.05):
        return np.percentile(returns, confidence * 100) * 100
    
    def calculate_beta(self, stock_returns, market_returns):
        covariance = np.cov(stock_returns, market_returns)[0][1]
        market_variance = np.var(market_returns)
        return covariance / market_variance if market_variance != 0 else 0
    
    def get_stock_summary(self):
        summary = {}
        returns_df = self.calculate_returns()
        try:
            spy = yf.Ticker('SPY').history(period='2y')
            market_returns = spy['Close'].pct_change().dropna()
        except:
            market_returns = None
        
        for name, data in self.stock_data.items():
            current_price = data['Close'].iloc[-1]
            start_price = data['Close'].iloc[0]
            total_return = ((current_price - start_price) / start_price) * 100
            stock_returns = returns_df[name]
            volatility = stock_returns.std() * np.sqrt(250) * 100
            sharpe_ratio = self.calculate_sharpe_ratio(stock_returns)
            max_drawdown = self.calculate_max_drawdown(data['Close'])
            var_95 = self.calculate_var(stock_returns)
            beta = None
            if market_returns is not None and len(stock_returns) > 0:
                aligned_stock = stock_returns.reindex(market_returns.index).dropna()
                aligned_market = market_returns.reindex(aligned_stock.index).dropna()
                if len(aligned_stock) > 20:  # Need sufficient data
                    beta = self.calculate_beta(aligned_stock, aligned_market)
            annualized_return = ((1 + stock_returns.mean()) ** 250 - 1) * 100
            win_rate = (stock_returns > 0).sum() / len(stock_returns) * 100
            
            summary[name] = {
                'current_price': current_price,
                'total_return': total_return,
                'annualized_return': annualized_return,
                'volatility': volatility,
                'sharpe_ratio': sharpe_ratio,
                'max_drawdown': max_drawdown,
                'var_95': var_95,
                'beta': beta,
                'win_rate': win_rate,
                'symbol': self.major_stocks[name],
                'trading_days': len(stock_returns)
            }
        return summary
    
    def create_time_series_chart(self, normalize=True):
        fig = go.Figure()
        colors = px.colors.qualitative.Set3
        
        for i, (name, data) in enumerate(self.stock_data.items()):
            if normalize:
                normalized_prices = (data['Close'] / data['Close'].iloc[0]) * 100
                y_data = normalized_prices
                y_title = "Normalized Price (Base = 100)"
            else:
                y_data = data['Close']
                y_title = "Stock Price ($)"
            fig.add_trace(go.Scatter(
                x=data.index,
                y=y_data,
                mode='lines',
                name=name,
                line=dict(color=colors[i % len(colors)], width=2),
                hovertemplate=f'<b>{name}</b><br>' +
                             'Date: %{x}<br>' +
                             'Price: %{y:.2f}<br>' +
                             '<extra></extra>'
            ))
        
        fig.update_layout(
            title=dict(
                text="Stock Price Time Series Analysis",
                x=0.5,
                font=dict(size=16)
            ),
            xaxis_title="Date",
            yaxis_title=y_title,
            hovermode='x unified',
            template='plotly_white',
            height=450,  # Mobile-optimized height
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=10)  # Smaller legend font
            ),
            margin=dict(l=40, r=40, t=60, b=40)  # Tighter margins
        )
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1M", step="month", stepmode="backward"),
                        dict(count=3, label="3M", step="month", stepmode="backward"),
                        dict(count=6, label="6M", step="month", stepmode="backward"),
                        dict(count=1, label="1Y", step="year", stepmode="backward"),
                        dict(step="all", label="All")
                    ])
                ),
                rangeslider=dict(visible=True),
                type="date"
            )
        )
        
        return fig
    
    def create_correlation_heatmap(self):
        corr_matrix = self.calculate_correlation_matrix()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.index,
            colorscale='pubu',
            zmid=0,
            text=np.round(corr_matrix.values, 2),
            texttemplate="%{text}",
            textfont={"size": 10},
            hovertemplate='<b>%{y} vs %{x}</b><br>Correlation: %{z:.3f}<extra></extra>'
        ))
        
        fig.update_layout(
            title=dict(
                text="Stock Correlation Matrix",
                x=0.5,
                font=dict(size=14)
            ),
            height=380,  # Mobile-optimized height
            template='plotly_white',
            margin=dict(l=50, r=50, t=60, b=50)
        )
        return fig
    
    def create_volatility_chart(self):
        summary = self.get_stock_summary()
        
        stocks = list(summary.keys())
        volatilities = [summary[stock]['volatility'] for stock in stocks]
        returns = [summary[stock]['annualized_return'] for stock in stocks]
        sharpe_ratios = [summary[stock]['sharpe_ratio'] for stock in stocks]
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=volatilities,
            y=returns,
            mode='markers+text',
            text=stocks,
            textposition="top center",
            marker=dict(
                size=[abs(sr) * 8 + 8 for sr in sharpe_ratios],
                color=sharpe_ratios,
                colorscale='RdYlGn',
                showscale=True,
                colorbar=dict(title="Sharpe Ratio"),
                line=dict(width=1, color='black')
            ),
            hovertemplate='<b>%{text}</b><br>' +
                         'Volatility: %{x:.1f}%<br>' +
                         'Annualized Return: %{y:.1f}%<br>' +
                         'Sharpe Ratio: %{marker.color:.2f}<br>' +
                         '<extra></extra>',
            customdata=sharpe_ratios
        ))
        
        fig.update_layout(
            title=dict(
                text="Risk-Adjusted Return Analysis",
                x=0.5,
                font=dict(size=14)
            ),
            xaxis_title="Volatility (%)",
            yaxis_title="Return (%)",
            template='plotly_white',
            height=420,  # Mobile-optimized height
            margin=dict(l=50, r=50, t=60, b=50),
            annotations=[
                dict(
                    text="Size = Sharpe Ratio",
                    xref="paper", yref="paper",
                    x=0.02, y=0.98,
                    showarrow=False,
                    font=dict(size=9)
                )
            ]
        )
        
        return fig
    
    def create_performance_metrics_chart(self):
        summary = self.get_stock_summary()
        metrics_data = []
        for stock, data in summary.items():
            metrics_data.append({
                'Stock': stock,
                'Sharpe Ratio': data['sharpe_ratio'],
                'Max Drawdown (%)': abs(data['max_drawdown']),
                'VaR 95% (%)': abs(data['var_95']),
                'Win Rate (%)': data['win_rate'],
                'Beta': data['beta'] if data['beta'] else 0
            })
        
        df = pd.DataFrame(metrics_data)
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Sharpe Ratio', 'Maximum Drawdown (%)', 
                          'Value at Risk 95% (%)', 'Win Rate (%)'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Sharpe Ratio
        fig.add_trace(
            go.Bar(x=df['Stock'], y=df['Sharpe Ratio'], name='Sharpe Ratio',
                   marker_color='lightblue'),
            row=1, col=1
        )
        
        # Max Drawdown
        fig.add_trace(
            go.Bar(x=df['Stock'], y=df['Max Drawdown (%)'], name='Max Drawdown',
                   marker_color='lightcoral'),
            row=1, col=2
        )
        
        # VaR
        fig.add_trace(
            go.Bar(x=df['Stock'], y=df['VaR 95% (%)'], name='VaR 95%',
                   marker_color='lightsalmon'),
            row=2, col=1
        )
        
        # Win Rate
        fig.add_trace(
            go.Bar(x=df['Stock'], y=df['Win Rate (%)'], name='Win Rate',
                   marker_color='lightgreen'),
            row=2, col=2
        )
        
        fig.update_layout(
            title_text="Risk Metrics Dashboard",
            title_font_size=14,
            showlegend=False,
            height=480,  # Mobile-optimized height
            margin=dict(l=50, r=50, t=60, b=50)
        )
        
        # Rotate x-axis labels
        fig.update_xaxes(tickangle=45)
        
        return fig
    
    def calculate_portfolio_metrics(self, weights=None):
        """Calculate portfolio-level metrics with equal or custom weights"""
        returns_df = self.calculate_returns()
        
        if weights is None:
            weights = np.array([1/len(returns_df.columns)] * len(returns_df.columns))
        portfolio_returns = (returns_df * weights).sum(axis=1)
        portfolio_return = portfolio_returns.mean() * 250 * 100
        portfolio_volatility = portfolio_returns.std() * np.sqrt(250) * 100
        portfolio_sharpe = self.calculate_sharpe_ratio(portfolio_returns)
        portfolio_var = self.calculate_var(portfolio_returns)
        portfolio_cumulative = (1 + portfolio_returns).cumprod()
        portfolio_max_dd = self.calculate_max_drawdown(portfolio_cumulative)
        
        return {
            'portfolio_return': portfolio_return,
            'portfolio_volatility': portfolio_volatility,
            'portfolio_sharpe': portfolio_sharpe,
            'portfolio_var': portfolio_var,
            'portfolio_max_drawdown': portfolio_max_dd,
            'diversification_ratio': self.calculate_diversification_ratio(returns_df, weights)
        }
    
    def calculate_diversification_ratio(self, returns_df, weights):
        individual_vols = returns_df.std() * np.sqrt(250)
        weighted_avg_vol = np.sum(weights * individual_vols)
        portfolio_vol = (returns_df * weights).sum(axis=1).std() * np.sqrt(250)
        return weighted_avg_vol / portfolio_vol if portfolio_vol != 0 else 1
    
    def get_portfolio_summary(self):
        portfolio_metrics = self.calculate_portfolio_metrics()
        individual_summary = self.get_stock_summary()
        returns_df = self.calculate_returns()
        actual_trading_days = len(returns_df) 
        avg_correlation = self.calculate_correlation_matrix().values[np.triu_indices_from(
            self.calculate_correlation_matrix().values, k=1)].mean()
        return {
            'portfolio_metrics': portfolio_metrics,
            'individual_metrics': individual_summary,
            'portfolio_size': len(self.stock_data),
            'avg_correlation': avg_correlation,
            'data_points': actual_trading_days,
            'total_observations': actual_trading_days * len(self.stock_data)
        }
