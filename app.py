import json

from flask import Flask, request, jsonify, render_template

with open('partners.json') as f:
    partners = json.load(f)


def get_partner_by_id(id): #получение партнера по id
    for partner in partners["partners"]:
        if partner["id"] == id:
            return partner
    return jsonify({"error": "Партнер с данным ID не найден"}), 404


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/partners', methods=['POST']) #Создание партнеров с бюджетами
def create_partner():
    partner_name = request.args.get('name')
    partner_budget = request.args.get('budget')
    partner = {
        "id": len(partners["partners"]) + 1,
        "name": partner_name,
        "budget": partner_budget,
        "spent_budget": 0
    }

    partners["partners"].append(partner)
    with open('partners.json', 'w') as file:
        json.dump(partners, file)
    return jsonify(partner), 200


@app.route('/api/partners/<int:id>', methods=['GET']) # Получение информации о партнере
def get_partner(id):
    get_partner_by_id(id)


@app.route('/api/partners/<int:id>/cashback', methods=['PUT']) #обновление данных о выплаченном кэшбэке
def update_cashback(id):
    data = request.json
    cashback_amount = data.get('cashback')
    partner = get_partner_by_id(id)
    partner['spent_budget'] = cashback_amount
    with open('partners.json', 'w') as file:
        json.dump(partners, file)
    return jsonify(partner), 200


if __name__ == '__main__':
    app.run(port=8080)
