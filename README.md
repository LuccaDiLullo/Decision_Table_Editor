# Decision Table Editor 

**Description:** The project focuses on developing a "Decision Table Editor" - a vital tool that assists users in representing and analyzing multiple conditions in a structured format. This allows for clear visual representation of complex decision-making scenarios, ensuring that all possible conditions and their outcomes are meticulously covered. Built using Python, the project emphasizes maintaining code quality, robustness, and user experience. Integrated tools such as Flake8 for linting ensure code adheres to best practices, while Behave enables Gherkin-style testing to verify that the application's functionality aligns with its intended behavior.

## Table of Contents
- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Tools and Their Purpose](#tools-and-their-purpose)
- [Setting up Virtual Environment](#setting-up-virtual-environment)
- [Installation](#installation)
- [Usage](#usage)

## Getting Started
This section provides a brief overview of how to clone the repository and get the project up and running on your local machine.

### Prerequisites
Before you start, make sure you have:
- **Python version 3.x**: Required to run the application. [Download Python here](https://www.python.org/downloads/).
- **Git**: For cloning the repository. [Download Git here](https://git-scm.com/).
- **Virtualenv**: To create a virtual environment for the project. Install using pip:
    ```bash
    pip install virtualenv
    ```

### Tools and Their Purpose
- **Flake8**: A linting tool to enforce code standards and catch potential errors. [Learn more about Flake8](https://flake8.pycqa.org/en/latest/).
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
1. **Running the Linter with Flake8:**
   ```bash
   flake8 .

2. **Running the Application:**
   ```bash
   python ./main.py
