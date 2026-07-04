import os
import json
import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
from pydantic import BaseModel, Field
from typing import List, Optional

# Load dotenv if present
load_dotenv()

# Page configuration for a professional workspace layout
st.set_page_config(
    page_title="CineExtract AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom SaaS-style Premium Minimalist CSS
st.markdown("""
<style>
    /* Import developer fonts */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    /* Global page overrides - Dark mode with subtle ambient lighting gradients */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #040508 !important;
        background-image: 
            radial-gradient(at 0% 0%, rgba(124, 58, 237, 0.03) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(59, 130, 246, 0.03) 0px, transparent 50%) !important;
        color: #9ca3af !important;
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    }
    
    /* Remove default Streamlit top decoration space */
    [data-testid="stHeader"] {
        display: none !important;
    }
    .block-container {
        padding-top: 3.5rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 1200px !important;
    }
    
    /* Sidebar custom styles (File Explorer & Settings) */
    [data-testid="stSidebar"] {
        background-color: #07080c !important;
        border-right: 1px solid rgba(255, 255, 255, 0.03) !important;
        padding-top: 2rem !important;
    }
    
    /* Style the sidebar button entries to look like file explorer tree items */
    [data-testid="stSidebar"] .stButton > button {
        background-color: transparent !important;
        color: #8e94a0 !important;
        border: none !important;
        text-align: left !important;
        justify-content: flex-start !important;
        padding: 8px 12px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.8rem !important;
        width: 100% !important;
        border-radius: 6px !important;
        margin-bottom: 2px !important;
        transition: background-color 0.15s ease, color 0.15s ease;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: rgba(255, 255, 255, 0.02) !important;
        color: #ffffff !important;
    }
    
    /* Style main action button on the workspace with luxury violet-to-blue gradient */
    .main-workspace-col .stButton > button {
        background: linear-gradient(135deg, #7c3aed 0%, #3b82f6 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em !important;
        box-shadow: 0 4px 20px rgba(124, 58, 237, 0.15) !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        text-transform: uppercase;
        width: 100% !important;
    }
    .main-workspace-col .stButton > button:hover {
        box-shadow: 0 6px 24px rgba(124, 58, 237, 0.3) !important;
        transform: translateY(-1px);
    }
    .main-workspace-col .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Input overrides to look unified and minimal */
    div[data-baseweb="textarea"] {
        background-color: #0b0c11 !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px !important;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    div[data-baseweb="textarea"] textarea {
        color: #f3f4f6 !important;
        font-size: 0.9rem !important;
        line-height: 1.55 !important;
    }
    div[data-baseweb="textarea"]:focus-within {
        border-color: rgba(124, 58, 237, 0.4) !important;
        box-shadow: 0 0 0 1px rgba(124, 58, 237, 0.2), inset 0 2px 4px rgba(0, 0, 0, 0.2) !important;
    }

    div[data-baseweb="input"], div[data-baseweb="select"] {
        background-color: #0b0c11 !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="input"] input {
        color: #f3f4f6 !important;
        font-size: 0.85rem !important;
    }
    
    /* Control Row Label overrides */
    label[data-testid="stWidgetLabel"] {
        color: #6b7280 !important;
        font-size: 0.72rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
    }

    /* Tabs Override (Minimalist border style) */
    div[data-baseweb="tab-list"] {
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
        gap: 24px;
        background: transparent !important;
    }
    div[data-baseweb="tab"] {
        background-color: transparent !important;
        color: #6b7280 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        padding: 8px 0px 12px 0px !important;
        border: none !important;
        border-bottom: 2px solid transparent !important;
    }
    div[data-baseweb="tab"][aria-selected="true"] {
        color: #ffffff !important;
        border-bottom: 2px solid #7c3aed !important;
    }

    /* Output Card UI styling - Glassmorphism card */
    .output-card {
        background: rgba(17, 18, 25, 0.45) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
        padding: 32px !important;
        backdrop-filter: blur(12px) !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
    }
    
    .output-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 12px;
        letter-spacing: -0.02em;
    }
    
    .meta-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        padding: 14px 0;
        margin-bottom: 20px;
    }
    
    .meta-col {
        display: flex;
        flex-direction: column;
    }
    
    .meta-lbl {
        font-size: 0.65rem;
        text-transform: uppercase;
        color: #4b5563;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.05em;
        margin-bottom: 2px;
    }
    
    .meta-val {
        font-size: 0.88rem;
        font-weight: 500;
        color: #e5e7eb;
    }

    .output-label {
        font-size: 0.65rem;
        text-transform: uppercase;
        color: #4b5563;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
        display: block;
    }
    
    .summary-text {
        font-size: 0.92rem;
        line-height: 1.6;
        color: #d1d5db;
        margin-bottom: 20px;
    }
    
    .genre-tag {
        display: inline-block;
        background: rgba(124, 58, 237, 0.08);
        border: 1px solid rgba(124, 58, 237, 0.2);
        color: #a78bfa;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        padding: 3px 10px;
        border-radius: 6px;
        margin-right: 8px;
        margin-bottom: 8px;
        font-weight: 500;
    }
    
    .cast-chip {
        display: inline-block;
        background: rgba(255, 255, 255, 0.02);
        color: #d1d5db;
        font-size: 0.8rem;
        padding: 6px 12px;
        border-radius: 6px;
        margin-right: 8px;
        margin-bottom: 8px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Document stat counter under text-area */
    .stat-counter {
        display: flex;
        justify-content: flex-end;
        gap: 16px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: #4b5563;
        margin-top: 4px;
        margin-bottom: 12px;
    }
    
    /* Awaiting Input placeholder design */
    .status-placeholder {
        border: 1px dashed rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        height: 280px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: #4b5563;
        font-size: 0.8rem;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .sidebar-header {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #4b5563;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
        padding-left: 8px;
        font-weight: 600;
    }
    
    .sidebar-brand {
        font-size: 1.25rem;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.02em;
        margin-bottom: 2rem;
        padding-left: 8px;
        text-transform: uppercase;
        background: linear-gradient(135deg, #ffffff 0%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# Pydantic Model for Movie Extraction
class Movie(BaseModel):
    title: str = Field(description="The exact title of the movie.")
    release_year: Optional[int] = Field(description="The year the movie was released, or null if not mentioned.")
    genre: List[str] = Field(description="List of genres associated with the movie.")
    director: Optional[str] = Field(description="Name of the movie director, or null if not mentioned.")
    cast: List[str] = Field(description="List of actors/cast members mentioned in the paragraph.")
    rating: Optional[float] = Field(description="Movie rating, normalized out of 10 if necessary, or null if not mentioned.")
    summary: str = Field(description="A concise summary of the movie's plot/description in 2-3 sentences.")

# Sample Paragraphs
SAMPLES = {
    "interstellar.txt": "Directed by Christopher Nolan, the sci-fi masterpiece Interstellar (2014) stars Matthew McConaughey as Cooper, a former NASA pilot who leads a crew of astronauts through a wormhole in search of a new home for humanity. The film features an incredible cast including Anne Hathaway, Jessica Chastain, and Michael Caine. It currently boasts an impressive rating of 8.7/10. It is a stunning visual and emotional journey about love, time, and human survival.",
    "the_dark_knight.txt": "The Dark Knight is a gritty 2008 superhero action-drama co-written and directed by Christopher Nolan. Based on the DC Comics character Batman, the film is the second installment in The Dark Knight Trilogy. It stars Christian Bale as Bruce Wayne / Batman, alongside Heath Ledger as the iconic Joker, Gary Oldman, Aaron Eckhart, Maggie Gyllenhaal, and Michael Caine. The movie was a critical and commercial triumph, securing a rating of 9.0/10.",
    "spirited_away.txt": "Spirited Away is a breathtaking 2001 Japanese animated fantasy film written and directed by Hayao Miyazaki. The movie tells the story of Chihiro Ogino, a 10-year-old girl who enters the world of spirits. After her parents are turned into pigs, she takes a job working in Yubaba's bathhouse to find a way to free them. Featuring voice acting by Rumi Hiiragi and Miyu Irino, this masterpiece has earned a rating of 8.6/10 globally."
}

# --- LEFT SIDEBAR (Explorer & Settings Panel) ---
with st.sidebar:
    st.markdown('<div class="sidebar-brand">CineExtract</div>', unsafe_allow_html=True)
    
    # Preset Files Section
    st.markdown('<div class="sidebar-header">Source Presets</div>', unsafe_allow_html=True)
    
    if "input_text" not in st.session_state:
        st.session_state.input_text = ""
        
    if st.button("interstellar.txt"):
        st.session_state.input_text = SAMPLES["interstellar.txt"]
        st.rerun()
    if st.button("the_dark_knight.txt"):
        st.session_state.input_text = SAMPLES["the_dark_knight.txt"]
        st.rerun()
    if st.button("spirited_away.txt"):
        st.session_state.input_text = SAMPLES["spirited_away.txt"]
        st.rerun()
    if st.button("clear_buffer.txt"):
        st.session_state.input_text = ""
        st.rerun()
        
    # Parameters Section
    st.markdown('<div class="sidebar-header">Parameters</div>', unsafe_allow_html=True)
    
    env_key = os.getenv("MISTRAL_API_KEY")
    api_key = st.text_input(
        "API Key",
        value=env_key if env_key else "",
        type="password",
        help="Credentials are kept strictly in-memory."
    )
    
    model_name = st.selectbox(
        "Model",
        options=["mistral-small-2506", "mistral-medium-latest", "open-mixtral-8x7b"]
    )
    
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.1,
        step=0.05
    )

# --- MAIN WORKSPACE ---
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="main-workspace-col">', unsafe_allow_html=True)
    st.markdown("<span class=" + '"output-label"' + ">Source Document</span>", unsafe_allow_html=True)
    
    paragraph_input = st.text_area(
        label="Paragraph Input",
        value=st.session_state.input_text,
        height=280,
        label_visibility="collapsed",
        placeholder="Paste movie summary, review, or description script here..."
    )
    
    # Render word/character counters under the textarea
    char_count = len(paragraph_input)
    word_count = len(paragraph_input.split()) if char_count > 0 else 0
    st.markdown(f"""
    <div class="stat-counter">
        <span>WORDS: {word_count}</span>
        <span>CHARS: {char_count}</span>
    </div>
    """, unsafe_allow_html=True)
    
    extract_btn = st.button("RUN EXTRACTOR")
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown("<span class=" + '"output-label"' + ">Structured Output</span>", unsafe_allow_html=True)
    
    if extract_btn:
        if not api_key:
            st.error("Missing Mistral API Key. Please insert your credentials in the control panel.")
        elif not paragraph_input.strip():
            st.warning("Empty source document. Paste text or click a preset file on the left.")
        else:
            with st.spinner("Processing document..."):
                try:
                    # Model setup using modern LangChain structured output framework
                    model = ChatMistralAI(
                        model=model_name,
                        temperature=temperature,
                        api_key=api_key
                    )
                    
                    # Modern with_structured_output handles parsing natively using Mistral API schemas
                    structured_llm = model.with_structured_output(Movie)
                    
                    prompt = ChatPromptTemplate.from_messages([
                        (
                            "system",
                            "Extract structured movie information containing title, release year, genres, director, cast members, rating, and summary from the provided paragraph."
                        ),
                        (
                            "human",
                            "{paragraph}"
                        )
                    ])
                    
                    # Create modern execution chain
                    chain = prompt | structured_llm
                    
                    # Invoke pipeline
                    movie_data: Movie = chain.invoke({"paragraph": paragraph_input})
                    
                    # Modern Visual Layout
                    tab_details, tab_json = st.tabs(["Structured Data", "Raw JSON"])
                    
                    with tab_details:
                        st.markdown(f"""
                        <div class="output-card">
                            <div class="output-title">{movie_data.title}</div>
                            
                            <div style="margin-bottom: 16px;">
                                {" ".join([f'<span class="genre-tag">{g}</span>' for g in movie_data.genre])}
                            </div>
                            
                            <div class="meta-grid">
                                <div class="meta-col">
                                    <div class="meta-lbl">Release Year</div>
                                    <div class="meta-val">{movie_data.release_year if movie_data.release_year else "N/A"}</div>
                                </div>
                                <div class="meta-col">
                                    <div class="meta-lbl">Director</div>
                                    <div class="meta-val">{movie_data.director if movie_data.director else "N/A"}</div>
                                </div>
                                <div class="meta-col">
                                    <div class="meta-lbl">IMDb Rating</div>
                                    <div class="meta-val">{movie_data.rating if movie_data.rating else "N/A"} / 10</div>
                                </div>
                            </div>
                            
                            <div>
                                <span class="output-label">Plot Summary</span>
                                <div class="summary-text">{movie_data.summary}</div>
                            </div>
                            
                            <div>
                                <span class="output-label">Cast Members</span>
                                <div style="margin-top: 6px;">
                                    {"".join([f'<span class="cast-chip">{actor}</span>' for actor in movie_data.cast]) if movie_data.cast else '<span style="color: #4b5563">No cast members extracted</span>'}
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    with tab_json:
                        # Print beautiful formatted, copyable JSON using standard stream code block
                        json_str = json.dumps(movie_data.model_dump(), indent=2)
                        st.code(json_str, language="json")
                        
                except Exception as e:
                    st.error(f"Extraction failed: {str(e)}")
                    st.info("Ensure that the model can connect using the provided API key.")
    else:
        st.markdown("""
        <div class="status-placeholder">
            <div>awaiting_workspace_compilation</div>
        </div>
        """, unsafe_allow_html=True)