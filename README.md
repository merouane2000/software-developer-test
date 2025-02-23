# Customer Purchase Management System

## Overview

This project is a Customer Purchase Management System that consists of:

1. **Streamlit frontend**  
   - for uploading and analyzing customer purchases.

2. **FastAPI backend**  
   - for handling purchase data and providing APIs.

3. **Docker**  
   - setup for containerizing both the frontend and backend.
   
## Features 

1. **Frontend (Streamlit):**  
   - Upload single or bulk purchases via CSV.
   - Filter purchases by date and country.
   - Display key performance indicators (KPIs) like total purchases,   total amount, and average purchase amount.

2. **Backend (FastAPI):**  
   - RESTful API for adding single or bulk purchases.
   - Filter purchases by country and date.
   - In-memory storage for simplicity (can be replaced with a database)..

3. **Docker**  
   - Containerized frontend and backend for easy deployment.

## Technologies Used
1. **Frontend:**  
   - Streamlit
   - Pandas
   - Requests

2. **Backend:**  
   - FastAPI
   - Pydantic
   - Uvicorn 

3. **Containerization:**  
   - Docker

## Running Locally

1. **Clone the repository:**  
   - `git clone https://github.com/your-username/customer-purchase-management.git`

   - `cd customer-purchase-management`


2. **Set up the backend:**  
   - `cd backend`
   - `pip install -r requirements.txt`
   - `uvicorn main:app --host 0.0.0.0 --port 8000`


3. **Set up the frontend:**  
   - `cd ../frontend`
   - `pip install -r requirements.txt`
   - `streamlit run app.py`

## Testing 
This project includes unit tests for the FastAPI backend to ensure the endpoints behave as expected.
1. **Running the Tests :**
-Navigate to the root directory of the project and run the following command:
-`pytest test_backend.py -v`
or 
- `python -m pytest test_backend.py -v`

## Running Docker

1. **Build the Docker Image Backend:**  
   - `docker build -t fastapi-backend .`
  
2. **Run the Docker Container Backend:**  
 - `docker run -p 8000:8000 fastapi-backend`

1. **Build the Docker Image frontend:**  
   - `docker build -t streamlit-app .`
  
2. **Run the Docker Container Frontend:**  
 - `docker run -p 8501:8501 streamlit-app`
