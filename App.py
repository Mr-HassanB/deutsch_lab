import streamlit as st
import openai
from streamlit_mic_recorder import mic_recorder
import io

# --- 1. CONFIGURATION VISUELLE (Style Duolingo) ---
st.set_page_config(page_title="Deutsch Lab Coach", page_icon="🦉", layout="centered")

st.markdown("""
    <style>
    /* Couleurs Duolingo */
    .stApp { background-color: #FFFFFF; }
    .stChatMessage { 
        border-radius: 20px; 
        border: 2px solid #E5E5E5; 
        padding: 15px;
        margin-bottom: 15px;
    }
    .stChatInputContainer { padding-bottom: 20px; }
    h1 { color: #58CC02; font-family: 'Helvetica Neue', sans-serif; font-weight: bold; text-align: center; }
    
    /* Animation du bouton micro */
    .mic-container {
        display: flex;
        justify-content: center;
        padding: 20px;
        background: #F7F7F7;
        border-radius: 15px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BARRE LATÉRALE ---
with st.sidebar:
    st.markdown('<img src="https://api.dicebear.com/7.x/bottts/svg?seed=Felix" style="width:120px; display:block; margin:auto;">', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>Coach Felix</h2>", unsafe_allow_html=True)
    st.divider()
    api_key = st.text_input("Clé API OpenAI", type="password", help="Entre ta clé pour activer l'IA")
    st.markdown("---")
    st.write("💡 **Astuce :** Parle en Allemand, et si tu es bloqué, pose ta question en Français !")

# --- 3. LOGIQUE DE L'IA ---
st.title("🦉 Deutsch Lab")

if api_key:
    client = openai.OpenAI(api_key=api_key)

    # Initialisation de la mémoire
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "Tu es Felix, un coach d'allemand ludique. Réponds toujours en allemand. Si l'utilisateur parle français, réponds en allemand puis donne une explication rapide en français."}
        ]

    # Affichage de la discussion
    for message in st.session_state.messages:
        if message["role"] != "system":
            avatar = "👤" if message["role"] == "user" else "https://api.dicebear.com/7.x/bottts/svg?seed=Felix"
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])

    # --- 4. ZONE DE SAISIE (MICRO & TEXTE) ---
    st.write("### 🎤 Parle ou écris :")
    
    # Le Micro
    audio_record = mic_recorder(
        start_prompt="Démarrer le micro 🎤",
        stop_prompt="Envoyer 📤",
        key='recorder'
    )

    # Si on reçoit un enregistrement audio
    if audio_record:
        audio_bio = io.BytesIO(audio_record['bytes'])
        audio_bio.name = "audio.wav"
        
        with st.spinner("Transcription en cours..."):
            transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_bio)
            user_input = transcript.text
    else:
        # Sinon, on vérifie si l'utilisateur a tapé du texte
        user_input = st.chat_input("Écris ton message ici...")

    # Traitement de la réponse
    if user_input:
        # Ajouter le message utilisateur
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)

        # Générer la réponse de Felix
        with st.chat_message("assistant", avatar="https://api.dicebear.com/7.x/bottts/svg?seed=Felix"):
            with st.spinner("Felix réfléchit..."):
                # 1. Texte via GPT
                completion = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=st.session_state.messages
                )
                ai_response = completion.choices[0].message.content
                st.markdown(ai_response)

                # 2. Voix via TTS
                audio_res = client.audio.speech.create(
                    model="tts-1",
                    voice="onyx",
                    input=ai_response
                )
                audio_res.stream_to_file("speech_output.mp3")
                st.audio("speech_output.mp3", format="audio/mp3", autoplay=True)

        st.session_state.messages.append({"role": "assistant", "content": ai_response})

else:
    st.info("👋 Bienvenue ! Entre ta clé API OpenAI dans la barre latérale pour commencer à parler avec Felix.")