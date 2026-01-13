import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from core.player_controller import AIVOController
import multiprocessing

class AIVOGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("程式夥伴 - 智慧播放器 v1.0")
        self.root.geometry("500x400")
        
        self.controller = AIVOController()
        self.selected_file = None
        self.selected_bgm = None

        self._setup_ui()
        self._load_voices()

    def _setup_ui(self):
        # 標題
        tk.Label(self.root, text="智慧播放器", font=("Arial", 18, "bold")).pack(pady=10)

        # 檔案選取區塊
        file_frame = tk.LabelFrame(self.root, text="檔案設定", padx=10, pady=10)
        file_frame.pack(padx=20, pady=10, fill="x")

        self.lbl_text = tk.Label(file_frame, text="文本: 尚未選擇", fg="gray")
        self.lbl_text.grid(row=0, column=0, sticky="w")
        tk.Button(file_frame, text="選擇文本", command=self._select_text).grid(row=0, column=1, padx=5)

        self.lbl_bgm = tk.Label(file_frame, text="背景音樂: 尚未選擇", fg="gray")
        self.lbl_bgm.grid(row=1, column=0, sticky="w")
        tk.Button(file_frame, text="選擇音樂", command=self._select_bgm).grid(row=1, column=1, padx=5)

        # 在「檔案設定」下方增加「聲音設定」
        voice_frame = tk.LabelFrame(self.root, text="語音人聲設定", padx=10, pady=10)
        voice_frame.pack(padx=20, pady=10, fill="x")

        tk.Label(voice_frame, text="選擇人聲:").grid(row=0, column=0, sticky="w")
        
        self.voice_combo = ttk.Combobox(voice_frame, state="readonly", width=40)
        self.voice_combo.grid(row=0, column=1, padx=5)
        # 當選單變動時觸發
        self.voice_combo.bind("<<ComboboxSelected>>", self._on_voice_selected)
        
        # 控制區塊
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=20)

        self.btn_play = tk.Button(control_frame, text="開始播放", bg="#4CAF50", fg="white", 
                                  width=15, height=2, command=self._handle_play)
        self.btn_play.grid(row=0, column=0, padx=10)

        self.btn_stop = tk.Button(control_frame, text="停止播放", bg="#f44336", fg="white", 
                                  width=15, height=2, command=self._handle_stop)
        self.btn_stop.grid(row=0, column=1, padx=10)

        # 狀態顯示
        self.status_var = tk.StringVar(value="狀態: 準備就緒")
        tk.Label(self.root, textvariable=self.status_var, fg="blue").pack(pady=10)

    def _select_text(self):
        file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("PDF files", "*.pdf")])
        if file:
            self.selected_file = file
            self.lbl_text.config(text=f"文本: {file.split('/')[-1]}", fg="black")

    def _select_bgm(self):
        file = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3 *.wav")])
        if file:
            self.selected_bgm = file
            self.lbl_bgm.config(text=f"音樂: {file.split('/')[-1]}", fg="black")

    def _handle_play(self):
        if not self.selected_file:
            messagebox.showwarning("提示", "請選擇檔案")
            return
        
        # 每次按下播放時，重新檢查進度
        last_pos = self.controller.progress_mgr.get_progress(self.selected_file)
        start_idx = 0
        
        if last_pos > 0:
            if messagebox.askyesno("續讀", f"是否從第 {last_pos + 1} 句繼續？"):
                start_idx = last_pos

        try:
            content = self.controller.parser.load_file(self.selected_file)
            # 確保這裡傳入了四個參數
            self.controller.start_session(self.selected_file, content, self.selected_bgm, start_idx)
            self.status_var.set(f"播放中 (從第 {start_idx+1} 句開始)")
        except Exception as e:
            messagebox.showerror("錯誤", str(e))

    def _handle_stop(self):
        self.controller.stop_all()
        self.status_var.set("狀態: 已停止")
        self.btn_play.config(state="normal")
    
    def _select_text(self):
        file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("PDF files", "*.pdf")])
        if file:
            self.selected_file = file
            # 檢查是否有存檔進度
            last_pos = self.controller.progress_mgr.get_progress(file)
            
            if last_pos > 0:
                self.lbl_text.config(text=f"文本: {file.split('/')[-1]} (進度: 第{last_pos+1}句)", fg="blue")
                self.resume_index = last_pos # 暫存進度
            else:
                self.lbl_text.config(text=f"文本: {file.split('/')[-1]}", fg="black")
                self.resume_index = 0

    def _load_voices(self):
        # 取得我們手動定義的 Edge-TTS 人聲
        self.all_voices = self.controller.get_voices()
        voice_names = [v['name'] for v in self.all_voices]
        self.voice_combo['values'] = voice_names
        self.voice_combo.current(0)
        self.controller.set_voice(self.all_voices[0]['id'])

    def _on_voice_selected(self, event):
        idx = self.voice_combo.current()
        selected_id = self.all_voices[idx]['id']
        self.controller.set_voice(selected_id)
        print(f"已切換人聲至: {self.all_voices[idx]['name']}")

if __name__ == "__main__":
    # Windows 下 multiprocessing 必須在 if __name__ == "__main__" 下運行
    multiprocessing.freeze_support()
    root = tk.Tk()
    app = AIVOGUI(root)
    
    # 當視窗關閉時，確保所有進程都被殺掉
    def on_closing():
        app._handle_stop()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()