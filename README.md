# 📈 Stock Market Analysis Dashboard

An interactive web dashboard for analyzing time series stock data of major brands with correlation analysis and advanced visualization features.

## 🚀 Features

- **Interactive Time Series Charts**: Zoom in/out of different time periods with range selectors
- **Stock Correlation Analysis**: Heatmap showing correlations between selected stocks
- **Risk vs Return Visualization**: Scatter plot analyzing volatility vs returns
- **Real-time Stock Filtering**: Select specific stocks to analyze
- **Normalized vs Actual Price Views**: Compare stocks on equal footing or see actual prices
- **Summary Statistics**: Key metrics for each stock including current price, returns, and volatility

## 📊 Supported Stocks

The dashboard analyzes these major brands:
- Apple (AAPL)
- Microsoft (MSFT)
- Google (GOOGL)
- Amazon (AMZN)
- Tesla (TSLA)
- Meta (META)
- Netflix (NFLX)
- NVIDIA (NVDA)
- JPMorgan (JPM)
- Johnson & Johnson (JNJ)

## 🛠️ Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the dashboard:**
   ```bash
   python run_dashboard.py
   ```

3. **Open your browser and navigate to:**
   ```
   http://127.0.0.1:8050
   ```

## 📋 Requirements

- Python 3.7+
- Internet connection (for fetching stock data)
- Web browser

## 🎯 Usage

1. **Time Series Analysis**: 
   - Use the range selector buttons (1M, 3M, 6M, 1Y, All) to zoom into specific periods
   - Toggle between normalized and actual price views
   - Select/deselect stocks using the dropdown

2. **Correlation Analysis**:
   - View the correlation heatmap to understand how stocks move together
   - Values closer to 1 indicate strong positive correlation
   - Values closer to -1 indicate strong negative correlation

3. **Risk Analysis**:
   - The volatility chart shows risk (x-axis) vs return (y-axis)
   - Stocks in the upper-left quadrant offer high returns with lower risk
   - Color coding indicates total return performance

## 🔧 Technical Details

- **Data Source**: Yahoo Finance (via yfinance library)
- **Frontend**: Dash with Bootstrap components
- **Visualization**: Plotly for interactive charts
- **Analysis**: Pandas and NumPy for data processing

## 📈 Dashboard Components

- **Main Time Series Chart**: Interactive line chart with zoom/pan capabilities
- **Correlation Heatmap**: Shows relationships between stock movements
- **Risk vs Return Scatter**: Analyzes volatility against total returns
- **Summary Cards**: Key statistics for selected stocks

## 🚨 Notes

- Stock data is fetched in real-time from Yahoo Finance
- Default period is 2 years of historical data
- Dashboard updates automatically when selections change
- All calculations use daily closing prices
