from core.player_controller import AIVOController
from core.content_parser import ContentParser
import os

def main():
    # 1. 初始化控制器與解析器
    player = AIVOController()
    parser = ContentParser()

    print("=== 智慧播放器 v0.2 ===")
    
    # 2. 設定要讀取的檔案 (請在此修改你的測試檔案路徑)
    # 建議在專案目錄下放一個 'novel.txt' 或 'paper.pdf' 測試
    input_file = "novel.txt" 
    bgm_file = "harp.wav"

    # 3. 解析文本
    print(f"正在讀取檔案: {input_file} ...")
    try:
        text_content = parser.load_file(input_file)
        
        # 簡單檢查是否有內容
        if not text_content or len(text_content) < 5:
            print("警告: 讀取到的內容過少或為空。")
        else:
            print(f"讀取成功！字數: {len(text_content)}")
            
    except Exception as e:
        print(f"錯誤: {e}")
        return

    # 4. 檢查 BGM
    if not os.path.exists(bgm_file):
        bgm_file = None
        print("提示: 無背景音樂檔案，將僅進行朗讀。")

    # 5. 開始播放
    # 為了避免一次讀太長，我們只取前 500 字做示範，實際使用可移除切片
    preview_text = text_content[:500] 
    
    player.start_session(preview_text, bgm_file)

    try:
        input(">> 按下 Enter 鍵以停止播放...\n")
    except KeyboardInterrupt:
        pass
    
    player.stop_all()

if __name__ == "__main__":
    main()