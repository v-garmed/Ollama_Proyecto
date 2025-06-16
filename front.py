# Importa la librería Streamlit para crear la interfaz web
import streamlit as st
# Importa el modelo OllamaLLM de langchain_ollama para procesamiento de lenguaje natural
from langchain_ollama import OllamaLLM
# Importa la plantilla de prompts para chat de langchain_core
from langchain_core.prompts import ChatPromptTemplate
# Importa la lista de productos desde el archivo productos.py
from productos import productos
# Importa la librería de expresiones regulares (no se usa en este código)
import re

# Importa la información del negocio desde infonegocio.py
from infonegocio import info

# Configura la página de Streamlit (título y diseño)
st.set_page_config(page_title="Fútbol de Hermanos", layout="wide")
# Muestra el título principal en la página
st.title("🏆 Futbol de Hermanos")
# Muestra una breve descripción debajo del título
st.write("Fútbol de Hermanos, más que una tienda, una pasión por el deporte.")

# Muestra el logo en la barra lateral
st.sidebar.image("images/Logo FUTBOL DE HERMANOS.jpg", use_container_width=True)
# Título en la barra lateral
st.sidebar.title("Fútbol de Hermanos")
# Información de contacto en la barra lateral
st.sidebar.markdown("📍 *Guadalajara, Jalisco*")
st.sidebar.markdown("📞 +52 55 1234 5678")
st.sidebar.markdown("📧 futboldehermanos@gmail.com")
st.sidebar.markdown("🌐 [Sitio Web](https://futboldehermanos.com)")

# Función para buscar productos que coincidan con el mensaje del usuario
def buscar_producto(mensaje):
    mensaje = mensaje.lower()  # Convierte el mensaje a minúsculas
    encontrados = []  # Lista para productos encontrados
    for producto in productos:  # Recorre todos los productos
        # Si algún alias del producto está en el mensaje, lo agrega a la lista
        if any(alias in mensaje for alias in producto["alias"]):
            encontrados.append(producto)
    return encontrados  # Devuelve la lista de productos encontrados

# Inicializa el historial de mensajes si no existe en la sesión
if "messages" not in st.session_state:
    st.session_state.messages = []

# Inicializa el indicador de primer mensaje si no existe en la sesión
if "first_message" not in st.session_state:
    st.session_state.first_message = True

# Muestra el historial de chat almacenado en la sesión
for message in st.session_state.messages:
    with st.chat_message(message["role"]):  # Muestra el mensaje según el rol (usuario o asistente)
        st.markdown(message["content"])

# Si es la primera vez que se carga la página, muestra el saludo inicial del bot
if st.session_state.first_message:
    saludo = "Hola, te saluda tu asistente de venta BOTin 🤖⚽. ¿Cómo puedo ayudarte hoy?"
    with st.chat_message("assistant"):
        st.markdown(saludo)
    st.session_state.messages.append({"role": "assistant", "content": saludo})
    st.session_state.first_message = False  # Marca que ya no es el primer mensaje

# Configura el modelo LLaMA y la cadena de procesamiento si no existe en la sesión
if "ollama" not in st.session_state:
    # Plantilla para el prompt que se enviará al modelo
    template = """
    Responde la siguiente pregunta en español.

    Aquí está el contexto del negocio: 
    {infonegocio}

    {context}

    Pregunta: {question}

    Respuesta:
    """
    # Inicializa el modelo OllamaLLM con el modelo llama3.1
    model = OllamaLLM(model="llama3.1")
    # Crea el prompt a partir de la plantilla
    prompt = ChatPromptTemplate.from_template(template)
    # Crea la cadena de procesamiento combinando prompt y modelo
    chain = prompt | model
    # Inicializa el contexto como cadena vacía
    context = ""

# Captura la entrada del usuario desde el chat
if user_input := st.chat_input("Escribe tu pregunta aquí..."):
    # Muestra el mensaje del usuario en el chat
    with st.chat_message("user"):
        st.markdown(user_input)

    # Agrega el mensaje del usuario al historial de mensajes
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Invoca el modelo con el contexto, la información del negocio y la pregunta del usuario
    result = chain.invoke({
        "infonegocio": info,
        "context": context,
        "question": user_input
    })

    # Busca productos relacionados con la pregunta del usuario
    productos_encontrados = buscar_producto(user_input)

    # Muestra la respuesta del asistente y los productos encontrados
    with st.chat_message("assistant"):
        st.markdown(result)
        for producto in productos_encontrados:
            st.image(producto["imagen"], use_column_width=True)
            st.markdown(f"### {producto['nombre']}")
            st.markdown(f"💵 **Precio:** {producto['precio']}")
            st.markdown(f"📌 **Tallas disponibles:** {producto['tallas']}")
            with st.expander("🧵 Ver características"):
                st.markdown(producto["caracteristicas"])

    # Agrega la respuesta del asistente al historial de mensajes
    st.session_state.messages.append({
        "role": "assistant",
        "content": result
    })

    # Actualiza el contexto con la última interacción
    context += f"Tú: {user_input}\nBot: {result}\n"
