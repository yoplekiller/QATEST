from project.config import API_BASE_URL
import json
import requests
from tests.api.get_product_id import get_product_id

def test_add_to_cart():
    product_id = get_product_id()

    if not product_id:
        print("Error: product_id is None")
        return

    payload = {"product_id": product_id, "quantity": 1}
    headers = {"Content-Type": "application/json"}

    response = requests.post(f"{API_BASE_URL}/cart/add", data = json.dumps(payload), headers=headers)

    print(f"Response: {response.json()}")
    assert response.status_code == 200, f"Error: {response.text}"
    assert response.json()["success"] == True, "Failed to add product cart"



