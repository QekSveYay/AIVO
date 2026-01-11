from engines.tts_engine import TTSEngine
from engines.music_engine import MusicEngine
import time

class SmartPlayerController:
    def __init__(self):
        self.tts = TTSEngine()
        self.music = MusicEngine()
        
    def start_session(self, text_content, bgm_path=None):
        """
        開始一個閱讀工作階段：播放背景音樂並朗讀文字
        """
        print("--- 啟動智慧播放模式 ---")
        
        # 1. 如果有背景音樂，先開始播放
        if bgm_path:
            self.music.load_music(bgm_path)
            self.music.set_volume(0.3) # 背景音樂音量調低，以免蓋過人聲
            self.music.play(loop=True)
            
        # 2. 稍微停頓，營造氛圍
        time.sleep(1)
        
        # 3. 開始朗讀
        self.tts.speak(text_content)

    def stop_all(self):
        """停止所有聲音"""
        self.tts.stop()
        self.music.stop()
        print("--- 播放已停止 ---")