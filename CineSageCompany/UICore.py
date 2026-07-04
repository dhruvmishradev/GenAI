import os
import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI

# Load environment variables (e.g., MISTRAL_API_KEY)
load_dotenv()

# Set up Streamlit page configuration with a premium look
st.set_page_config(
    page_title="Professional Movie Info Extractor",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Initialize session state variables for input and response
if "paragraph_input" not in st.session_state:
    st.session_state.paragraph_input = ""
if "response_content" not in st.session_state:
    st.session_state.response_content = ""

# Callback function to clear input and response
def clear_all():
    st.session_state.paragraph_input = ""
    st.session_state.response_content = ""

# Custom CSS for a clean, premium, modern appearance
st.markdown(
    """
    <style>
    /* Premium style enhancements */
    .main .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
    }
    h1 {
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    .stTextArea textarea {
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        transition: border-color 0.3s ease;
    }
    .stTextArea textarea:focus {
        border-color: #f75c03; /* Warm orange accent color matching Mistral AI branding */
        box-shadow: 0 0 0 1px #f75c03;
    }
    /* Primary button style */
    div.stButton > button[kind="primary"] {
        background-color: #f75c03 !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 0.5rem 2rem !important;
        font-weight: 600 !important;
        width: 100%;
        transition: transform 0.1s ease, background-color 0.3s ease !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #d94e02 !important;
        transform: translateY(-1px);
    }
    div.stButton > button[kind="primary"]:active {
        transform: translateY(1px);
    }
    /* Secondary button style */
    div.stButton > button[kind="secondary"] {
        background-color: transparent !important;
        color: #666 !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 8px !important;
        padding: 0.5rem 2rem !important;
        font-weight: 600 !important;
        width: 100%;
        transition: all 0.3s ease !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        border-color: #f75c03 !important;
        color: #f75c03 !important;
        background-color: #fff8f5 !important;
    }
    .output-container {
        background-color: #f8f9fa;
        border-left: 5px solid #f75c03;
        padding: 1.5rem;
        border-radius: 8px;
        margin-top: 1.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header Section
st.title("🔍 Professional Movie Information Extraction")
st.write("Extract precise, structured factual information from text without hallucinations.")

# Verification that API key is set
api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    st.warning("⚠️ `MISTRAL_API_KEY` not detected in environment variables or `.env` file. Please ensure it is set.")

# Input Field
paragraph = st.text_area(
    "Paste your paragraph here:",
    key="paragraph_input",
    height=200,
    placeholder="Enter the source text from which you want to extract information...",
)

# Action Buttons
col1, col2 = st.columns([4, 1])
with col1:
    extract_clicked = st.button("Extract Information", type="primary")
with col2:
    st.button("Clear", type="secondary", on_click=clear_all)

# Trigger Action
if extract_clicked:
    if not paragraph.strip():
        st.error("Please enter a paragraph to extract information.")
    elif not api_key:
        st.error("Cannot proceed: MISTRAL_API_KEY is missing. Please set it in your environment or .env file.")
    else:
        with st.spinner("Analyzing text and extracting key information..."):
            try:
                # Initialize model and prompt exactly as specified
                model = ChatMistralAI(
                    model="mistral-small-2506",
                    temperature=0.9
                )

                prompt = ChatPromptTemplate.from_messages(
                    [
                        (
                            "system",
                            """
You are a Professional Information Extraction Assistant.

Your Task:
Extract the most useful and relevant information from the given paragraph and present it in a clean, well-structured format.

Rules:
- Read the entire paragraph carefully.
- Extract ONLY information explicitly mentioned.
- Do NOT hallucinate or assume missing information.
- If any information is unavailable, write "Not Mentioned".
- Keep summaries concise and factual.
- Preserve names, dates, numbers, and titles exactly as written.
- Do NOT add explanations or extra commentary.
- Organize the output with proper headings.
- Use bullet points where appropriate.
"""
                        ),
                        (
                            "human",
                            """
Extract useful information from the following paragraph.

{paragraph}
"""
                        )
                    ]
                )

                final_prompt = prompt.invoke(
                    {
                        "paragraph": paragraph
                    }
                )

                response = model.invoke(final_prompt)
                st.session_state.response_content = response.content
                
            except Exception as e:
                st.error(f"An error occurred during extraction: {e}")

# Display Output if exists
if st.session_state.response_content:
    st.subheader("Results")
    st.markdown(st.session_state.response_content)