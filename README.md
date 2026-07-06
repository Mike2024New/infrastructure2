# infrastructure

🧩 Монорепозиторий переиспользуемых утилит для Python-проектов. Централизованное управление, модульная установка.

---

## О проекте

Этот монорепозиторий содержит общие компоненты, которые используются во многих моих проектах. Вместо того чтобы
дублировать код в каждом проекте, он вынесен сюда и подключается как зависимость.

Этот монорепозиторий логическое развитие пакета [infrastructure](https://github.com/Mike2024New/infrastructure), который
разрастался быстрее чем я думал. И в итоге получилась такая ситуация, когда ради одного незначительного компонента (
например шины сообщений), нужно было тащить огромный зоопарк из зависимостей (requests, typer, pydantic и так далее).
Теперь подключаются только реально необходимые пакеты под конкретный проект.

---

## Требования

- Python >= 3.12

> Пакет `infrastructure` предназначен для работы с виртуальным окружением в корневом каталоге, от этого зависит работа
> всех встроенных компонентов. Папку с виртуальным окружением необходимо называть `.venv`.

---

## Компоненты

1. [MessageBus](packages/infrastructure_message_bus/README.md) - шина сообщений - общение приложений, логирование.
2. [GitClient](packages/infrastructure_git_client/README.md) - простой git клиент, для автоматизации отправки обновления
   компонентов в репозиторий git.
3. [PathUtils](packages/infrastructure_path_utils/README.md) - набор утилит для работы с путями, например поиск
   корневого пути проекта.
4. [Builder](packages/infrastructure_builder/README.md) - сборщик исполняемых файлов (.exe, .bin).
5. [HttpClients](packages/infrastructure_http_clients/README.md) - http клиент, для выполнения запросов, например
   загрузка файлов.
6. [cli_utils](packages/infrastructure_cli_utils/README.md) - cli утилиты (typer, консольный интерфейс и так далее).
7. [settings-manager](packages/infrastructure_settings_manager/README.md) - менеджер настроек (pydantic модели
   конфигураций,json, .env).
8. [server](packages/infrastructure_server/README.md) - запуск сервера Fastapi.
9. [Other](packages/infrastructure_other/README.md) - прочие утилиты, которые не вошли ни в одну из категорий.

---

## Установка

> Это полная установка включает в себя все пакеты из раздела [комоненты](#компоненты), инструкцию по установке
> конкретного пакета см. в разделе, но общий синтаксис ссылки на пакет из pyproject.toml такой:

```text
<package-name> @git+https://github.com/Mike2024New/infrastructure2.git@main#subdirectory=packages/<package-path>
```

Если планируется использовать все пакеты то:

Для toml:

```text
"infrastructure2 @ git+https://github.com/Mike2024New/infrastructure2.git"
```

Для прямой uv установки:

```bash
uv add git+https://github.com/Mike2024New/infrastructure2.git
```

Для pip установки:

```bash
# установка в режиме editable пакета.
pip install -e "git+https://github.com/Mike2024New/infrastructure2.git#egg=infrastructure2"
```

---

## 📝 История изменений

<div id="change-history">
<details>
<summary>03.07.2026 - v0.2.0 - 6449a8</summary>

- infrastructure_path_utils==0.2.0
- infrastructure_message_bus==0.2.0

</details>
<details>
<summary>03.07.2026 - v0.1.0 - e0e5b8</summary>

- infrastructure_other==0.1.0

</details>
<details>
<summary>03.07.2026 - v0.1.0 - f9b299</summary>

- infrastructure_git_client==0.1.0

</details>
</div>

---

## 📜Лицензии

* Этот проект распространяется под лицензией MIT. Подробнее в файле [LICENSE](LICENSE).

---

## Примечания

1. Версии в pyproject.toml изменяются инкрементально на каждый коммит (даже на незначительное изменение). До тех пор
   пока действует обратная совместимость с сервисами которые используют этот пакет, меняются только минорные версии.
2. Сообщения в коммитах формируются автоматически, с помощью uuid4. Связь версии с коммитом см.
   в [история изменений](#-история-изменений).