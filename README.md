# Автотест: Проверка футера only.digital

Проверяет наличие футера и ключевых элементов на сайте [https://only.digital/](https://only.digital/).

## Функционал
- Проверка отображения футера.
- Проверка логотипа, ссылки "Контакты", email, соцсетей, копирайта.
- Проверка на нескольких страницах: `/`, `/about`, `/services`.

## Технологии
- Python
- Selenium
- Pytest

## Запуск
```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск тестов
pytest test_footer.py -v