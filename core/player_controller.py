import multiprocessing
import time
import pyttsx3
import threading
from engines.music_engine import MusicEngine
from engines.tts_engine import TTSEngine, tts_single_speak
from core.content_parser import ContentParser
from core.progress_manager import ProgressManager

class AIVOController:
    def __init__(self):
        self.music = MusicEngine()
        self.parser = ContentParser()
        self.progress_mgr = ProgressManager()
        self.tts_engine = TTSEngine()
        self.selected_voice_id = None

        self.is_running = False
        self.stop_signal = False
        self.current_worker = None 
        self.current_file_path = None
        self.current_index = 0

    def start_session(self, file_path, text_content, bgm_path=None, start_index=0):
        if self.is_running: self.stop_all()

        # 1. 取得完整句子列表
        all_sentences = self.parser.split_text(text_content)
        # 2. 篩選出要讀的部分
        remaining_sentences = all_sentences[start_index:]
        
        if not remaining_sentences:
            print("沒有可讀的內容")
            return

        self.current_file_path = file_path
        self.is_running = True
        self.stop_signal = False
        
        if bgm_path:
            self.music.load_music(bgm_path)
            self.music.set_volume(0.2)
            self.music.play(loop=True)

        # 啟動管理執行緒
        self.master_thread = threading.Thread(
            target=self._manage_sentences, 
            args=(remaining_sentences, start_index)
        )
        self.master_thread.daemon = True
        self.master_thread.start()

    def _manage_sentences(self, sentences, start_offset):
        """
        主管理迴圈：一句一句派發任務給進程
        """
        # 取得目前的 voice_id
        vid = self.selected_voice_id

        for i, sentence in enumerate(sentences):
            if self.stop_signal: break
            
            # 關鍵修正：計算目前真正的句子編號
            real_index = i + start_offset
            
            # 更新進度紀錄
            if self.current_file_path:
                self.progress_mgr.save_progress(self.current_file_path, real_index)

            if sentence.strip():
                print(f">>> 朗讀第 {real_index + 1} 句: {sentence[:15]}...")
                
                # 建立並啟動語音進程
                # 將 voice_id 傳給進程
                self.current_worker = multiprocessing.Process(
                    target=tts_single_speak, 
                    args=(sentence, vid)
                )
                self.current_worker.start()
                self.current_worker.join() # 等待唸完
            
            time.sleep(0.3) # 句間短暫停頓

        self.is_running = False
        self.music.stop()
        print("--- 任務完成 ---")

    def stop_all(self):
        self.stop_signal = True
        if self.current_worker and self.current_worker.is_alive():
            self.current_worker.terminate()
        self.music.stop()
        self.is_running = False
    
    def get_voices(self):
        return self.tts_engine.get_available_voices()

    def set_voice(self, voice_id):
        self.selected_voice_id = voice_id