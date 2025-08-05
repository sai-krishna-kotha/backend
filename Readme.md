# KPA-ERP Backend API Implementation

This document provides the necessary information to set up and understand the backend API developed for the KPA-ERP technical assignment.

---

### Setup Instructions for the Project

To run this backend project locally, please follow these steps.

**Prerequisites:**
* Python 3.8+
* A running instance of PostgreSQL.

**Installation Steps:**

1.  **Clone the Repository:**
    Clone this project to your local machine.
    ```bash
    git clone [your-repo-url]
    cd kpa_backend_assignment
    ```

2.  **Create a Python Virtual Environment:**
    It is recommended to use a virtual environment to manage dependencies.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    Install all the required Python packages using the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Database Configuration:**
    * Ensure your PostgreSQL server is active.
    * Create a new database and a user with access privileges.
    * Create a `.env` file in the root of the project directory by copying the `.env.example` file.
    * Update the `.env` file with your PostgreSQL connection string:
      ```
      DATABASE_URL="postgresql://YOUR_DB_USER:YOUR_DB_PASSWORD@localhost/YOUR_DB_NAME"
      ```

5.  **Run the API Server:**
    Use Uvicorn to run the FastAPI application. The `--reload` flag enables hot-reloading for development.
    ```bash
    uvicorn app.main:app --reload
    ```
    The API will now be running at `http://127.0.0.1:8000`. Interactive documentation (Swagger UI) is available at `http://127.0.0.1:8000/docs`.

---

### The Technologies and Tech Stack Used

* **Backend Language:** Python 3.10
* **API Framework:** FastAPI
* **Database:** PostgreSQL
* **Object-Relational Mapper (ORM):** SQLAlchemy
* **Web Server:** Uvicorn (ASGI)
* **Data Validation:** Pydantic

---

### A List and Description of the Implemented APIs

Two API endpoints were implemented to handle the creation and retrieval of Wheel Specification forms.

#### 1. Create Wheel Specification Form

* **Method:** `POST`
* **URL:** `/api/forms/wheel-specifications`
* **Description:** This endpoint accepts a JSON payload to create a new wheel specification record in the database. It validates the incoming data against a Pydantic schema and returns a success response upon creation.
* **Request Body Example:**
    ```json
    {
      "formNumber": "WHEEL-TEST-001",
      "submittedBy": "user_id_123",
      "submittedDate": "2025-08-05",
      "fields": {
        "treadDiameterNew": "915",
        "lastShopIssueSize": "837",
        "condemningDia": "825",
        ...
      }
    }
    ```
* **Success Response (201 Created):**
    ```json
    {
      "success": true,
      "message": "Wheel specification submitted successfully.",
      "data": {
        "formNumber": "WHEEL-TEST-001",
        "submittedBy": "user_id_123",
        "submittedDate": "2025-08-05",
        "status": "Saved"
      }
    }
    ```

#### 2. Get Wheel Specification Forms

* **Method:** `GET`
* **URL:** `/api/forms/wheel-specifications`
* **Description:** This endpoint retrieves one or more wheel specification records from the database. It supports optional filtering via query parameters.
* **Query Parameters (Optional):**
    * `formNumber` (string)
    * `submittedBy` (string)
    * `submittedDate` (string, in `YYYY-MM-DD` format)
* **Success Response (200 OK):**
    ```json
    {
      "success": true,
      "message": "Filtered wheel specification forms fetched successfully.",
      "data": [
        {
          "formNumber": "WHEEL-TEST-001",
          ...
        }
      ]
    }
    ```

---

### Any Limitations or Assumptions Made

* **Assumption:** It was assumed that the provided Flutter frontend codebase was in a stable, runnable state for integration with the new backend.

* **Limitation & Resolution:** The primary limitation encountered was the stability of the provided frontend environment. Integrating with the codebase required an extensive debugging effort to resolve a series of pre-existing issues before end-to-end functionality could be tested and confirmed.

    Key challenges within the frontend code that were successfully diagnosed and resolved include:
    * Missing Firebase configuration files causing initial build failures.
    * State management providers (`AuthProvider`, `AuthModel`) with hard dependencies on Firebase, leading to runtime crashes.
    * Platform-specific plugins (`permission_handler`) incompatible with the web build target.
    * Application routing logic that prevented navigation to the main screens.
    * Missing image assets and package dependencies (`Gap`) causing silent rendering failures.
    * API connection logic for both `POST` and `GET` requests was absent from the relevant providers and was implemented from scratch to complete the integration.

    After this systematic debugging process, all application-level issues were resolved, resulting in a fully operational frontend that successfully tests both implemented backend APIs.