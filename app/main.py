from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

inventory_db = [
    {"id": 1, "name": "Laptop Server", "quantity": 10},
    {"id": 2, "name": "Router Switch", "quantity": 5}
]

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "UP", "service": "inventory-service"}), 200

@app.route('/api/v1/inventory', methods=['GET'])
def get_inventory():
    return jsonify({"success": True, "data": inventory_db}), 200

@app.route('/api/v1/inventory', methods=['POST'])
def add_inventory():
    data = request.get_json()
    if not data or 'name' not in data or 'quantity' not in data:
        return jsonify({"success": False, "message": "Invalid payload"}), 400
    
    new_item = {
        "id": len(inventory_db) + 1,
        "name": data['name'],
        "quantity": data['quantity']
    }
    inventory_db.append(new_item)
    return jsonify({"success": True, "data": new_item}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)