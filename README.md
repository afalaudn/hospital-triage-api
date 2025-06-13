# AI Triage Assist API V.1.0

A minimal FastAPI service that recommends a hospital specialist department based on patient symptoms, age, and gender. The service uses Google's Gemini Pro LLM via LangChain for the recommendation logic.

## Prerequisites

Before you begin, ensure you have the following installed:
*   [Git](https://git-scm.com/)
*   [Conda](https://docs.conda.io/en/latest/miniconda.html) (or Miniconda)

## 1. Setup and Installation

Follow these steps to set up your local development environment.

### Step 1: Clone the Repository

```bash
git clone <https://github.com/afalaudn/hospital-triage-api.git>
cd hospital-triage-api
```

### Step 2: Create and Activate the Conda Environment

This will create a new Conda environment named `triage-api-env` using the provided file and install all necessary dependencies.

```bash
# Create the environment from the file
conda env create -f environment.yml

# Activate the environment
conda activate triage-api-env
```
*(**Alternative using pip/venv:** If you don't use Conda, you can create a virtual environment and use `pip install -r requirements.txt`)*

### Step 3: Configure Your API Key

The application requires a Google AI Studio API key to function.

1.  Create a new file named `.env` in the project's root directory.
2.  Add your API key to the file. Get your key from [Google AI Studio](https://aistudio.google.com/).

```plaintext
# .env
GOOGLE_API_KEY="YOUR_GOOGLE_AI_STUDIO_API_KEY"
```

## 2. Running the Application

With the environment activated, start the FastAPI development server using Uvicorn.

```bash
uvicorn main:app --reload
```
The server will be running at `http://127.0.0.1:8000`. The `--reload` flag automatically restarts the server when code changes are detected.

## 3. How to Test

You can test the API in two primary ways:

### A) Using the Interactive API Docs (Swagger UI)

Navigate to **`http://127.0.0.1:8000/docs`** in your web browser. You can test the `/recommend` endpoint directly from the documentation page.

### B) Using `curl`

Open a new terminal and run the following `curl` command to send a `POST` request to the endpoint.

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/recommend' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "gender": "female",
  "age": 62,
  "symptoms": ["pusing", "mual", "sulit berjalan"]
}'
```

#### Expected Response:

```json
{
  "recommended_department": "Neurology"
}
```