import subprocess
import atexit
import ollama
import sys
import time

def install_deps():
    """
    Install dependencies and get the server running.
    """
    atexit.register(stop_server)

    # Check if winget is available (Windows Package Manager)
    print("Checking for winget (Windows Package Manager)...")
    try:
        # Run the 'winget --version' command
        result = subprocess.run(['winget', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        
        # If it runs successfully, winget is available
        if result.returncode == 0:
            print("winget is available.")
            print(result.stdout.decode())  # Print the version
        else:
            print("winget is not available. Please install Windows Package Manager first.")
            exit(1)

    except FileNotFoundError:
        print("winget is not available.")
        print("Please install Windows Package Manager from the Microsoft Store or download the installer from GitHub.")
        exit(1)

    # Install dependencies using winget
    try:
        print("Installing ollama...")
        subprocess.run(['winget', 'install', 'Ollama.Ollama'], check=True, shell=True)
        print("ollama installed successfully.")
    except subprocess.CalledProcessError as e:
        print("Failed to install ollama. Please check your winget installation and try again.")
        print(e)
        exit(1)
    except Exception as e:
        print("An unexpected error occurred while installing ollama.")
        print(e)
        exit(1)

    # Verify ollama installation
    try:
        print("Verifying ollama installation...")
        result = subprocess.run(['ollama', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if result.returncode == 0:
            print("ollama is installed successfully.")
            print(result.stdout.decode())  # Print the version
        else:
            print("ollama installation failed. Please check the error message.")
            print(result.stderr.decode())
            exit(1)
    except FileNotFoundError:
        print("ollama is not installed. Please check your installation.")
        exit(1)
    except Exception as e:
        print("An unexpected error occurred while verifying ollama installation.")
        print(e)
        exit(1)

    # Install ollama python package first to avoid dependency issues
    try:
        print("Installing ollama Python package...")
        pip_cmd = [sys.executable, '-m', 'pip', 'install', 'ollama']
        subprocess.run(pip_cmd, check=True, stdout=subprocess.PIPE, shell=True)
        print("ollama Python package installed successfully.")
    except subprocess.CalledProcessError as e:
        print("Failed to install ollama Python package. Trying alternative method...")
        try:
            subprocess.run(['pip', 'install', 'ollama'], check=True, stdout=subprocess.PIPE, shell=True)
            print("ollama Python package installed successfully with alternative method.")
        except Exception as e2:
            print("Failed to install ollama Python package. Please check your Python installation.")
            print(e2)
            exit(1)
    except Exception as e:
        print("An unexpected error occurred while installing ollama Python package.")
        print(e)
        exit(1)

    # Verify ollama Python package installation
    try:
        print("Verifying ollama Python package installation...")
        import ollama
        print("ollama Python package is installed successfully.")
    except ImportError:
        print("ollama Python package is not installed. Please check your installation.")
        exit(1)
    except Exception as e:
        print("An unexpected error occurred while verifying ollama Python package installation.")
        print(e)
        exit(1)

    # Install llama3.2 small LLM via ollama
    try:
        print("Installing Llama 3.2 small LLM via ollama...")
        subprocess.run(['ollama', 'pull', 'llama3.2:3b'], check=True, shell=True)
        print("Llama 3.2 small LLM installed successfully.")
    except subprocess.CalledProcessError as e:
        print("Failed to install Llama 3.2 small LLM. Please check your ollama installation and try again.")
        print(e)
        exit(1)
    except Exception as e:
        print("An unexpected error occurred while installing Llama 3.2 small LLM.")
        print(e)
        exit(1)

    # Verify Llama 3.2 LLM installation
    try:
        print("Verifying Llama 3.2 LLM installation...")
        result = subprocess.run(['ollama', 'list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        
        if result.returncode == 0:
            output = result.stdout.decode()
            if 'llama3.2:3b' in output or 'llama3.2' in output:
                print("Llama 3.2 LLM is installed successfully.")
                print(output)  # Print the list of installed models
            else:
                print("Llama 3.2 LLM installation failed. Please check the error message.")
                print(output)
                exit(1)
        else:
            print("Failed to verify Llama 3.2 LLM installation.")
            print(result.stderr.decode())
            exit(1)
    except FileNotFoundError:
        print("ollama command not found. Please check your installation.")
        exit(1)
    except Exception as e:
        print("An unexpected error occurred while verifying Llama 3.2 LLM installation.")
        print(e)
        exit(1)


def start_server():
    try:
        print("Starting the ollama server...")
        # Check if ollama server is already running (Windows equivalent)
        ps_result = subprocess.run(['tasklist', '/fi', 'imagename eq ollama.exe'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        if "ollama.exe" in ps_result.stdout.decode():
            print("Ollama server is already running.")
        else:
            subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                shell=True
            )
            print("Ollama server started successfully.")
            print("Waiting for server to initialize...")
            time.sleep(2)
    except Exception as e:
        print("An unexpected error occurred while starting the ollama server.")
        print(e)
        exit(1)

def stop_server():
    """Function to run when the script exits, to clean up resources if needed."""
    try:
        print("Stopping the ollama server...")
        subprocess.run(['taskkill', '/f', '/im', 'ollama.exe'], check=False, shell=True)
        print("Ollama server stopped successfully.")
    except subprocess.CalledProcessError as e:
        print("Failed to stop the ollama server. It may not be running.")
        print(e)
    except Exception as e:
        print("An unexpected error occurred while stopping the ollama server.")
        print(e)

def run_prompt(prompt, model="llama3.2:3b"):
    """
    Run a prompt using the specified Ollama model.
    
    Args:
        prompt (str): The prompt to send to the model
        model (str): The model to use (default: llama3.2:3b)
    
    Returns:
        str: The model's response
    """
    try:
        print(f"Running prompt with model '{model}'...")
        
        response = ollama.chat(model=model, messages=[
            {
                'role': 'user',
                'content': prompt,
            },
        ])
        
        result = response['message']['content']
        return result
        
    except Exception as e:
        error_msg = f"Error running prompt: {e}"
        print(error_msg)
        return error_msg