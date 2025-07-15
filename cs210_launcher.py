"""
CS210 Final Project Launcher
Complete launcher for the Heart Disease Prediction System
Includes all components: API, Web Interface, and Streamlit App
"""

import subprocess
import time
import os
import sys
from pathlib import Path
import webbrowser
from threading import Thread

class CS210ProjectLauncher:
    def __init__(self):
        self.processes = []
        self.project_dir = Path(__file__).parent

    def print_banner(self):
        """Print project banner."""
        print("=" * 80)
        print(" CS210 FINAL PROJECT - HEART DISEASE PREDICTION SYSTEM")
        print("=" * 80)
        print("Author: AP")
        print("Course: CS210 - Data Management for Data Science")
        print("Date: July 2025")
        print("Features: Multi-Model ML Pipeline + Interactive Web Apps")
        print("=" * 80)

    def check_dependencies(self):
        """Check if required packages are installed."""
        required_packages = [
            'flask', 'scikit-learn', 'pandas', 'numpy',
            'streamlit', 'plotly', 'requests'
        ]

        missing_packages = []
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                missing_packages.append(package)

        if missing_packages:
            print(f" Missing packages: {', '.join(missing_packages)}")
            print("📦 Installing missing packages...")

            for package in missing_packages:
                try:
                    subprocess.run([sys.executable, '-m', 'pip', 'install', package],
                                 check=True, capture_output=True)
                    print(f" Installed {package}")
                except subprocess.CalledProcessError:
                    print(f" Failed to install {package}")
                    return False

        print(" All dependencies satisfied")
        return True

    def start_api_server(self):
        """Start the Flask API server."""
        print("\n Starting CS210 API Server...")
        api_file = self.project_dir / "heart_disease_api.py"

        if not api_file.exists():
            print(f" API file not found: {api_file}")
            return False

        try:
            process = subprocess.Popen([
                sys.executable, str(api_file)
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            self.processes.append(('API Server', process))
            print(" API Server started on http://localhost:5000")

            # Wait for server to start
            time.sleep(3)
            return True

        except Exception as e:
            print(f" Failed to start API server: {e}")
            return False

    def start_improved_web_interface(self):
        """Start the improved web interface if it exists."""
        print("\n Starting Improved Web Interface...")
        web_file = self.project_dir / "improved_web_interface.py"

        if web_file.exists():
            try:
                process = subprocess.Popen([
                    sys.executable, str(web_file)
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                self.processes.append(('Improved Web Interface', process))
                print(" Improved Web Interface started on http://localhost:5000")
                time.sleep(2)
                return True

            except Exception as e:
                print(f" Failed to start improved web interface: {e}")
                return False
        else:
            print(" Improved web interface not found, skipping...")
            return True

    def start_streamlit_app(self):
        """Start the Streamlit application."""
        print("\n Starting CS210 Streamlit App...")
        app_file = self.project_dir / "app.py"

        if not app_file.exists():
            print(f" Streamlit app file not found: {app_file}")
            return False

        try:
            process = subprocess.Popen([
                sys.executable, '-m', 'streamlit', 'run', str(app_file),
                '--server.port', '8501',
                '--server.headless', 'true'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            self.processes.append(('Streamlit App', process))
            print(" Streamlit App started on http://localhost:8501")

            # Wait for Streamlit to start
            time.sleep(5)
            return True

        except Exception as e:
            print(f" Failed to start Streamlit app: {e}")
            return False

    def open_browsers(self):
        """Open browsers for the applications."""
        print("\n Opening applications in browser...")

        time.sleep(2)

        # Open Streamlit app (main interface)
        try:
            webbrowser.open('http://localhost:8501')
            print(" Opened Streamlit App in browser")
        except:
            print(" Could not open Streamlit App in browser")

        # Open API documentation (if improved interface is not running)
        if not any('Improved Web Interface' in name for name, _ in self.processes):
            try:
                webbrowser.open('http://localhost:5000/example')
                print(" Opened API Documentation in browser")
            except:
                print(" Could not open API Documentation in browser")

    def display_access_info(self):
        """Display access information."""
        print("\n" + "=" * 80)
        print(" CS210 HEART DISEASE PREDICTION SYSTEM - READY!")
        print("=" * 80)

        print("\n ACCESS POINTS:")

        if any('Streamlit App' in name for name, _ in self.processes):
            print("🏠 Main Application (Streamlit): http://localhost:8501")
            print("   • Interactive risk assessment forms")
            print("   • CS210 model performance analysis")
            print("   • Feature importance visualization")
            print("   • Project documentation")

        if any('API Server' in name for name, _ in self.processes):
            print("\n🔌 API Endpoints: http://localhost:5000")
            print("   • POST /predict - Single patient prediction")
            print("   • GET /model_performance - CS210 evaluation results")
            print("   • GET /feature_importance - Feature analysis")
            print("   • GET /example - API usage examples")

        if any('Improved Web Interface' in name for name, _ in self.processes):
            print("\n✨ Improved Interface: http://localhost:5000")
            print("   • Severity prediction system")
            print("   • Color-coded risk levels")
            print("   • Interactive visualizations")

        print("\n CS210 PROJECT FEATURES:")
        print("   • Multi-model comparison (Logistic, RF, GB)")
        print("   • 85.9% accuracy with Gradient Boosting")
        print("   • Key feature identification (cholesterol, max HR)")
        print("   • Deployment-ready deployment")
        print("   • Interactive web applications")

        print("\n" + "=" * 80)

    def wait_for_exit(self):
        """Wait for user to exit and cleanup."""
        try:
            print("\n⌨  Press Ctrl+C to stop all services...")
            while True:
                # Check if any process has terminated
                for name, process in self.processes:
                    if process.poll() is not None:
                        print(f"  {name} has stopped")

                time.sleep(1)

        except KeyboardInterrupt:
            print("\n\n🛑 Shutting down CS210 Heart Disease Prediction System...")
            self.cleanup()

    def cleanup(self):
        """Clean up all processes."""
        for name, process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f" Stopped {name}")
            except subprocess.TimeoutExpired:
                process.kill()
                print(f"🔨 Force killed {name}")
            except Exception as e:
                print(f" Error stopping {name}: {e}")

        print("\n👋 Thank you for using the CS210 Heart Disease Prediction System!")
        print("📚 Project demonstrates: ML Pipeline + Model Comparison + Web Deployment")

    def run(self):
        """Run the complete CS210 project."""
        self.print_banner()

        # Check dependencies
        if not self.check_dependencies():
            print(" Cannot start due to missing dependencies")
            return

        # Start services
        success = True

        # Start API server
        if not self.start_api_server():
            success = False

        # Start improved web interface (if available)
        self.start_improved_web_interface()

        # Start Streamlit app
        if not self.start_streamlit_app():
            success = False

        if not success:
            print(" Some services failed to start")
            self.cleanup()
            return

        # Open browsers and display info
        self.open_browsers()
        self.display_access_info()

        # Wait for exit
        self.wait_for_exit()

def main():
    """Main function."""
    launcher = CS210ProjectLauncher()
    launcher.run()

if __name__ == '__main__':
    main()
