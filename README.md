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
10. [process-utils](packages/infrastructure_process_utils/README.md) - вспомогательные утилиты по управлению процессами.
11. [streaming](packages/infrastructure_streaming/README.md) - набор стриминговых клиентов

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
<summary>26.08.2026 - v0.68.0 - 54f05a</summary>

- infrastructure_progress==0.3.0

</details>
<details>
<summary>26.08.2026 - v0.67.0 - a16119</summary>

- infrastructure_progress==0.2.0

</details>
<details>
<summary>25.08.2026 - v0.65.0 - e6b670</summary>

- infrastructure_streaming==0.4.0

</details>
<details>
<summary>19.08.2026 - v0.64.0 - e0706d</summary>

- infrastructure_path_utils==0.4.0

</details>
<details>
<summary>19.08.2026 - v0.63.0 - 4ca740</summary>

- infrastructure_path_utils==0.3.0

</details>
<details>
<summary>14.08.2026 - v0.62.0 - 094b76</summary>

- infrastructure_streaming==0.3.0

</details>
<details>
<summary>12.08.2026 - v0.61.0 - 809ebe</summary>

- infrastructure_streaming==0.2.0

</details>
<details>
<summary>10.08.2026 - v0.58.0 - 123e07</summary>

- infrastructure_http_clients==0.8.0

</details>
<details>
<summary>10.08.2026 - v0.57.0 - 727bc6</summary>

- infrastructure_http_clients==0.7.0

</details>
<details>
<summary>08.08.2026 - v0.56.0 - 75b2e2</summary>

- infrastructure_http_clients==0.6.0
- infrastructure_server==0.19.0

</details>
<details>
<summary>05.08.2026 - v0.55.0 - 0ead0b</summary>

- infrastructure_other==0.10.0
- infrastructure_cli_utils==0.13.0

</details>
<details>
<summary>02.08.2026 - v0.54.0 - 11db61</summary>

- infrastructure_message_bus==0.10.0
- infrastructure_server==0.18.0

</details>
<details>
<summary>01.08.2026 - v0.53.0 - 58ef1d</summary>

- infrastructure_process_utils==0.6.0
- infrastructure_server==0.17.0

</details>
<details>
<summary>01.08.2026 - v0.52.0 - e7266e</summary>

- infrastructure_server==0.16.0

</details>
<details>
<summary>01.08.2026 - v0.51.0 - 725f4c</summary>

- infrastructure_server==0.15.0

</details>
<details>
<summary>01.08.2026 - v0.50.0 - 866f17</summary>

- infrastructure_server==0.14.0

</details>
<details>
<summary>31.07.2026 - v0.49.0 - 53d968</summary>

- infrastructure_cli_utils==0.12.0

</details>
<details>
<summary>31.07.2026 - v0.48.0 - dc675b</summary>

- infrastructure_message_bus==0.9.0

</details>
<details>
<summary>31.07.2026 - v0.47.0 - 6b94e2</summary>

- infrastructure_message_bus==0.8.0

</details>
<details>
<summary>30.07.2026 - v0.46.0 - a40c78</summary>

- infrastructure_builder==0.3.0

</details>
<details>
<summary>30.07.2026 - v0.44.0 - bcde77</summary>

- infrastructure_process_utils==0.5.0
- infrastructure_other==0.9.0

</details>
<details>
<summary>30.07.2026 - v0.43.0 - baf3fc</summary>

- infrastructure_other==0.8.0
- infrastructure_message_bus==0.7.0

</details>
<details>
<summary>30.07.2026 - v0.42.0 - fbe6ff</summary>

- infrastructure_message_bus==0.6.0

</details>
<details>
<summary>30.07.2026 - v0.41.0 - 1644cf</summary>

- infrastructure_other==0.7.0

</details>
<details>
<summary>30.07.2026 - v0.40.0 - 748850</summary>

- infrastructure_other==0.6.0

</details>
<details>
<summary>30.07.2026 - v0.39.0 - 62c5f3</summary>

- infrastructure_other==0.5.0

</details>
<details>
<summary>30.07.2026 - v0.38.0 - 15bde7</summary>

- infrastructure_other==0.4.0

</details>
<details>
<summary>30.07.2026 - v0.37.0 - f924d7</summary>

- infrastructure_cli_utils==0.11.0

</details>
<details>
<summary>30.07.2026 - v0.36.0 - 3f9b04</summary>

