import streamlit as st
from altair.vegalite.v5.display import olli_renderer
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

# Header
st.set_page_config(page_title="Atena", page_icon="🦉")

# Menu configuración
st.sidebar.header("⚙️ Configuració")
st.sidebar.markdown("---")

# Control de temperatura
temperatura = st.sidebar.slider(
    "Temperatura",
    min_value=0.0,
    max_value=2.0,
    value=0.7,
    step=0.1,
    help="Més alt = més creativitat"
)

# Selector de modelo
modelo_elegido = st.sidebar.selectbox(
    "Model",
    ["gemini-2.5-flash", "gemini-pro", "gemini-1.5-flash", ],
    index=0
)

# Botón para limpiar chat
st.sidebar.markdown("---")
if st.sidebar.button("Netejar conversa"):
    st.session_state.mensajes = []
    st.rerun()

# Modelo dinámico
chat_model = ChatGoogleGenerativeAI(
    model=modelo_elegido,
    temperature=temperatura
)

# Configuración inicial
st.title("Atena")
st.markdown("Deessa de la saviesa, la guerra i els oficis.")

chat_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Inicializar el historial de mensajes en session_state
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Renderizar historial existente
for msg in st.session_state.mensajes:
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)

# Memoria entre returns
if "temperatura" not in st.session_state:
    st.session_state.temperatura = 0.7

# Acceso a la memoria
print(st.session_state.temperatura)

# Input de usuario
pregunta = st.chat_input("Escribe tu mensaje:")

if pregunta:
    # Mostrar y almacenar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(pregunta)

    st.session_state.mensajes.append(HumanMessage(content=pregunta))

    respuesta = chat_model.invoke(st.session_state.mensajes)

    with st.chat_message("assistant"):
        st.markdown(respuesta.content)

    st.session_state.mensajes.append(respuesta)