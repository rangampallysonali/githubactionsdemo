import requests
import random
import time

BASE_URL = "http://localhost:4000"

def wait_for_app(timeout=20):
    start = time.time()
    while time.time() - start < timeout:
        try:
            res = requests.get(BASE_URL + "/")
            if res.status_code == 200:
                return
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)
    raise Exception("App did not become ready in time")

def setup_module(module):
    wait_for_app()

def test_home():
    res = requests.get(BASE_URL + "/")
    assert res.status_code == 200
    assert "Book API" in res.text

def test_add_book():
    book_id = random.randint(1000, 9999)
    data = {
        "id": book_id,
        "title": "Docker Book",
        "author": "You"
    }

    res = requests.post(BASE_URL + "/books", json=data)
    assert res.status_code == 200
    assert res.json()["message"] == "Book added"

def test_get_books():
    res = requests.get(BASE_URL + "/books")
    assert res.status_code == 200
    assert isinstance(res.json(), list)

def test_delete_book():
    book_id = random.randint(10000, 99999)
    data = {
        "id": book_id,
        "title": "To Delete",
        "author": "You"
    }
    requests.post(BASE_URL + "/books", json=data)

    res = requests.delete(BASE_URL + f"/books/{book_id}")
    assert res.status_code == 200
    assert res.json()["message"] == "Book deleted"