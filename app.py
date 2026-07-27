import streamlit as st
import json
import speech_recognition as sr
import sounddevice as sd
import soundfile as sf
import serial
import time

# -----------------------------
# 🔌 Arduino Connection (SAFE)
# -----------------------------
if "arduino" not in st.session_state:
    try:
        st.session_state.arduino = serial.Serial('COM3', 9600, timeout=1)
        time.sleep(2)
        st.success("✅ Arduino Connected")
    except Exception as e:
        st.error(f"❌ Arduino not connected: {e}")
        st.session_state.arduino = None

arduino = st.session_state.arduino

# -----------------------------
# 📂 Load JSON data
# -----------------------------
with open("data.json") as f:
    data = json.load(f)

# -----------------------------
# 🧠 Diagnosis function
# -----------------------------
def diagnose(user_input):
    user_input = user_input.lower()
    words = user_input.split()

    best_match = None
    max_matches = 0

    for item in data:
        match_count = 0
        for symptom in item["symptoms"]:
            symptom = symptom.lower()
            for word in words:
                if symptom in word or word in symptom:
                    match_count += 1

        if match_count > max_matches:
            max_matches = match_count
            best_match = item

    return best_match

# -----------------------------
# 🚨 Emergency detection
# -----------------------------
def check_emergency(user_input):
    user_input = user_input.lower()
    if "emerg" in user_input or "help" in user_input or "sos" in user_input:
        return True
    return False

# -----------------------------
# 🎤 Voice input (3 sec)
# -----------------------------
def get_voice_input():
    fs = 44100
    duration = 3

    st.write("🎤 Listening...")

    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()

    sf.write("temp.wav", recording, fs)

    r = sr.Recognizer()
    with sr.AudioFile("temp.wav") as source:
        audio = r.record(source)

    try:
        return r.recognize_google(audio, language='en-IN')
    except Exception as e:
        return "Error: " + str(e)

# -----------------------------
# 🖥️ UI
# -----------------------------
st.title("🎤 AI Health Chatbot")

if st.button("🎙️ Speak Now"):

    user_input = get_voice_input()

    st.markdown("### 💬 You said:")
    st.info(user_input)

    # 🚨 Emergency
    if check_emergency(user_input):
        st.error("🚨 EMERGENCY DETECTED!")
        st.markdown("### 📞 Call Ambulance Immediately: 108 / 102")

        if arduino:
            try:
                arduino.write(b'S')
                arduino.flush()
            except:
                st.error("⚠️ Arduino send failed")

    else:
        result = diagnose(user_input)

        if result:
            disease = result['disease']
            medicine = result['medicine']

            st.success(f"Disease: {disease}\nMedicine: {medicine}")

            if arduino:
                try:
                    if medicine == "Paracetamol":
                        arduino.write(b'1')
                    elif medicine == "Ibuprofen":
                        arduino.write(b'2')
                    elif medicine == "Antacid":
                        arduino.write(b'3')
                    elif medicine == "Cetirizine":
                        arduino.write(b'4')
                    elif medicine == "Eno":
                        arduino.write(b'5')

                    arduino.flush()

                except:
                    st.error("⚠️ Arduino send failed")

        else:
            st.warning("No matching illness found.")
