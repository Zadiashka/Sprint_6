def test_smoke(driver):
    driver.get("https://qa-scooter.praktikum-services.ru")
    assert driver.current_url.startswith("http")
