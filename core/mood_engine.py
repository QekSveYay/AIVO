import os
import json
import random

class MoodEngine:
    def __init__(self, music_folder="music"):
        self.music_folder = music_folder
        self.mood_map = {
            "tense": ["緊張", "恐怖", "殺死", "黑影", "危險", "突然", "心跳"],
            "happy": ["笑", "開心", "陽光", "溫暖", "希望", "愉快", "婚禮"],
            "calm": ["安靜", "湖泊", "微風", "思考", "睡著", "深夜", "和平"],
            "academic": ["研究", "數據", "實驗", "結果", "理論", "證明", "論文"]
        }
        # 載入音樂清單
        self.music_library = {
            "tense": ["tense_1.mp3"],
            "happy": ["happy_1.mp3"],
            "calm": ["calm_1.mp3"],
            "academic": ["study_1.mp3"]
        }

    def detect_mood(self, text):
        """簡單的關鍵字情緒檢測"""
        scores = {mood: 0 for mood in self.mood_map.keys()}
        for mood, keywords in self.mood_map.items():
            for word in keywords:
                if word in text:
                    scores[mood] += 1
        
        # 取得得分最高的情緒，若無則預設為 calm
        detected = max(scores, key=scores.get)
        if scores[detected] == 0:
            return "calm"
        return detected

    def get_music_for_text(self, text):
        mood = self.detect_mood(text)
        playlist = self.music_library.get(mood, self.music_library["calm"])
        song = random.choice(playlist)
        return os.path.join(self.music_folder, song)