"""
Пара тестов на публичное демо-API Swagger Petstore
(https://petstore.swagger.io/v2), без авторизации.
"""

import random

import allure
import pytest


@allure.epic("Swagger Petstore")
@allure.feature("Pet")
@pytest.mark.api
class TestPetstoreApi:

    @allure.title("Создание питомца и получение его по id")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_and_get_pet(self, api_session, api_base_url):
        pet_id = random.randint(1_000_000, 9_999_999)
        payload = {
            "id": pet_id,
            "name": "doggie",
            "status": "available",
        }

        with allure.step(f"Создаём питомца с id={pet_id}"):
            create_response = api_session.post(f"{api_base_url}/pet", json=payload)
            assert create_response.status_code == 200, create_response.text

        with allure.step("Получаем созданного питомца по id"):
            get_response = api_session.get(f"{api_base_url}/pet/{pet_id}")
            assert get_response.status_code == 200
            body = get_response.json()

        with allure.step("Проверяем данные питомца"):
            assert body["id"] == pet_id
            assert body["name"] == "doggie"
            assert body["status"] == "available"

        with allure.step("Удаляем питомца (очистка тестовых данных)"):
            delete_response = api_session.delete(f"{api_base_url}/pet/{pet_id}")
            assert delete_response.status_code == 200

    @allure.title("Запрос несуществующего питомца возвращает 404")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_nonexistent_pet_returns_404(self, api_session, api_base_url):
        nonexistent_pet_id = 0

        with allure.step(f"Запрашиваем питомца с заведомо несуществующим id={nonexistent_pet_id}"):
            response = api_session.get(f"{api_base_url}/pet/{nonexistent_pet_id}")

        with allure.step("Проверяем, что API вернул 404 Not Found"):
            assert response.status_code == 404

    @allure.title("Поиск питомцев по статусу 'available'")
    @allure.severity(allure.severity_level.NORMAL)
    def test_find_pets_by_status_available(self, api_session, api_base_url):
        with allure.step("Запрашиваем список питомцев со статусом available"):
            response = api_session.get(
                f"{api_base_url}/pet/findByStatus", params={"status": "available"}
            )
            assert response.status_code == 200
            pets = response.json()

        with allure.step("Проверяем, что список не пуст и у всех статус available"):
            assert isinstance(pets, list)
            assert len(pets) > 0
            assert all(pet.get("status") == "available" for pet in pets)
