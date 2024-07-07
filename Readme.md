### Analytics Backend - User Data Management API

- This project provides a Django REST API for user registration, login, and data management functionalities.

### Please note: Due to server optimization, the backend response time might be slightly longer (up to 1 minute) on the initial application load. This is because the backend server spins down during periods of inactivity. Subsequent requests will experience faster response times.

## Features:

# User Authentication:

- Register new users with username, email, and password.
- Login existing users for secure access to protected endpoints.

# Data Management:

- Upload CSV data (link) to the database (protected route).
- Perform various queries on uploaded data (protected route):
- Exact match on numerical columns.
- Substring match on string columns.
- Aggregate functions (min, max, mean) on numerical columns.
- Less than and greater than comparisons on date columns.
- Retrieve all uploaded data (optional for data validation).

# Technology Stack:

- Backend: Django
- Database: SQLite (default, in-house)

# Frontend Integration:

- The Frontend for this Backend is hosted at: https://analytics-frontend-mq5e.onrender.com

* Frontend code repo: https://github.com/UP11SRE/analytics-frontend.git

# Render:

- A deployed instance is also available at: https://analytics-backend-odh4.onrender.com

# Deployment Options:

- Docker:

* Pull the pre-built image from Docker Hub:

* docker pull raja110199/analytics-backend:latest

* Run the container locally:

* docker run -p 8000:8000 raja110199/analytics-backend:latest

# API Usage:

# Authentication:

# Register users:

- POST request to /api/register with a JSON body containing username, email, and password.
- Login users:
- POST request to /api/login with a JSON body containing username and password.
- Upon successful login, a token will be returned in the response. Use this token for authorization in subsequent requests.

# Data Management:

- Authorization:

- All data management endpoints (/api/upload and /api/get_data) require authorization via the token obtained from login.
- Include the token in the request header as Authorization: Token <your_token>.

# Upload Data:

- POST request to /api/upload with a JSON body containing:
- csv_file: Link to the CSV spreadsheet.
- and token in the header

# Query Data:

- POST request to /api/get_data with a JSON body containing query parameters. Refer to the detailed documentation below for specific query formats.

# Query Documentation:

- Exact Match:

* Parameter: Column Name (e.g., AppID)
* Value: Value (e.g., 20220)
* parameter: query_type , value : "Exact"
* Example:

JSON
{
"column": "AppID",
"value": "20220",
"query_type": "exact"
}

This query retrieves rows where the AppID column exactly matches the value 20220.

- Substring Match (String Columns):

* Parameter Type: Column Name (e.g., Product Name)
* Value Type: Value (e.g., "Jolt") - Enclose the text in double quotes
* parameter: query_type , value: "String"

Example:

JSON
{
"column": "Product Name",
"value": "\"Jolt\"",
"query_type": "string"
}

- This query returns rows where the Product Name column contains the exact term "Jolt" (case-sensitive).

* Aggregate Queries (min, max, mean):

- Parameter Type: Choose "min", "max", or "mean" from the dropdown
- Value Type: Column Name (e.g., Price)
- parameter: query_type , value: "Aggregate"

Example:

JSON
{
"column": "Price",
"query_type": "min"
}

- This query calculates the minimum value present in the Price column.

* Date-Based Queries (less than, greater than):

- Parameter Type: Column Name (e.g., Release_date)
- Value Type: Date (e.g., oct 21, 2008)
- parameter: query_type , value: "lessthan" or "greaterthan"

Example:

JSON
{
"column Name": "Release_date
"value": "21-10-2008"
"query_type": "lessthan or greaterthan"

}

- This query retrieves rows where the Release_date column has values earlier than "2024-07-10".

# Important Notes:

- For column names containing spaces (e.g., "Release Date"), enter them using underscores instead (e.g., "Release_Date"). This ensures proper query interpretation.
- Currently supported aggregate functions are min, max, and mean.
- Date comparisons are restricted to date columns.

## Project Overview Video

- For a visual explanation of this project, you can view a video walkthrough here: https://www.loom.com/share/5d9f22d342d04422b7387ccd65d783c8?sid=04541838-ed7f-4207-a9d9-7c07c6c54e60

## cost of running your system in production 24x7 for 30 days, assuming one file upload and 100 queries a day.

- If you want a super reliable system, you can turn to AWS.
  If you take a micro server for the application, rds for the database and additional disk space for it, add S3 Storage, along with some traffic fees, you can get $25-30. And you will have to optimize the code a bit for this.

- Or there is a normal option that works: Rent a VPS that is a little better than the minimum, which will be enough for everything and will cost $5-10 per month. Maybe 15$, if the hosting provider is expensive.

# Contribution

- This project is not currently open for external contributions.

# License

- This project is licensed under the MIT License.
