# Panaversity User Management and Authentication

This is a FastAPI project for user management and authentication.

## Setup Instructions
### 1. Clone the Repository

```bash
git clone https://github.com/HamzaNasiem/user_management_and_authentication.git
cd user_management_and_authentication

### 2. Set Up Environment Variables

Create a `.env` file in the root directory of the project and add the following keys with your own values:
DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/<database_name>
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
WHATSAPP_API_KEY=your_whatsapp_api_key
OAUTH_CLIENT_ID=your_oauth_client_id
OAUTH_CLIENT_SECRET=your_oauth_client_secret
OAUTH_REDIRECT_URI=https://yourdomain.com/oauth/callback
OAUTH_SCOPE=email profile
OAUTH_AUTH_URL=https://oauthprovider.com/authorize
OAUTH_TOKEN_URL=https://oauthprovider.com/token

**Note:** Never share your `.env` file or its contents publicly.
### 3. Build and Run the Application Using Docker Compose
```bash
docker-compose up --build

### 4. Access the Application
Open your browser and go to [http://localhost:8000](http://localhost:8000).
The Swagger documentation is available at [http://localhost:8000/docs](http://localhost:8000/docs).

