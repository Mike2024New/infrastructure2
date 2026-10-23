from pydantic import BaseModel, Field


class DownloadTask(BaseModel):
    """Схема с формированием задания для загрузки файла"""
    url: str = Field(description='целевой url')
    relative_path_file: str = Field(description='Относительный путь, например resources/models')
    label: str = Field(description='название файла, отображаемое при загрузке (шильдик)')

    def get_downloader(self, root_dir) -> dict:
        """
        Получение аргументов для download_file (**)
        :param root_dir: корень проекта или той папки куда планируется качать (достраивает путь, глобальный + относительный)
        """
        return {
            "url": self.url,
            "file_path": root_dir / self.relative_path_file,
            "label": self.label,
        }


if __name__ == '__main__':
    data = {
        "assets": [
            {
                "label": "tiny/model.bin",
                "relative_path_file": "srv_stt/resources/models/tiny/model.bin",
                "url": "https://huggingface.co/Systran/faster-whisper-tiny/resolve/main/model.bin"
            },
            {
                "label": "gemma-3-1b-it-Q4_K_M.gguf",
                "relative_path_file": "srv_llm/resources/models/gemma-3-1b-it-Q4_K_M.gguf",
                "url": "https://huggingface.co/lmstudio-community/gemma-3-1b-it-GGUF/resolve/main/gemma-3-1b-it-Q4_K_M.gguf"
            }
        ]
    }

    # сборка заданий на загрузку из json
    download_tasks = [DownloadTask.model_validate(asset) for asset in data["assets"]]
