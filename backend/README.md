# EcoDrive-Backend

EcoDrive-Backend is an efficient FastAPI application designed to manage various functionalities like rides, recommendations, redeemables, and more.

## Table of Contents

- [EcoDrive-Backend](#ecodrive-backend)
  - [Table of Contents](#table-of-contents)
  - [Project Structure](#project-structure)
  - [Setup and Running](#setup-and-running)
  - [🐋 Docker support](#-docker-support)
    - [Environment Variables](#environment-variables)
  - [API Endpoints](#api-endpoints)
  - [Database Models](#database-models)

## Project Structure

The project structure is organized as follows:

```plaintext
.
├── app
│   ├── main.py                           # Main application runner
│   └── server
│       ├── app.py
│       ├── config.py                     # General Configuration
│       ├── database                      # Database CRUD operations
│       │   ├── ...
│       ├── dependencies.py               # API Dependencies
│       ├── models                        # Pydantic Models for API
│       │   ├── ...
│       ├── routes                        # API Endpoints/Routes
│       │   ├── ...
│       └── utils.py                      # Utilities
├── requirements.txt                      # Python dependencies
├── static                                # Static assets
│   ├── icons
│   ├── recommendations
│   └── redeemables
├── tests
│   └── api_auth_test.py                  # Authentication Tests
└── triggers
    ├── recommendations.json              # Recommendation triggers
    ├── recommendations.py
    ├── redeemable.json                   # Redeemable triggers
    ├── redeemable.py
    ├── vehicles.json                     # Vehicle triggers
    └── vehicles.py
```

## Setup and Running

To set up and run the project locally, use the following steps:

1. Set up a virtual environment:

```bash
python3 -m venv venv
```

2. Activate the virtual environment:

```bash
source ./venv/bin/activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python app/main.py
```

## 🐋 Docker support

You can also run the service with this command:

```sh
cp .env.example .env
# Make sure to edit the .env file properly
docker-compose up -d
```

This will start the FastAPI application and it should be accessible on [`http://localhost:8000/`](http://localhost:8000/docs).

### Environment Variables

The application uses environment variables for configuration. An example `.env` file is provided as `.env.example` in the root directory. Before running the application, make a copy of this file, rename it to `.env`, and fill in the appropriate values.

```plaintext
MONGO_URL="mongodb://<USER>:<PASSWORD>@<HOST>:<PORT>/?authMechanism=DEFAULT"  # MongoDB Connection URL
SECRET_KEY="<YOUR_SECRET_KEY>"   # Secret key for encoding and decoding JWT tokens
PORT=8000                       # The port on which the FastAPI application will run
ACCESS_TOKEN_EXPIRE_MINUTES=30  # Token expiration time in minutes
PROJECT_ENVIRONMENT="DEVELOPMENT" # Use "DEVELOPMENT" for development mode or "RELEASE" for release mode
```

## API Endpoints

The application's functionalities are divided into different modules such as rides, recommendations, redeemables, and more. Each module has its own set of routes. Here are some examples:

- **Rides**: Manage and log rides. Users earn points based on their rides.
  - Routes can be found in `app/server/routes/ride.py`.
  
- **Recommendations**: Provide eco-friendly recommendations to users.
  - Routes can be found in `app/server/routes/recommendation.py`.
  
- **Redeemables**: Items or services that users can redeem using their earned points.
  - Routes can be found in `app/server/routes/redeemable.py`.

## Database Models

The application uses database models defined using Pydantic. These models can be found under the `app/server/models` directory. Each module (rides, recommendations, redeemables, etc.) has its own model.

For example, the Ride model is defined in `app/server/models/ride.py` and it contains attributes like user_id, distance, points_obtained, etc.
