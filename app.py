import streamlit as st
from openai import OpenAI

# Configuración de la página para dispositivos móviles
st.set_page_config(
    page_title="J.A.R.V.I.S. Mobile", page_icon="🤖", layout="centered"
)

# Estilo visual futurista / limpio
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

# Configurar API Key
api_key = st.sidebar.text_input("API Key de OpenAI", type="password")

if not api_key:
    st.warning("Por favor, ingrese su API Key de OpenAI en la barra lateral para iniciar los sistemas.")
else:
    client = OpenAI(api_key=api_key)

    # Inicializar el historial de conversación con el System Prompt de JARVIS
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    "Eres J.A.R.V.I.S. (Just A Rather Very Intelligent System), "
                    "el asistente de inteligencia artificial avanzado. Eres formal, "
                    "eficiente, altamente inteligente, analítico y un poco sarcástico. "
                    "Te diriges al usuario siempre como 'Señor'. Responde de forma "
                    "concisa y directa, ideal para dispositivos móviles."
                ),
            }
        ]

    # Mostrar el historial de chat
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Entrada del usuario
    if prompt := st.chat_input("¿Qué orden desea ejecutar, Señor?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generar respuesta de JARVIS
        with st.chat_message("assistant"):
            with st.spinner("Analizando datos..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=st.session_state.messages,
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                
                st.session_state.messages.append({"role": "assistant", "content": reply})

                # Reproducir respuesta con voz sintetizada
                audio_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={reply.replace(' ', '%20')}&tl=es&client=tw-ob"
                st.audio(audio_url, format="audio/mp3", autoplay=True)
