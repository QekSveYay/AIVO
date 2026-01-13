import pyttsx3

import pyttsx3

class TTSEngine:
    def __init__(self):
        # 建立一個臨時引擎來讀取系統資訊
        self.temp_engine = pyttsx3.init()

    def get_available_voices(self):
        """
        取得系統內建的所有人聲清單
        """
        voices = self.temp_engine.getProperty('voices')
        voice_list = []
        for voice in voices:
            # 儲存名稱與 ID，ID 是切換聲音的關鍵
            voice_list.append({
                'id': voice.id,
                'name': voice.name,
                'languages': voice.languages
            })
        return voice_list

# 注意：tts_single_speak 函式需要接收 voice_id
def tts_single_speak(text, voice_id=None):
    try:
        engine = pyttsx3.init()
        if voice_id:
            engine.setProperty('voice', voice_id)
        
        engine.setProperty('rate', 160)
        engine.setProperty('volume', 1.0)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
        del engine
    except Exception as e:
        print(f"TTS Process Error: {e}")