from core.player_controller import SmartPlayerController
import time

def main():
    # 1. 實例化控制器
    player = SmartPlayerController()

    # 模擬輸入資料 (未來這裡會接上檔案讀取器)
    sample_text = """
    這是一個智慧播放器的測試文本。
    我們正在測試文字轉語音的功能，同時背景應該會有輕音樂在播放。
    未來的版本，這裡的聲音將會被替換成更擬真的 AI 人聲。
    """
    
    # 假設你有一個 mp3 檔案，請替換成實際路徑，或者設為 None 測試純朗讀
    # 這裡請準備一個 'bgm.mp3' 放在同目錄下，或是將路徑設為 None
    bgm_file = "harp.wav" 
    
    # 為了演示，我們檢查一下檔案是否存在，若無則不播音樂
    import os
    if not os.path.exists(bgm_file):
        print(f"提示: 找不到 {bgm_file}，將僅進行語音朗讀。")
        bgm_file = None

    # 2. 開始播放
    player.start_session(sample_text, bgm_file)

    # 3. 模擬程式運行，等待使用者輸入來停止
    try:
        input("按下 Enter 鍵以停止播放...\n")
    except KeyboardInterrupt:
        pass
    
    # 4. 停止並退出
    player.stop_all()

if __name__ == "__main__":
    main()