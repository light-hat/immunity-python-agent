import json
import os


# class Config(object):
#     def __init__(self):
#         base_dir = os.path.dirname(os.path.abspath(__file__))
#         file_path = os.path.join(base_dir, '../config.json')
#         with open(file_path, 'rb') as config:
#             data = config.read()
#             self.config = json.loads(data)

#     def get(self, key, default=None):
#         return self.config.get(key, default)

#     def set(self, key, value):
#         self.config[key] = value

class Config(object):
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(base_dir, '../config.json')

        if not os.path.exists(self.file_path):
            # создаём пустой конфиг
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=2)

        with open(self.file_path, 'r', encoding='utf-8') as f:
            try:
                self.config = json.load(f)
            except json.JSONDecodeError:
                # если файл пустой или битый — используем пустой словарь
                self.config = {}

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self._save()

    def _save(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
