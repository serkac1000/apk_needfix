import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

try:
    from app import app
    logging.info("App imported successfully")
    
    if __name__ == '__main__':
        port = int(os.environ.get('PORT', 5000))
        logging.info(f"Starting APK Editor on port {port}")
        app.run(debug=True, host='0.0.0.0', port=port)
        
except Exception as e:
    logging.error(f"Failed to start application: {e}")
    print(f"Error starting app: {e}")
    raise
