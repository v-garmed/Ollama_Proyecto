import streamlit as st
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from productos import productos
import re

# ----- Información base -----
from infonegocio import info


st.set_page_config(page_title="Fútbol de Hermanos", layout="wide")
st.title("🏆 Futbol de Hermanos")
st.write("Fútbol de Hermanos, más que una tienda, una pasión por el deporte.")


# Imagen/logo en la barra lateral (opcional)
st.sidebar.image("images/Logo FUTBOL DE HERMANOS.jpg", use_container_width=True)  # Cambia por tu logo si tienes

# Título o mensaje de bienvenida
st.sidebar.title("Fútbol de Hermanos")

# Opcional: Información de contacto
st.sidebar.markdown("📍 *Guadalajara, Jalisco*")
st.sidebar.markdown("📞 +52 55 1234 5678")
st.sidebar.markdown("📧 futboldehermanos@gmail.com")
st.sidebar.markdown("🌐 [Sitio Web](https://futboldehermanos.com)")



# ----- Función para buscar productos -----
def buscar_producto(mensaje):
    mensaje = mensaje.lower()
    encontrados = []
    for producto in productos:
        if any(alias in mensaje for alias in producto["alias"]):
            encontrados.append(producto)
    return encontrados

# ----- Estado inicial -----
if "messages" not in st.session_state:
    st.session_state.messages = []

if "first_message" not in st.session_state:
    st.session_state.first_message = True

# ----- Mostrar historial de chat -----
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ----- Primera respuesta del bot -----
if st.session_state.first_message:
    saludo = "Hola, te saluda tu asistente de venta BOTin 🤖⚽. ¿Cómo puedo ayudarte hoy?"
    with st.chat_message("assistant"):
        st.markdown(saludo)
    st.session_state.messages.append({"role": "assistant", "content": saludo})
    st.session_state.first_message = False

# ----- Configurar modelo LLaMA -----
if "ollama" not in st.session_state:
    template = """
    Responde la siguiente pregunta en español.

    Aquí está el contexto del negocio: 
    {infonegocio}

    {context}

    Pregunta: {question}

    Respuesta:
    """
    model = OllamaLLM(model="llama3.1")
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    context = ""

# ----- Entrada del usuario -----
if user_input := st.chat_input("Escribe tu pregunta aquí..."):
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    result = chain.invoke({
        "infonegocio": info,
        "context": context,
        "question": user_input
    })

    # Buscar productos relacionados
    productos_encontrados = buscar_producto(user_input)

    with st.chat_message("assistant"):
        st.markdown(result)
        for producto in productos_encontrados:
            st.image(producto["imagen"], use_column_width=True)
            st.markdown(f"### {producto['nombre']}")
            st.markdown(f"💵 **Precio:** {producto['precio']}")
            st.markdown(f"📌 **Tallas disponibles:** {producto['tallas']}")
            with st.expander("🧵 Ver características"):
                st.markdown(producto["caracteristicas"])

    st.session_state.messages.append({
        "role": "assistant",
        "content": result
    })

    context += f"Tú: {user_input}\nBot: {result}\n"
