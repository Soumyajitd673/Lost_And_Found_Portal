# Campus Find – Campus Lost and Found Portal

GitHub Repository: https://github.com/Soumyajitd673/Lost_And_Found_Portal

Campus Find is a web application developed for IIT Bhilai students to report, browse, and recover lost belongings. It provides a centralized platform for lost and found reports, user authentication, item tracking, and administration.

## Features

- User registration and login with OTP verification.
- Report lost and found items with images.
- Browse reported items.
- User profile with lost and found report history.
- Report misleading or inappropriate posts.
- Admin panel to review and resolve reported issues.
- Secure account deletion.

## Technology Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, FastAPI
- **Database:** MySQL
- **ORM:** SQLAlchemy
- **Validation:** Pydantic
- **Server:** Uvicorn

## Prerequisites

- Python installed
- MySQL Server installed and running
- Git

## Installation and Execution

1. Clone the repository:

   ```bash
   git clone <REPOSITORY_URL>
   ```

2. Navigate to the project code root folder:

   ```bash
   cd <PROJECT_FOLDER>
   ```

3. Create a virtual environment:

   ```bash
   py -m venv venv
   ```

4. Activate the virtual environment:

   ```bash
   venv\Scripts\activate
   ```

5. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Create a `.env` file in the project root directory and configure it as described below.

7. Run the following commands one by one:

   **Command 1 – Gmail OAuth Setup (Optional, run only once):**

   ```bash
   py -m backend.service.gmail_oauth_setup
   ```

   This sets up Gmail OAuth for sending OTP emails to users. If this step is skipped, OTPs will be printed in the backend terminal during local testing.

   **Command 2 – Start the Application:**

   ```bash
   uvicorn app:app --reload
   ```

8. Open the application in your browser:

   **http://127.0.0.1:8000**

   API documentation:

   **http://127.0.0.1:8000/docs**

## Environment Variables

Create a `.env` file in the project root directory with the following structure:

```env
# Database Configuration
DB_USER=<mysql_user_name>
DB_PASSWORD=<password>
DB_HOST=localhost
DB_PORT=3306
DB_NAME=FindhubDB

# Session Configuration
SESSION_KEY=your_secret_session_key
```

**Notes:**

- Replace the database placeholders with your MySQL credentials.
- `SESSION_KEY` should contain a strong, randomly generated secret.
- Never commit your `.env` file or expose your credentials publicly.

## Database Setup

1. Start your MySQL server.
2. Ensure that the database credentials in `.env` are correct.

The database and its tables are created automatically when the application starts, so there is no need to create the database manually.