- infrastructure_cli_utils==0.10.0

</details>
<details>
<summary>30.07.2026 - v0.35.0 - 148f4b</summary>

- infrastructure_other==0.3.0

</details>
<details>
<summary>30.07.2026 - v0.34.0 - f0b106</summary>

- infrastructure_message_bus==0.5.0

</details>
<details>
<summary>30.07.2026 - v0.33.0 - 2a717f</summary>

- infrastructure_message_bus==0.4.0

</details>
<details>
<summary>30.07.2026 - v0.32.0 - 7e1bb9</summary>

- infrastructure_server==0.13.0

</details>
<details>
<summary>29.07.2026 - v0.31.0 - 212a73</summary>

- infrastructure_server==0.12.0

</details>
<details>
<summary>29.07.2026 - v0.30.0 - a785eb</summary>

- infrastructure_server==0.11.0

</details>
<details>
<summary>29.07.2026 - v0.29.0 - 998f03</summary>

- infrastructure_server==0.10.0

</details>
<details>
<summary>29.07.2026 - v0.28.0 - 6a1b7a</summary>

- infrastructure_cli_utils==0.9.0

</details>
<details>
<summary>29.07.2026 - v0.27.0 - 05c984</summary>

- infrastructure_message_bus==0.3.0

</details>
<details>
<summary>29.07.2026 - v0.26.0 - 93d6e0</summary>

- infrastructure_http_clients==0.5.0

</details>
<details>
<summary>27.07.2026 - v0.25.0 - 2e60ed</summary>

- infrastructure_cli_utils==0.8.0

</details>
<details>
<summary>27.07.2026 - v0.24.0 - e4c158</summary>

- infrastructure_builder==0.2.0

</details>
<details>
<summary>27.07.2026 - v0.23.0 - 8f8e56</summary>

- infrastructure_cli_utils==0.7.0

</details>
<details>
<summary>27.07.2026 - v0.22.0 - c8a5f4</summary>

- infrastructure_server==0.9.0

</details>
<details>
<summary>25.07.2026 - v0.21.0 - 7cf76c</summary>

- infrastructure_cli_utils==0.6.0

</details>
<details>
<summary>25.07.2026 - v0.20.0 - 9fb27e</summary>

- infrastructure_server==0.8.0
- infrastructure_process_utils==0.4.0

</details>
<details>
<summary>25.07.2026 - v0.19.0 - 6f09e7</summary>

- infrastructure_server==0.7.0

</details>
<details>
<summary>25.07.2026 - v0.18.0 - f7175a</summary>

- infrastructure_server==0.6.0

</details>
<details>
<summary>25.07.2026 - v0.17.0 - 8fd80d</summary>

- infrastructure_cli_utils==0.5.0

</details>
<details>
<summary>25.07.2026 - v0.15.0 - 2a6d79</summary>

- infrastructure_cli_utils==0.4.0
- infrastructure_server==0.5.0

</details>
<details>
<summary>24.07.2026 - v0.14.0 - 86970f</summary>

- infrastructure_cli_utils==0.3.0

</details>
<details>
<summary>24.07.2026 - v0.13.0 - bb7815</summary>

- infrastructure_cli_utils==0.2.0
- infrastructure_other==0.2.0
- infrastructure_settings_manager==0.2.0

</details>
<details>
<summary>24.07.2026 - v0.12.0 - bf3af9</summary>

- infrastructure_process_utils==0.3.0

</details>
<details>
<summary>24.07.2026 - v0.11.0 - 94f115</summary>

- infrastructure_process_utils==0.2.0

</details>
<details>
<summary>24.07.2026 - v0.9.0 - 43f609</summary>

- infrastructure_server==0.4.0

</details>
<details>
<summary>24.07.2026 - v0.8.0 - af41db</summary>

- infrastructure_http_clients==0.4.0

</details>
<details>
<summary>24.07.2026 - v0.7.0 - b2b71b</summary>

- infrastructure_http_clients==0.3.0

</details>
<details>
<summary>24.07.2026 - v0.6.0 - 661a7c</summary>

- infrastructure_http_clients==0.2.0

</details>
<details>
<summary>24.07.2026 - v0.5.0 - 799e49</summary>

- infrastructure_server==0.3.0

</details>
<details>
<summary>23.07.2026 - v0.4.0 - 71df99</summary>

- infrastructure_server==0.2.0

</details>
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