# test_footer.py
"""
Автотест: Проверка наличия футера и его элементов на сайте https://only.digital/

Проверяет:
- Отображение футера.
- Наличие логотипа Only.
- Наличие ссылки "Контакты".
- Наличие email в формате mailto.
- Наличие иконок социальных сетей.
- Наличие копирайта.

Страницы: главная, /about, /services.

Основано на принципах из книги "Совершенный код" — читаемость, надежность, простота.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


# Список тестируемых URL
URLS = [
    "https://only.digital/",
    "https://only.digital/about",
    "https://only.digital/services"
]


@pytest.fixture(scope="module")
def driver():
    """
    Фикстура: создаёт один экземпляр драйвера на весь модуль.
    Использует headless-режим для эффективности.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Уберите для отладки
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    yield driver
    driver.quit()


def find_footer(driver):
    """
    Находит футер на странице.
    :return: WebElement или None
    """
    try:
        footer = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.TAG_NAME, "footer"))
        )
        return footer
    except TimeoutException:
        return None


def check_logo(footer):
    """Проверяет наличие логотипа Only в футере."""
    try:
        logo = footer.find_element(By.CSS_SELECTOR, "footer img[alt='Only']")
        return logo.is_displayed()
    except NoSuchElementException:
        return False


def check_contact_link(footer):
    """Проверяет наличие ссылки 'Контакты'."""
    try:
        link = footer.find_element(By.XPATH, ".//a[text()='Контакты']")
        return link.is_displayed() and link.get_attribute("href").startswith("https")
    except NoSuchElementException:
        return False


def check_email(footer):
    """Проверяет наличие email с mailto."""
    try:
        email_link = footer.find_element(By.XPATH, ".//a[contains(@href, 'mailto:')]")
        email_href = email_link.get_attribute("href")
        return email_link.is_displayed() and "info@" in email_href
    except NoSuchElementException:
        return False


def check_social_icons(footer):
    """Проверяет наличие хотя бы одной иконки соцсети."""
    try:
        icons = footer.find_elements(By.CSS_SELECTOR, ".socials a")
        return len(icons) > 0
    except NoSuchElementException:
        return False


def check_copyright(footer):
    """Проверяет наличие текста копирайта."""
    try:
        copyright_text = footer.find_element(By.XPATH, ".//*[contains(text(), '©')]")
        return copyright_text.is_displayed()
    except NoSuchElementException:
        return False


@pytest.mark.parametrize("url", URLS)
def test_footer_and_elements(driver, url):
    """
    Параметризованный тест: проверяет футер и его элементы на каждой странице.
    """
    print(f"\nТестирование страницы: {url}")
    driver.get(url)

    # 1. Проверка наличия футера
    footer = find_footer(driver)
    assert footer is not None, f"Футер не найден или не отображается на {url}"

    # 2. Проверка элементов
    assert check_logo(footer), "Логотип Only отсутствует в футере"
    assert check_contact_link(footer), "Ссылка 'Контакты' отсутствует или невалидна"
    assert check_email(footer), "Email (mailto) отсутствует или некорректен"
    assert check_social_icons(footer), "Иконки социальных сетей отсутствуют"
    assert check_copyright(footer), "Текст копирайта отсутствует"