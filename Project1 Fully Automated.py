import subprocess
import webbrowser
import time
import os

# Path to the Streamlit app file
streamlit_file = 'Day2.py'

# Port number for Streamlit (default is 8501)
port = 8504
def find_available_port(starting_port):
    port = starting_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            result = s.connect_ex(('localhost', port))
            if result != 0:
                return port
        port += 1
        
url = f'http://localhost:{port}'

def run_streamlit_app():
    # Start the Streamlit server
    process = subprocess.Popen(['streamlit', 'run', streamlit_file, '--server.port', str(port)])

    try:
        # Wait for a short time to ensure the server starts
        time.sleep(5)  # Adjust if needed for your app to fully start

        # Open the Streamlit app in a web browser
        # webbrowser.open_new_tab(url) ensures that it opens in a new tab if possible
        if not any(tab.startswith(url) for tab in webbrowser._open_tab):
            webbrowser.open(url, new=2)

        # Wait for the Streamlit app to run for a while before stopping it
        time.sleep(5)  # Run for 30 seconds or adjust based on your needs
        
        # Terminate the Streamlit server
        process.terminate()
        print("Streamlit app stopped automatically after running once.")
    
    except KeyboardInterrupt:
        print("Streamlit app interrupted by user.")
        process.terminate()

if __name__ == '__main__':
    run_streamlit_app()

