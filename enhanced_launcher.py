"""
Enhanced Heart Disease Severity Prediction System Launcher
Launches both API and Web Interface with severity prediction capabilities
"""

import subprocess
import time
import sys
import os
from threading import Thread

def start_api():
    """Start the Enhanced Severity API server."""
    print("🚀 Starting Enhanced Severity API Server...")
    try:
        subprocess.run([sys.executable, "enhanced_severity_api.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Enhanced API server stopped")
    except Exception as e:
        print(f"❌ Error starting API server: {e}")

def start_web_interface():
    """Start the Enhanced Web Interface."""
    print("🌐 Starting Enhanced Web Interface...")
    time.sleep(3)  # Wait for API to start
    try:
        subprocess.run([sys.executable, "enhanced_web_interface.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Enhanced web interface stopped")
    except Exception as e:
        print(f"❌ Error starting web interface: {e}")

def main():
    """Launch the enhanced system."""
    print("=" * 70)
    print("🔬 ENHANCED HEART DISEASE SEVERITY PREDICTION SYSTEM")
    print("=" * 70)
    print("📊 Features:")
    print("   • Binary Classification (Disease/No Disease)")
    print("   • Severity Level Prediction (0-4)")
    print("   • Advanced Visualization")
    print("   • Detailed Probability Analysis")
    print("=" * 70)
    
    # Check if files exist
    required_files = [
        "enhanced_severity_api.py",
        "enhanced_web_interface.py", 
        "heart_disease_data.csv"
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Missing required file: {file}")
            return
    
    print("✅ All required files found")
    print("\n🚀 Starting services...")
    
    # Start API server in background thread
    api_thread = Thread(target=start_api, daemon=True)
    api_thread.start()
    
    # Start web interface in main thread
    try:
        start_web_interface()
    except KeyboardInterrupt:
        print("\n🛑 Enhanced system shutdown initiated")
    
    print("\n📊 Enhanced Heart Disease Severity Prediction System stopped")
    print("🎯 System provided both binary and severity-level predictions!")

if __name__ == '__main__':
    main()
