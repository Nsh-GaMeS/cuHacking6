# Smart Dollar

## Description
Smart Dollar is an intelligent finance tracker designed to help you set and achieve SMART (Specific, Measurable, Achievable, Relevant, and Time-Bound) financial goals. With personalized AI-driven insights, Smart Dollar optimizes your savings strategy, making it easier and more efficient to reach your financial targets faster. 🚀💰

This repository is designed to be the backend, API and DateBase of Smart Dollar. It aims to have simple deployment steps to work along with the UI.
Check out the UI project for Smart Dollar [here](https://github.com/Nsh-GaMeS/Smart-Dollar-UI)
## Getting Started

### Prerequisites
Make sure you have the following installed:
- python 3.10
- visual studio code
- git

### Installation
Follow these steps to set up the project:
1. Clone the repository:
    ```bash
    git clone https://github.com/Nsh-GaMeS/cuHacking6.git
    ```
2. Navigate to the project directory:
    ```bash
    cd cuHacking6
    ```
3. Create a virtual environment:
    ```bash
    python -m venv venv
    ```

4. Activate virtual environment:    
    ### Activation Scripts
    To activate the project, use the following scripts:

    #### For Windows
    ```bash
    .\scripts\activate-windows.ps1
    ```

    #### For macOS/Linux
    ```bash
    source ./venv/bin/activate
    ```
5. Install the dependencies:
    ```bash
    pip install -r requirements.txt 
    ```


## Usage
1. Start the api server:
```bash
uvicorn main:app --reload
```

open http://localhost:8000/docs to see the api dashboard.

2. run the api through ngrok to make it public:
```bash
ngrok http 8000
```
> **Note:** This has to run in a terminal session after running the api server(step 1). Since by default the api server runs on port 8000, the ngrok command will expose the api server to the internet.

> **Note:** Note the ngrok link that is generated. Thats the public link to the api server.
