#!/usr/bin/env python3
"""
Render.com optimized startup script for Stock Market Dashboard
Handles data loading with proper error handling and timeouts
"""

import os
import sys
import time
import signal
from dashboard import app, analyzer

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    print(f"\n🛑 Received signal {signum}, shutting down gracefully...")
    sys.exit(0)

def preload_data():
    """Preload stock data with timeout and error handling"""
    print("🔄 Preloading stock data for faster response times...")
    
    try:
        # Set a timeout for data loading
        start_time = time.time()
        success = analyzer.fetch_stock_data(period='2y')
        load_time = time.time() - start_time
        
        if success:
            print(f"✅ Data loaded successfully in {load_time:.1f} seconds")
            print(f"📊 Loaded {len(analyzer.stock_data)} stocks")
            return True
        else:
            print("⚠️ Some data failed to load, but continuing...")
            return len(analyzer.stock_data) > 0
            
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        print("🔄 Continuing with limited functionality...")
        return False

def main():
    """Main startup function optimized for Render"""
    
    # Register signal handlers
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    print("🚀 Starting Stock Market Dashboard on Render.com")
    print("=" * 60)
    
    # Get environment variables
    port = int(os.environ.get('PORT', 10000))
    debug = os.environ.get('DEBUG', 'false').lower() == 'true'
    
    print(f"📡 Port: {port}")
    print(f"🐛 Debug: {debug}")
    print(f"🌍 Environment: {'Development' if debug else 'Production'}")
    
    # Preload data (with timeout for Render's build limits)
    data_loaded = preload_data()
    
    if not data_loaded:
        print("⚠️ Warning: Running with limited data")
    
    print("\n🌐 Dashboard Features:")
    print("• Interactive time series analysis")
    print("• Real-time correlation matrices") 
    print("• Portfolio optimization metrics")
    print("• Advanced risk analytics")
    print("• Dynamic Treasury rate integration")
    
    print(f"\n🎯 Dashboard will be available at your Render URL")
    print("📱 Optimized for mobile and desktop viewing")
    print("\n" + "=" * 60)
    
    # Start the server
    try:
        if debug:
            app.run_server(debug=True, host='0.0.0.0', port=port)
        else:
            # Production mode - let gunicorn handle this
            print("🔧 Starting in production mode...")
            app.run_server(debug=False, host='0.0.0.0', port=port)
            
    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()