import pyttsx3

class TTSEngine:
    def __init__(self):
        # 嘗試初始化，若驅動有問題則捕捉錯誤
        try:
            self.engine = pyttsx3.init()
            self._set_properties()
        except Exception as e:
            print(f"TTS 引擎初始化失敗: {e}")
            self.engine = None

    def _set_properties(self):
        if self.engine:
            self.engine.setProperty('rate', 150)
            self.engine.setProperty('volume', 0.9)

    def speak_sentence(self, text):
        if not self.engine:
            return

        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except RuntimeError:
            # 這通常發生在迴圈已經在跑的時候，我們可以忽略
            pass
        except Exception as e:
            print(f"朗讀錯誤: {e}")

    def stop(self):
        if self.engine:
            self.engine.stop()