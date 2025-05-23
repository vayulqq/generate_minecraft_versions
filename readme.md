# Генератор ссылок на JAR-файлы Minecraft

Этот Python-скрипт собирает информацию о всех версиях Minecraft (release, snapshot, alpha, beta и других) с официального манифеста Mojang и создаёт таблицу с прямыми ссылками на скачивание серверных и клиентских JAR-файлов. Таблица сохраняется в файл `versions.md` в папке `temp` в формате Markdown, готовом для использования на GitHub.

## Особенности
- **Полное покрытие версий**: Обрабатывает все типы версий Minecraft (release, snapshot, old_alpha, old_beta и другие).
- **Асинхронные запросы**: Использует `aiohttp` для быстрого и параллельного получения данных.
- **Устойчивость к ошибкам**: Включает повторные попытки при сбоях сети и обработку отсутствующих JAR-файлов.
- **Сортировка**: Версии упорядочены от самой новой к самой старой по дате релиза.
- **Готовый Markdown**: Генерирует красивую таблицу в формате Markdown с колонками:
  - Версия Minecraft
  - URL для скачивания серверного JAR
  - URL для скачивания клиентского JAR
- **Производительность**: Ограничивает количество одновременных запросов, чтобы не перегружать сервер Mojang.

## Требования
- Python 3.7+
- Библиотека `aiohttp` для асинхронных HTTP-запросов

## Установка
1. Убедитесь, что у вас установлен Python 3.7 или выше.
2. Установите необходимую библиотеку:
   ```bash
   pip install aiohttp
   ```
3. Скачайте скрипт `generate_minecraft_versions.py` из этого репозитория.

## Использование
1. Поместите скрипт `generate_minecraft_versions.py` в любую папку.
2. Запустите скрипт командой:
   ```bash
   python generate_minecraft_versions.py
   ```
3. После выполнения скрипт создаст папку `temp` (если она ещё не существует) и сохранит в ней файл `versions.md` с таблицей всех версий Minecraft.

## Пример вывода
Файл `temp/versions.md` будет выглядеть примерно так:

```markdown
# Minecraft Version Download Links

| Minecraft Version | Server Jar Download URL | Client Jar Download URL |
|-------------------|-------------------------|-------------------------|
| 1.21.1            | https://.../server.jar  | https://.../client.jar  |
| 1.21              | https://.../server.jar  | https://.../client.jar  |
| 1.20.6            | https://.../server.jar  | https://.../client.jar  |
| a1.0.5            | Not found               | Not found               |
| b1.7.3            | Not found               | https://.../client.jar  |
```

- **Minecraft Version**: Идентификатор версии (например, `1.21.1`, `a1.0.5`, `b1.7.3`).
- **Server Jar Download URL**: Прямая ссылка на серверный JAR или `Not found`, если файл недоступен.
- **Client Jar Download URL**: Прямая ссылка на клиентский JAR или `Not found`, если файл недоступен.

## Как работает скрипт
1. Запрашивает манифест версий с `https://launchermeta.mojang.com/mc/game/version_manifest.json`.
2. Асинхронно загружает JSON-файлы для каждой версии, чтобы извлечь ссылки на JAR-файлы.
3. Сортирует версии по дате выпуска (от новых к старым).
4. Создаёт файл `versions.md` с таблицей в папке `temp`.

## Замечания
- Скрипт использует асинхронные запросы с ограничением в 10 одновременных соединений, чтобы избежать перегрузки сервера Mojang.
- Если JAR-файл для версии отсутствует, в таблице указывается `Not found`.
- Для повторных запусков манифест версий кэшируется, чтобы сократить время выполнения.
- Для просмотра .md файлов вы можете использовать [dillinger.io](https://dillinger.io).

## Контакты
Если у вас есть вопросы или предложения, создайте issue в этом репозитории или свяжитесь со мной через GitHub.
