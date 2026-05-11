import streamlit as st
import datetime
import json
import os

st.set_page_config(page_title="Diana", page_icon="●", layout="centered")

# Black & White Theme
st.markdown("""
    <style>
    .stApp { background-color: black; color: white; }
    .user-msg { 
        text-align: right; 
        background: #1f1f1f; 
        padding: 12px; 
        border-radius: 15px; 
        margin: 8px 0; 
    }
    .diana-msg { 
        text-align: left; 
        background: #2a2a2a; 
        padding: 12px; 
        border-radius: 15px; 
        margin: 8px 0; 
    }
    </style>
""", unsafe_allow_html=True)

# Memory Setup
MEMORY_FILE = "diana_memory.json"

if "memory" not in st.session_state:
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            st.session_state.memory = json.load(f)
    else:
        st.session_state.memory = {"facts": {}, "history": []}

def save_memory():
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(st.session_state.memory, f, indent=2, ensure_ascii=False)

# Process Command Function (Defined BEFORE use)
def process_command(text):
    text = text.lower().strip()
    
    if "remember that" in text:
        try:
            key = text.split("remember that")[1].split("is")[0].strip()
            value = text.split("is", 1)[1].strip()
            st.session_state.memory["facts"][key] = value
            save_memory()
            return f"Got it. Remembered that {key} is {value}."
        except:
            return "I didn't understand the remember command."
    
    elif "what is" in text or "who is" in text:
        key = text.replace("what is", "").replace("who is", "").strip()
        if key in st.session_state.memory["facts"]:
            return f"{key} is {st.session_state.memory['facts'][key]}"
        return f"I don't know about {key} yet."
    
    elif "time" in text:
        return f"Current time is {datetime.datetime.now().strftime('%I:%M %p')}"
    
    elif "hello" in text or "hi" in text or "hey" in text:
        return "Hello sir. How can I help you today?"
    
    return "Understood. I'm listening."

# ====================== UI ======================
st.title("Diana")
st.caption("Black & White • Minimal • Always Ready")

# Display Chat History
for msg in st.session_state.memory["history"]:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg">You: {msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="diana-msg">Diana: {msg["content"]}</div>', unsafe_allow_html=True)

# User Input
user_input = st.text_input("Type here or say 'Hey Diana'", key="input")

if st.button("Send") or (user_input and user_input != st.session_state.get("last_input", "")):
    if user_input.strip():
        st.session_state.memory["history"].append({"role": "user", "content": user_input})
        
        response = process_command(user_input)
        
        st.session_state.memory["history"].append({"role": "assistant", "content": response})
        save_memory()
        
        st.session_state.last_input = user_input
        st.rerun()

# Voice Button
if st.button("🎤 Speak to Diana"):
    st.info("Voice feature coming soon (using browser microphone)")

# Sidebar
with st.sidebar:
    st.header("Diana Status")
    st.success("● Online")
    st.write(f"Memory Entries: {len(st.session_state.memory['facts'])}")
    if st.button("Clear Memory"):
        st.session_state.memory = {"facts": {}, "history": []}
        save_memory()
        st.success("Memory Cleared")
