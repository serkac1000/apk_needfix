#!/usr/bin/env python3
"""
Auto-start server script for APK Editor
Automatically starts the Flask server and opens browser to 127.0.0.1:5000
"""

import os
import sys
import time
import threading
import webbrowser
import logging
from urllib.request import urlopen
from urllib.error import URLError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def check_server_ready(host='127.0.0.1', port=5000, timeout=30):
    """Check if server is ready to accept connections"""
    url = f'http://{host}:{port}'
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            response = urlopen(url, timeout=5)
            if response.getcode() == 200:
                logging.info(f"Server is ready at {url}")
                return True
        except URLError:
            time.sleep(1)
            continue
    
    logging.warning(f"Server not ready after {timeout} seconds")
    return False

def open_browser(host='127.0.0.1', port=5000, delay=3):
    """Open browser after a delay"""
    time.sleep(delay)
    url = f'http://{host}:{port}'
    
    if check_server_ready(host, port):
        logging.info(f"Opening browser to {url}")
        webbrowser.open(url)
    else:
        logging.error("Server not ready, browser not opened")

def start_server():
    """Start the Flask server"""
    try:
        # Import and start the app
        from app import app
        
        host = '127.0.0.1'
        port = 5000
        
        logging.info(f"Starting APK Editor server at http://{host}:{port}")
        logging.info("Press Ctrl+C to stop the server")
        
        # Start browser opening in background thread
        browser_thread = threading.Thread(target=open_browser, args=(host, port, 2))
        browser_thread.daemon = True
        browser_thread.start()
        
        # Start Flask server
        app.run(
            debug=False,  # Set to False for auto-start to avoid reloader issues
            host=host,
            port=port,
            use_reloader=False  # Disable reloader for clean auto-start
        )
        
    except ImportError as e:
        logging.error(f"Failed to import app: {e}")
        print("Error: Could not import the Flask app. Make sure all dependencies are installed.")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Failed to start server: {e}")
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    print("=" * 60)
    print("APK Editor - Auto Start Server")
    print("=" * 60)
    print("Starting server and opening browser automatically...")
    print("Server will be available at: http://127.0.0.1:5000")
    print("=" * 60)
    
    start_server()