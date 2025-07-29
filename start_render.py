import os
import sys
import time
import signal
from dashboard import app, analyzer
def signal_handler(signum, frame):
    print(f"\nReceived signal {signum}, shutting down gracefully...")
    sys.exit(0)

def preload_data():
    print("Preloading stock data for faster response times...")
    try:
        start_time = time.time()
        success = analyzer.fetch_stock_data(period='2y')
        load_time = time.time() - start_time
        if success:
            print(f"Data loaded successfully in {load_time:.1f} seconds")
            print(f"Loaded {len(analyzer.stock_data)} stocks")
            return True
        else:
            print("⚠Some data failed to load, but continuing...")
            return len(analyzer.stock_data) > 0
            
    except Exception as e:
        print(f"Error loading data: {e}")
        print("Continuing with limited functionality...")
        return False

def main():

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    print("Starting Stock Market Dashboard on Render.com")
    print("=" * 60)
    port = int(os.environ.get('PORT', 10000))
    debug = os.environ.get('DEBUG', 'false').lower() == 'true'
    
    print(f"Port: {port}")
    print(f"Debug: {debug}")
    print(f"Environment: {'Development' if debug else 'Production'}")
    data_loaded = preload_data()
    
    if not data_loaded:
        print("Warning: Running with limited data")
    
    try:
        if debug:
            app.run_server(debug=True, host='0.0.0.0', port=port)
        else:
            print("🔧 Starting in production mode...")
            app.run_server(debug=False, host='0.0.0.0', port=port)
            
    except Exception as e:
        print(f"Server startup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
