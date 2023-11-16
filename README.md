# Decision Table Editor

**Description:** The project focuses on developing a "Decision Table Editor" - a tool that assists users in representing and analyzing multiple conditions in a structured format. This allows for a clear visual representation of complex decision-making scenarios, enabling all possible conditions and their outcomes to be meticulously covered. Built using Python, the project emphasizes maintaining code quality, robustness, and ease of use.

## Table of Contents
- [Getting Started](#getting-started)
- [Usage](#usage)

## Getting Started
This section provides a brief overview of how to download and run the Decision Table Editor on your local machine.

### Download the Application
1. Go to the [Releases](https://github.com/LuccaDiLullo/Decision_Table_Editor/releases) section of this repository.

2. Download the appropriate executable for your operating system.

### Usage
1. **Running the Application:**
   - For Windows, double-click on the downloaded `.exe` file.
   - For Mac, double-click on the downloaded executable file.
  
----------------------------------------------------------------------------------------------------------------------------------------
  
# In case of Executable not Working

## Table of Contents
- [Prerequisites](#prerequisites)
- [Tools and Their Purpose](#tools-and-their-purpose)
- [Setting up Virtual Environment](#setting-up-virtual-environment)
- [Installation](#installation)
- [Usage](#usage)

### Prerequisites
Before you start, make sure you have:
- **Python version 3.x**: Required to run the application. [Download Python here](https://www.python.org/downloads/).
- **Git**: For cloning the repository. [Download Git here](https://git-scm.com/).
- **Virtualenv**: To create a virtual environment for the project. Install using pip:
    ```bash
    pip install virtualenv
    ```

### Tools and Their Purpose
- **Behave**: A tool for writing tests in the Gherkin language to ensure functionality aligns with intended behavior. [Learn more about Behave](https://behave.readthedocs.io/en/stable/).
- **PyWebIO**: Used for building web applications with Python. [Learn more about PyWebIO](https://pywebio.readthedocs.io/en/latest/).

### Setting up Virtual Environment
1. **Create a virtual environment:**
    ```bash
    virtualenv venv
    ```

2. **Activate the virtual environment:**
    - On Windows:
      ```bash
      .\venv\Scripts\activate
      ```
    - On macOS and Linux:
      ```bash
      source venv/bin/activate
      ```

### Installation
1. **Clone the Repository:**
    ```bash
    git clone https://github.com/LuccaDiLullo/Decision_Table_Editor
    ```

2. **Navigate to the project directory:**
    ```bash
    cd Decision_Table_Editor
    ```

3. **Install Necessary Dependencies inside the virtual environment:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. **Running the Application:**
   ```bash
   python ./main.py
