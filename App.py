import streamlit as st
from groq import Groq

# --- 1. CONFIGURATION VISUELLE (STYLE CLAIR UNIQUEMENT) ---
st.set_page_config(page_title="Deutsch Lab", page_icon="🦉")

st.markdown("""
    <style>
    /* Fond blanc total */
    .stApp, .stSidebar, .stSidebar > div {
        background-color: #FFFFFF !important;
    }
    
    /* Texte en noir pour tout le monde */
    p, span, div, label, h1, h2, h3 {
        color: #000000 !important;
    }

    /* Bulles de chat bien visibles */
    .stChatMessage {
        background-color: #F0F2F6 !important;
        border: 1px solid #D1D1D1 !important;
        border-radius: 15px !important;
    }

    /* Forcer le titre en vert Duolingo */
    .duo-title {
        color: #58CC02 !important;
        font-weight: bold;
        text-align: center;
        font-size: 32px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BARRE LATÉRALE (ACCÈS MOBILE) ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>Paramètres</h2>", unsafe_allow_html=True)
    # L'image de l'avatar
    st.markdown('<img src="https://api.dicebear.com/7.x/bottts/svg?seed=Felix" style="width:100px; display:block; margin:auto;">', unsafe_allow_html=True)
    
    st.write("---")
    # Zone de la clé
    groq_key = st.text_input("Clé API Groq (gsk_...)", type="password")
    st.write("---")
    st.write("💡 **Sur mobile :** Clique sur la petite flèche en haut à gauche pour fermer ce menu.")

# --- 3. CONTENU PRINCIPAL ---
st.markdown('<div class="duo-title">🦉 Mon Deutsch Lab</div>', unsafe_allow_html=True)

if not groq_key:
    # Message d'aide si la clé manque
    st.warning("⚠️ Pour commencer, clique sur les **3 petits traits (menu)** ou la **petite flèche** en haut à gauche de ton téléphone et entre ta clé Groq.")
else:
    client = Groq(api_key=groq_key)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "Tu es Felix, un prof d'allemand. Réponds en allemand de façon simple, puis traduis en français."}
        ]

    # Affichage des messages
    for message in st.session_state.messages:
        if message["role"] != "system":
            avatar = "👤" if message["role"] == "user" else "🤖"
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])

    # Zone de texte
    user_input = st.chat_input("Écris ici...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)

        with st.chat_message("assistant", avatar="🤖"):
            chat_completion = client.chat.completions.create(
                messages=st.session_state.messages,
                model="llama-3.3-70b-versatile",
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
