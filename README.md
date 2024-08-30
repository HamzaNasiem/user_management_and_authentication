# Panaversity User Management and Authentication

This is a FastAPI project for user management and authentication.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/HamzaNasiem/user_management_and_authentication
cd user_management_and_authentication

### 2. Set Up Environment Variables


#### Create a.env file in the root directory with the following content:
DATABASE_URL=postgresql://<username>:<password>@PostgresCont:5432/<database_name>
SECRET_KEY=your_secret_key
WHATSAPP_API_KEY=your_whatsapp_api_key
OAUTH_CLIENT_ID=your_oauth_client_id
OAUTH_CLIENT_SECRET=your_oauth_client_secret

#### 3. Build and Run the Application Using Docker Compose

```docker-compose up --build```

### 4. Access the Application

Open your browser and go to http://localhost:8000.
API documentation is available at http://localhost:8000/docs.
