import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List

# LangChain components
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables from .env file
load_dotenv()

# Check for API Key
if not os.getenv("GOOGLE_API_KEY"):
    raise EnvironmentError("GOOGLE_API_KEY environment variable not found.")

class PatientInfo(BaseModel):
    """Input model for patient data."""
    gender: str = Field(..., description="Patient's gender (e.g., 'male', 'female')")
    age: int = Field(..., gt=0, description="Patient's age, must be a positive integer.")
    symptoms: List[str] = Field(..., min_items=1, description="List of patient's symptoms.")

class RecommendationResponse(BaseModel):
    """Output model for the department recommendation."""
    recommended_department: str

app = FastAPI(
    title="AI Triage Assist API",
    description="Provides a specialist department recommendation based on patient symptoms using an LLM",
    version="1.0.0"
)

# Constrain the LLM just refer departments to this list to prevent hallucinate
VALID_DEPARTMENTS = [
    "Cardiology",
    "Neurology",
    "Orthopedics",
    "Gastroenterology",
    "Pulmonology",
    "Otolaryngology",
    "Dermatology",
    "Ophthalmology",
    "General Surgery",
    "Internal Medicine"
]

# The prompt template
prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert medical triage assistant. Your role is to recommend a hospital department "
            "based on a patient's symptoms, age, and gender. "
            "You must choose ONLY ONE department from the following list: {departments}. "
            "Do not provide any explanation, reasoning, or extra text. Only return the name of the department."
        ),
        (
            "human",
            "Patient Information:\n"
            "- Gender: {gender}\n"
            "- Age: {age}\n"
            "- Symptoms: {symptoms}\n\n"
            "Recommended Department:"
        ),
    ]
)

# Initialize the Google Gemini Pro model via LangChain
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.0)

# The output parser cleans up the LLM's response to a simple string
output_parser = StrOutputParser()

# Create the chain of operations: Prompt -> LLM -> Output Parser
chain = prompt_template | llm | output_parser


@app.post("/recommend", response_model=RecommendationResponse)
async def recommend_department(patient_info: PatientInfo):
    """
    Accepts patient information and returns a recommended specialist department.
    
    This endpoint uses a Large Language Model to analyze the symptoms and suggest
    the most appropriate department for a consultation.
    """
    symptoms_str = ", ".join(patient_info.symptoms)

    try:
        recommendation = await chain.ainvoke({
            "departments": ", ".join(VALID_DEPARTMENTS),
            "gender": patient_info.gender,
            "age": patient_info.age,
            "symptoms": symptoms_str,
        })
        
        if recommendation not in VALID_DEPARTMENTS:
            print(f"Warning: LLM returned an unconstrained value: '{recommendation}'. Defaulting.")
            recommendation = "Internal Medicine" # A safe default

        return RecommendationResponse(recommended_department=recommendation)

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to get recommendation from the AI service. Please try again later."
        )

@app.get("/", include_in_schema=False)
def read_root():
    return {"message": "Welcome to the AI Triage Assist API. Go to /docs for documentation."}