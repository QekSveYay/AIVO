import os
import re # 引入正則表達式模組
from pypdf import PdfReader

class ContentParser:
    def __init__(self):
        pass

    def load_file(self, file_path):
        """
        統一入口：判斷副檔名並呼叫對應的讀取函式
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"找不到檔案: {file_path}")

        # 取得副檔名並轉為小寫
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        if ext == '.txt':
            return self._parse_txt(file_path)
        elif ext == '.pdf':
            return self._parse_pdf(file_path)
        else:
            return f"不支援的檔案格式: {ext} (目前僅支援 .txt, .pdf)"

    def _parse_txt(self, file_path):
        """
        解析 TXT 檔案
        特別處理：嘗試不同的編碼 (UTF-8, Big5) 以防中文亂碼
        """
        encodings = ['utf-8', 'big5', 'cp950'] # 常見中文編碼
        
        for enc in encodings:
            try:
                with open(file_path, 'r', encoding=enc) as f:
                    content = f.read()
                    print(f"成功使用 {enc} 編碼讀取")
                    return content
            except UnicodeDecodeError:
                continue # 如果失敗，嘗試下一種編碼
        
        return "讀取失敗：無法識別檔案編碼。"

    def _parse_pdf(self, file_path):
        """
        解析 PDF 檔案
        """
        text_content = []
        if PdfReader is None:
            raise RuntimeError(
                "Missing dependency 'pypdf'. Install it with:\n"
                "  python -m pip install pypdf\n"
                "or add it to requirements.txt and install dependencies."
            )

        try:
            reader = PdfReader(file_path)
            # 遍歷每一頁
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    text_content.append(text)
            
            # 將所有頁面的文字合併
            full_text = "\n".join(text_content)
            
            # 簡單清理：論文常有換行斷句問題，這裡可以做初步處理
            # (視需求可加入更複雜的正則表達式清理)
            return full_text
            
        except Exception as e:
            return f"PDF 讀取錯誤: {str(e)}"
        
    def split_text(self, text):
        """
        將長文本切分為句子列表。
        依據：句號、驚嘆號、問號、換行符號
        """
        # 使用正則表達式切分
        # pattern 意思：遇到 。 ! ? 或是換行，就切一刀，並保留標點符號
        pattern = r'([。.!！?？\n]+)'
        segments = re.split(pattern, text)
        
        # re.split 會把標點符號也當成獨立元素，我們需要把它們跟前一句話合併
        sentences = []
        current_sentence = ""
        
        for seg in segments:
            current_sentence += seg
            # 如果這一段包含標點符號，通常代表句子結束
            if re.search(pattern, seg):
                sentences.append(current_sentence.strip())
                current_sentence = ""
        
        # 處理剩下的尾巴
        if current_sentence:
            sentences.append(current_sentence.strip())
            
        # 過濾掉空字串
        return [s for s in sentences if s]

# 簡單測試用
if __name__ == "__main__":
    parser = ContentParser()
    # 你可以在這裡放一個測試檔案路徑來測試
    # print(parser.load_file("test.txt"))