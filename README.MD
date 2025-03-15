# Smart Dollar

## Description
This project is designed to be the backend, API and DateBase of Smart Dollar. It aims to have simple deployment steps.

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
    cd yourproject
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
.\scripts\activate-windows.bat
```

#### For macOS/Linux
```bash
source scripts/activate-unix.sh
```
5. Install the dependencies:
    ```bash
    pip install -r requirements.txt 
    ```


## Usage
Start the api server:
```bash
uvicorn main:app --reload
```

open http://localhost:8000/docs to see the api dashboard.
