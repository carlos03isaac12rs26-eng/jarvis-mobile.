import streamlit as st
from google import genai

# Configuración de la página móvil
st.set_page_config(
    page_title="JARVIS Mobile",
    page_icon="🤖",
    layout="centered"
)

# Estilo visual futurista
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #00ffcc;
    }
    </style>
""", unsafe_allow_html=True)

st.title("J.A.R.V.I.S. v1.0")
st.write("Sistemas en línea. A su servicio, Señor.")

# Configurar API Key en la barra lateral
api_key = st.sidebar.text_input("API Key de Google Gemini", type="password")

if not api_key:
    st.warning("Por favor, ingrese su API Key de Gemini en la barra lateral para iniciar los sistemas.")
else:
    # Inicializar el cliente oficial de Google GenAI
    client = genai.Client(api_key=api_key)

    # Inicializar el historial de conversación en el formato nativo de Gemini
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostrar mensajes previos en pantalla
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Caja de entrada para hablar con el asistente
    if prompt := st.chat_input("Escriba su orden, Señor..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # Construir el historial para la API oficial de Google
                chat_history = []
                for m in st.session_state.messages[:-1]:
                    chat_history.append({
                        "role": "user" if m["role"] == "user" else "model",
                        "parts": [{"text": m["content"]}]
                    })

                # Crear el chat con las instrucciones del sistema (Personalidad de JARVIS)
                chat = client.chats.create(
                    model="gemini-3.8-flash",
                    history=chat_history,
                    config={
                        "system_instruction": (
                            "Eres JARVIS (Just A Rather Very Intelligent System), "
                            "el asistente de inteligencia artificial de Tony Stark. Eres formal, "
                            "eficiente, altamente inteligente y ligeramente ingenioso. "
                            "Te diriges al usuario siempre como 'Señor' y respondes de manera "
                            "concisa y directa, ideal para lectura en dispositivos móviles."
                        )
                    }
                )

                # Enviar el mensaje actual
                response = chat.send_message(prompt)
                reply = response.text
                
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
                
            except Exception as e:
                st.error(f"Error de sistema: {e}")
                
