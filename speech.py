
import time
import threading
from gtts import gTTS
import os
import tempfile
from datetime import datetime
import pygame  # Add this import at the top

# Speak the welcome message in Nepali
def speak_nepali(text):
    try:
        language = 'ne'
        speech = gTTS(text=text, lang=language, slow=False)
        fd, temp_path = tempfile.mkstemp(suffix=".mp3")
        os.close(fd)
        speech.save(temp_path)

        pygame.mixer.init()
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()

        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        # Stop and unload music
        pygame.mixer.music.stop()
        pygame.mixer.quit()

        os.remove(temp_path)
    except Exception as e:
        print(f"❌ Error during TTS: {e}")


# Function to welcome recognized person
def welcome_person(name):
    message = f"विरिन्ची कलेजमा {name} लाई स्वागत छ।"
    threading.Thread(target=speak_nepali, args=(message,)).start()