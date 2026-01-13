import json
import os
import hashlib

class ProgressManager:
    def __init__(self, storage_file="progress.json"):
        self.storage_file = storage_file
        self.progress_data = self._load_all_progress()

    def _load_all_progress(self):
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _get_file_id(self, file_path):
        # 建立檔案路徑的唯一 Hash
        return hashlib.md5(file_path.encode('utf-8')).hexdigest()

    def save_progress(self, file_path, index):
        file_id = self._get_file_id(file_path)
        self.progress_data[file_id] = {
            "path": file_path,
            "last_index": index
        }
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump(self.progress_data, f, indent=4)

    def get_progress(self, file_path):
        file_id = self._get_file_id(file_path)
        return self.progress_data.get(file_id, {}).get("last_index", 0)