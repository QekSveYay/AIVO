import multiprocessing
from core.player_controller import AIVOController
from core.content_parser import ContentParser
import os
import time

def main():
    player = AIVOController()
    parser = ContentParser()
    
    # 建立一個長一點的測試文本
    long_text = """
    這是第一句測試文本，我們正在測試分段讀取的功能。
    這是第二句，系統應該會先把文章切開，然後一句一句讀。
    這樣做的好處是，當你想要停止的時候，系統可以反應得更快。
    不像舊版本，必須等整篇文章讀完才能停下來。
    這是第五句，你可以試著在這一句讀完之前，按下 Enter 鍵停止。
    如果成功停止，代表我們的架構重構非常成功！
    接下來是湊字數的內容，為了證明它能處理長文。
    天氣真好，適合寫程式。
    人工智慧的發展日新月異，Python 是最好的語言。
    """
    
    # 或者讀取你的小說檔案
    # text_content = parser.load_file("novel.txt")
    
    # 這裡我們先用變數測試
    text_content = long_text
    bgm_file = "harp.wav"
    
    if not os.path.exists(bgm_file):
        bgm_file = None

    print("--- 按下 Enter 後開始播放 ---")
    input()
    
# 開始播放
    player.start_session(long_text, bgm_file)

    print(">> 系統運行中... 按下 Enter 鍵強制停止 <<")
    input() 
    
    player.stop_all()
    print("程式結束。")

# [非常重要] 這一行絕對不能少！
if __name__ == "__main__":
    multiprocessing.freeze_support() # 如果你以後要打包成 exe，這行會有幫助
    main()