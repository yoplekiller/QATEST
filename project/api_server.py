from flask import Flask, jsonify
from urllib3 import request

app = Flask(__name__)

cart=[]

@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    data = request.json
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    if not product_id:
        return jsonify({"success": False, "message": "product_id is required"}), 400

    for item in cart:
        if item["product_id"] == product_id:
            item["quantity"] += quantity
            return jsonify({"success": True, "cart": cart}), 200

    cart.append({"product_id": product_id, "quantity": quantity})
    return jsonify({"success": True, "cart": cart}), 200

@app.route('/cart/remove', methods=['POST'])
def remove_from_cart():
    data = request.json
    product_id = data.get("product_id")

    if not product_id:
        return jsonify({"success": False, "message": "product_id is required"}), 400

    global cart
    cart = [item for item in cart if item["product_id"] != product_id]

    return  jsonify({"success": True, "cart": cart}), 200

if __name__ == '__main__':
    app.run(debug=True)





