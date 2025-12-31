import streamlit as st
from groq import Groq
from streamlit_mic_recorder import mic_recorder
import io

# --- STYLE DUOLINGO ---
st.set_page_config(page_title="Deutsch Lab Gratuit", page_icon="🦉")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    .stChatMessage { border-radius: 20px; border: 2px solid #E5E5E5; }
    h1 { color: #58CC02; text-align: center; font-family: sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURATION GROQ ---
with st.sidebar:
    st.markdown('<img src="https://api.dicebear.com/7.x/bottts/svg?seed=Felix" style="width:100px; display:block; margin:auto;">', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Felix (Version Groq)</h3>", unsafe_allow_html=True)
    groq_key = st.text_input("Entre ta clé API GROQ (Gratuite)", type="password")
    st.info("Obtiens ta clé sur console.groq.com")

st.title("🦉 Mon Deutsch Lab")

if groq_key:
    client = Groq(api_key=groq_key)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "Tu es Felix, un prof d'allemand. Réponds en allemand. Si l'utilisateur parle français, explique en français à la fin."}
        ]

    # Affichage des messages
    for message in st.session_state.messages:
        if message["role"] != "system":
            avatar = "👤" if message["role"] == "user" else "https://api.dicebear.com/7.x/bottts/svg?seed=Felix"
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])

    # Entrée utilisateur
    user_input = st.chat_input("Écris ton message ici...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)

        with st.chat_message("assistant", avatar="https://api.dicebear.com/7.x/bottts/svg?seed=Felix"):
            with st.spinner("Felix écrit..."):
                chat_completion = client.chat.completions.create(
                    messages=st.session_state.messages,
                    model="llama-3.3-70b-versatile", # Un des meilleurs modèles gratuits
                )
                response = chat_completion.choices[0].message.content
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

else:
    st.warning("👈 S'il te plaît, ajoute ta clé Groq gratuite dans la barre latérale.")
