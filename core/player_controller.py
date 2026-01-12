import multiprocessing
import time
import pyttsx3
from engines.music_engine import MusicEngine
from core.content_parser import ContentParser

# === 極簡工人：只負責唸出一句話就關閉 ===
def tts_single_speak(text):
    """
    這個函式每次只執行一次朗讀，確保系統資源完全釋放。
    """
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        engine.say(text)
        engine.runAndWait()
        # 強制結束引擎，釋放驅動程式
        del engine
    except Exception as e:
        print(f"朗讀單句錯誤: {e}")

class AIVOController:
    def __init__(self):
        self.music = MusicEngine()
        self.parser = ContentParser()
        self.is_running = False
        self.stop_signal = False
        self.current_worker = None
        self.master_thread = None

    def start_session(self, text_content, bgm_path=None):
        if self.is_running:
            return # 防止重複啟動
            
        sentences = self.parser.split_text(text_content)
        if not sentences:
            return

        self.is_running = True
        self.stop_signal = False
        
        if bgm_path:
            self.music.load_music(bgm_path)
            self.music.set_volume(0.3)
            self.music.play(loop=True)

        import threading
        self.master_thread = threading.Thread(target=self._manage_sentences, args=(sentences,))
        self.master_thread.daemon = True # 確保主程式關閉時，這個執行緒也會關閉
        self.master_thread.start()

    def _manage_sentences(self, sentences):
        """
        主管理迴圈：一句一句派發任務給進程
        """
        for i, sentence in enumerate(sentences):
            if self.stop_signal:
                break
            
            if not sentence.strip():
                continue

            print(f"[{i+1}/{len(sentences)}] 正在朗讀: {sentence[:20]}...")

            # 為每一句話開一個獨立進程
            self.current_worker = multiprocessing.Process(
                target=tts_single_speak, 
                args=(sentence,)
            )
            self.current_worker.start()
            
            # 等待這一句唸完 (Join 會阻塞直到進程結束)
            self.current_worker.join()
            
            # 句子間的自然停頓
            time.sleep(0.2)

        self.music.stop()
        self.is_running = False
        print("--- 播放完畢 ---")

    def stop_all(self):
        self.stop_signal = True
        if self.current_worker and self.current_worker.is_alive():
            self.current_worker.terminate()
        self.music.stop()
        self.is_running = False