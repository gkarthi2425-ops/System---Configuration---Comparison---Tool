# System Configuration Comparison Tool

## Project Description

The System Configuration Comparison Tool is a Python-based GUI application that retrieves computer system information and compares it with a previously saved system configuration.

## Features

* Retrieve system information
* Display CPU information
* Display RAM information
* Display disk information
* Display operating system information
* Save system configuration
* Load saved configuration
* Compare two system configurations
* Show whether system parameters are the same or different

## Technologies Used

* Python
* Tkinter
* psutil
* JSON

## Requirements

Python 3.x

Install the required package using:

```bash
pip install psutil
```

## How to Run

1. Download or clone this repository.
2. Open the project folder in VS Code.
3. Open the terminal.
4. Install the required package:

```bash
pip install -r requirements.txt
```

5. Run the application:

```bash
python app.py
```

## Project Structure

```text
System-Configuration-Comparison/
│
├── app.py
├── requirements.txt
└── README.md
```

## Working

The application collects system information using the `psutil`, `platform`, and `socket` modules. The retrieved configuration can be saved as a JSON file and later compared with the current system configuration.

## Author

LPU B.Tech CSE Student
