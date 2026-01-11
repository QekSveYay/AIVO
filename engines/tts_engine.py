import threading

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None


class TTSEngine:
    def __init__(self):
        if pyttsx3 is None:
            raise RuntimeError(
                "Missing dependency 'pyttsx3'. Install it with:\n"
                "  python -m pip install pyttsx3\n"
                "or add it to requirements.txt and install dependencies."
            )
        # 初始化 pyttsx3
        self.engine = pyttsx3.init()
        self.is_speaking = False
        self._set_properties()

    def _set_properties(self):
        # 設定語速與音量 (未來可從外部調整)
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)

    def speak(self, text):
        """
        執行朗讀功能
        使用 Thread 防止卡住主程式
        """
        if not self.is_speaking:
            self.is_speaking = True
            # 開啟新執行緒來朗讀，避免介面凍結
            t = threading.Thread(target=self._run_speak, args=(text,))
            t.start()

    def _run_speak(self, text):
        print(f"正在朗讀: {text[:20]}...")
        self.engine.say(text)
        self.engine.runAndWait()
        self.is_speaking = False

    def stop(self):
        if self.is_speaking:
            self.engine.stop()
            self.is_speaking = False