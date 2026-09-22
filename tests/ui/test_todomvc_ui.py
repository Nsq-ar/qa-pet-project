"""
Пара UI-тестов через Playwright на публичной демо-странице TodoMVC
(https://demo.playwright.dev/todomvc/).
"""

import allure
import pytest
from playwright.sync_api import Page, expect

TODOMVC_URL = "https://demo.playwright.dev/todomvc/"


@allure.epic("TodoMVC demo")
@allure.feature("Todo list")
@pytest.mark.ui
class TestTodoMvcUi:

    @allure.title("Добавление новой задачи в список")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_new_todo_item(self, page: Page):
        with allure.step("Открываем страницу TodoMVC"):
            page.goto(TODOMVC_URL)

        with allure.step("Добавляем новую задачу"):
            new_todo_input = page.get_by_placeholder("What needs to be done?")
            new_todo_input.fill("Купить молоко")
            new_todo_input.press("Enter")

        with allure.step("Проверяем, что задача появилась в списке"):
            todo_items = page.get_by_test_id("todo-item")
            expect(todo_items).to_have_count(1)
            expect(todo_items.first).to_contain_text("Купить молоко")

    @allure.title("Отметка задачи как выполненной")
    @allure.severity(allure.severity_level.NORMAL)
    def test_mark_todo_as_completed(self, page: Page):
        with allure.step("Открываем страницу и добавляем задачу"):
            page.goto(TODOMVC_URL)
            new_todo_input = page.get_by_placeholder("What needs to be done?")
            new_todo_input.fill("Написать автотест")
            new_todo_input.press("Enter")

        with allure.step("Отмечаем задачу как выполненную"):
            todo_item = page.get_by_test_id("todo-item").first
            todo_item.get_by_role("checkbox").check()

        with allure.step("Проверяем, что задача получила статус 'completed'"):
            expect(todo_item).to_have_class("completed")
