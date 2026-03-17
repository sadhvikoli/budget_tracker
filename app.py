from flask import Flask, request, jsonify
import budget_tracker
app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome aboard Captain! 🏴‍☠️'


@app.route('/balance')
def balance():
    balance, data = budget_tracker.compute_budget_data()
    return {
        "balance": balance,
        "categories": data
    }

@app.route('/add-expense', methods=['POST'])
def add_expense():
    try:
        data = request.get_json()

        date = data.get("date")
        category = data.get("category")
        amount = data.get("amount")

        if not date or not category or amount is None:
            return jsonify({"error": "Missing required fields"}), 400

        if not isinstance(amount, int) or amount <= 0:
            return jsonify({"error": "Amount must be a positive integer"}), 400

        category = category.lower()

        balance, categories = budget_tracker.compute_budget_data()

        if category not in categories:
            return jsonify({"error": "Invalid category"}), 400

        remaining = categories[category]["remaining"]

        if amount > remaining:
            return jsonify({
                "error": f"Amount exceeds remaining budget ({remaining}) for {category}"
            }), 400

        budget_tracker.write_csv_from_json({
            "date": date,
            "category": category,
            "amount": amount
        })

        return jsonify({
            "message": "Expense added successfully 🏴‍☠️",
            "remaining_after": remaining - amount
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)


