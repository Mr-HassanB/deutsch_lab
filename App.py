import streamlit as st
from groq import Groq
from streamlit_mic_recorder import mic_recorder
import io

# --- 1. CONFIGURATION VISUELLE (Correction texte noir) ---
st.set_page_config(page_title="Deutsch Lab Coach", page_icon="🦉")

st.markdown("""
    <style>
    /* Fond de page blanc */
    .stApp { background-color: #FFFFFF; }
    
    /* Bulles de chat : fond gris clair et texte noir forcé */
    .stChatMessage { 
        border-radius: 20px; 
        border: 2px solid #E5E5E5; 
        background-color: #F8F9FA !important;
    }
    
    /* Forcer la couleur du texte en noir pour être lisible sur mobile */
    .stMarkdown p, .stMarkdown li, span { 
        color: #111111 !important; 
    }
    
    /* Titre en vert Duolingo */
    h1 { color: #58CC02; text-align: center; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BARRE LATÉRALE ---
with st.sidebar:
    st.markdown('<img src="https://api.dicebear.com/7.x/bottts/svg?seed=Felix" style="width:100px; display:block; margin:auto;">', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: black;'>Coach Felix</h3>", unsafe_allow_html=True)
    st.divider()
    # Zone pour la clé Groq (Gratuite)
    api_key = st.text_input("Clé API Groq (gsk_...)", type="password")
    st.markdown("[Obtenir une clé gratuite ici](https://console.groq.com/keys)")

# --- 3. LOGIQUE DE L'IA ---
st.title("🦉 Mon Deutsch Lab")

if api_key:
    client = Groq(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "Tu es Felix, un prof d'allemand sympa. Réponds en allemand, puis donne une courte traduction ou explication en français si la phrase est complexe."}
        ]

    # Affichage de la conversation
    for message in st.session_state.messages:
        if message["role"] != "system":
            avatar = "👤" if message["role"] == "user" else "https://api.dicebear.com/7.x/bottts/svg?seed=Felix"
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])

    # Zone d'écriture
    user_input = st.chat_input("Réponds à Felix ici...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)

        with st.chat_message("assistant", avatar="https://api.dicebear.com/7.x/bottts/svg?seed=Felix"):
            with st.spinner("Felix réfléchit..."):
                try:
                    chat_completion = client.chat.completions.create(
                        messages=st.session_state.messages,
                        model="llama-3.3-70b-versatile",
                    )
                    response = chat_completion.choices[0].message.content
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Erreur : {e}")

else:
    st.info("👋 Hallo! Pour commencer, entre ta clé API Groq gratuite dans la barre latérale à gauche.")
