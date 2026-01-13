import multiprocessing
import time
import asyncio
import edge_tts
import pygame
import os
import threading

from engines.music_engine import MusicEngine
from core.content_parser import ContentParser
from core.progress_manager import ProgressManager
from core.mood_engine import MoodEngine

# === 新的 Edge-TTS 工人 ===
def edge_tts_worker(text, voice_id):
    """
    使用 edge-tts 下載音訊並播放
    """
    async def amain():
        output_file = f"temp_speech_{os.getpid()}.mp3"
        communicate = edge_tts.Communicate(text, voice_id)
        await communicate.save(output_file)
        
        # 使用 pygame 播放生成的 MP3
        pygame.mixer.init()
        pygame.mixer.music.load(output_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)
        
        pygame.mixer.music.unload()
        if os.path.exists(output_file):
            os.remove(output_file)

    asyncio.run(amain())

class AIVOController:
    def __init__(self):
        self.music = MusicEngine()
        self.parser = ContentParser()
        self.progress_mgr = ProgressManager()
        self.mood_engine = MoodEngine()

        self.selected_voice_id = "zh-TW-HsiaoChenNeural" # 預設台灣女聲

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
        
        # 如果使用者沒選音樂，自動分析文本情緒並配樂
        if not bgm_path:
            bgm_path = self.mood_engine.get_music_for_text(text_content[:1000])
            print(f"自動偵測氛圍並配樂: {bgm_path}")
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
        for i, sentence in enumerate(sentences):
            if self.stop_signal: break
            
            real_index = i + start_offset
            if self.current_file_path:
                self.progress_mgr.save_progress(self.current_file_path, real_index)

            if sentence.strip():
                print(f">>> Edge-TTS 朗讀: {sentence[:15]}...")
                # 啟動 Edge-TTS 專用的進程
                self.current_worker = multiprocessing.Process(
                    target=edge_tts_worker, 
                    args=(sentence, self.selected_voice_id)
                )
                self.current_worker.start()
                self.current_worker.join()
            
            time.sleep(0.1)
        self.is_running = False

    def stop_all(self):
        self.stop_signal = True
        if self.current_worker and self.current_worker.is_alive():
            self.current_worker.terminate()
        self.music.stop()
        self.is_running = False
    
    def get_voices(self):
        """
        這部分我們可以手動列出常用的 Edge-TTS 人聲
        或是透過 edge-tts --list-voices 取得
        """
        return [
            {"id": "zh-TW-HsiaoChenNeural", "name": "曉臻 (台灣女聲)"},
            {"id": "zh-TW-YunJheNeural", "name": "雲哲 (台灣男聲)"},
            {"id": "zh-CN-XiaoxiaoNeural", "name": "曉曉 (普通話女聲)"},
            {"id": "zh-CN-YunxiNeural", "name": "雲希 (普通話男聲)"},
            {"id": "en-US-GuyNeural", "name": "Guy (美式男聲)"}
        ]

    def set_voice(self, voice_id):
        self.selected_voice_id = voice_id