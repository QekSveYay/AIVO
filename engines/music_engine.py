try:
    import pygame
except ImportError:
    pygame = None


class MusicEngine:
    def __init__(self):
        if pygame is None:
            raise RuntimeError(
                "Missing dependency 'pygame'. Install it with:\n"
                "  python -m pip install pygame\n"
                "or add it to requirements.txt and install dependencies."
            )
        pygame.mixer.init()
        self.is_playing = False

    def load_music(self, file_path):
        try:
            pygame.mixer.music.load(file_path)
            print(f"音樂已載入: {file_path}")
        except Exception as e:
            print(f"載入音樂失敗: {e}")

    def play(self, loop=True):
        # loop=True 預設背景音樂循環播放
        loops = -1 if loop else 0
        pygame.mixer.music.play(loops=loops)
        self.is_playing = True

    def pause(self):
        pygame.mixer.music.pause()
        self.is_playing = False

    def unpause(self):
        pygame.mixer.music.unpause()
        self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        
    def set_volume(self, volume):
        # volume 範圍 0.0 到 1.0
        pygame.mixer.music.set_volume(volume)