from huggingface_hub import utils as hf_utils
from huggingface_hub import HfApi
from loguru import logger


class Sha256Checker:
    """Проверка sha256 файлов перед загрузкой для доступных api"""

    @classmethod
    def check(cls, url: str, sha256: str):
        # цепочка методов для получения sha256
        if url.startswith('https://huggingface.co/'):
            return cls.hf_check_sha256(url=url, sha256=sha256)
        ...  # другие проверки
        return None

    @staticmethod
    def hf_check_sha256(url: str, sha256: str) -> bool | None:
        """
        Проверка файлов для hugging_face
        Парсинг url и получение sha256, вернет True/False в зависимости от результата
        :param url: url файла или модели (ключевое это должен быть именно файл)
        :param sha256: исходный sha256 (прописанный например в json или sql)
        :return: True/False/None -  если sha не был получен, например api отвалился или сбой сети, или прилетели волшебники на голубом вертолёте
        """
        try:
            res = hf_utils.parse_hf_uri(url)
        except Exception as err:
            logger.error(f'Ошибка парсинга hf url : {err}')  # переделать на логирование
            return None

        try:
            api = HfApi()
            info = api.model_info(
                repo_id=res.id,
                files_metadata=True,  # указать что данные получаются именно о файле
            )
        except hf_utils.HfHubHTTPError as err:
            # Ошибка сети, 404 или 401. Логируем и пропускаем проверку.
            logger.error(f"Не удалось получить метаданные для {url}: {err}")
            return None

        for sibling in info.siblings:
            if sibling.rfilename == res.path_in_repo:
                if sibling.lfs:
                    return sha256 == sibling.lfs.sha256
        logger.error(f'Не удалось получить sha256 для {url}')  # переделать на логирование
        return None


if __name__ == '__main__':
    result = Sha256Checker.check(
        url='https://huggingface.co/lmstudio-community/gemma-3-1b-it-GGUF/resolve/main/gemma-3-1b-it-Q4_K_M.gguf',
        sha256='8d78d9d059a7605c401c105e169e0b08e9f0edc603ceb842f1c4bbb834296d17',
    )
    print(result)
