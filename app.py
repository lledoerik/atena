import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

# === INITIAL CONFIGURATION ===
st.set_page_config(page_title="Atena", page_icon="🦉")

# === SIDEBAR CONFIGURATION ===
st.sidebar.title("⚙️ Configuració")

# Temperature control
st.sidebar.markdown("---")
temperature = st.sidebar.slider(
    "Temperatura",
    min_value=0.0,
    max_value=2.0,
    value=0.7,
    step=0.1,
    help="Més alt = més creativitat"
)

# Model selector
selected_model = st.sidebar.selectbox(
    "Model",
    ["gemini-2.5-flash", "gemini-pro", "gemini-1.5-flash"],
    index=0
)

# System prompt customization
system_prompt = st.sidebar.selectbox(
    "Triar personalitat",
    [
        "Assistent normal",
        "Professor de programació",
        "Entrenador de voleibol",
        "Expert en mitologia",
        "Personalitzat"
    ],
    index=0
)

# If custom is selected, show text area
custom_prompt = ""
if system_prompt == "Personalitzat":
    custom_prompt = st.sidebar.text_area(
        "Escriu el teu prompt:",
        placeholder="Ets un expert en...",
        height=100
    )

# Clear conversation button
st.sidebar.markdown("---")
if st.sidebar.button("🗑️ Netejar conversa", type="secondary"):
    st.session_state.messages = []
    st.rerun()

# === MAIN APPLICATION ===
st.title("🦉 Atena")
st.markdown("*Deessa de la saviesa, la guerra i els oficis.*")

# Create dynamic model
chat_model = ChatGoogleGenerativeAI(
    model=selected_model,
    temperature=temperature
)

# Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render existing history
for msg in st.session_state.messages:
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)

# User input
question = st.chat_input("Escriu el teu missatge:")

if question:
    # Display and store user message
    with st.chat_message("user"):
        st.markdown(question)

    st.session_state.messages.append(HumanMessage(content=question))

    # Define system prompts
    defined_prompts = {
        "Assistent normal": "",
        "Professor de programació": "Ets un professor de programació expert. Explica conceptes de forma clara i amb exemples pràctics.",
        "Entrenador de voleibol": "Ets un entrenador de voleibol amb molta experiència. Dona consells tècnics, tàctics i motivacionals sobre voleibol. Explica jugades, tècniques i estratègies.",
        "Expert en mitologia": "Ets un expert historiador especialitzat en mitologia grega. Explica mites, llegendes, déus i herois grecs amb detall i passió. Connecta les històries amb la cultura antiga.",
        "Personalitzat": custom_prompt
    }

    # Apply system prompt
    current_prompt = defined_prompts[system_prompt]
    messages_with_system = st.session_state.messages.copy()

    if current_prompt:
        # Add system prompt at the beginning
        messages_with_system.insert(0, SystemMessage(content=current_prompt))

    response = chat_model.invoke(messages_with_system)

    with st.chat_message("assistant"):
        st.markdown(response.content)

    st.session_state.messages.append(response)