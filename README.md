# RouteRover

## Introduction
RouteRover is a web application for optimizing and visualizing routes between two points based on mode of travel.

## Features

- Calculate the shortest route between two locations.
- Visualize the optimized route on a map.
- User-friendly web interface.

## Getting started

These instructions will help you set up and run the RouteRover app on your local machine.

### Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed.
- PostgreSQL, PostGIS, pgRouting set up with the necessary data.
- Flask and required Python packages installed. You can install them using `pip`:

### Installation

1. Clone the RouteRover repository

```bash
git clone https://github.com/sotieno/RouteRover.git
cd RouteRover
```

2. Create a virtual environment

```bash
python3 -m venv virtualenv

# activate virtual environment
source virtualenv/bin/activate # For Linux
source virtualenv/scripts/activate # For Windows

# install required packages
pip install -r requirements.txt
```

3. Configure your database connection by modifying 'config.py' with your database parameters.
4. Create and populate the necessary database tables
5. Create the flask application factory by running the following commands to run the application:

```bash
export FLASK_APP=core
export FLASK_ENV=development
flask run
```

## Usage

1. Open your web browser and go to http://localhost:5000/main/.
2. 'Register' or 'Login' to access 'Get Route' function.
3. Enter the starting point, destination and mode of travel in the input form and click the "Find Route" button.
4. The shortest route will be displayed on the map along with markers for the starting and ending points.

## Contributing
I welcome contributions from the community. If you would like to contribute to RouteRover, please follow these guidelines:

* Fork the repository.
* Create a new branch: git checkout -b feature/your-feature
* Make your changes and commit them: git commit -m 'Add feature'
* Push to the branch: git push origin feature/your-feature
* Create a pull request to the main repository

## Contact

Sylvia Otieno - [Github](https://github.com/sotieno) / [Twitter](https://twitter.com/sotienos)
