from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO = os.path.join(BASE_DIR, "data", "medicamentos.json")


def carregar_dados():
    if not os.path.exists(ARQUIVO):
        return []

    try:
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except json.JSONDecodeError:
        return []


def salvar_dados(Medicamentos):
    os.makedirs(os.path.dirname(ARQUIVO), exist_ok=True)
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(Medicamentos, arquivo, indent=4, ensure_ascii=False)


@app.route("/medicamentos", methods=["GET"])
def listar_medicamentos():
    Medicamentos = carregar_dados()
    return jsonify(Medicamentos)


@app.route("/medicamentos", methods=["POST"])
def adicionar_medicamento():
    Medicamentos = carregar_dados()
    novo = request.json

    if not novo or not novo.get("nome") or not novo.get("horario"):
        return jsonify({"erro": "Dados inválidos"}), 400

    Medicamentos.append(novo)
    salvar_dados(Medicamentos)

    return jsonify({"mensagem": "Medicamento adicionado com sucesso"}), 201


@app.route("/medicamentos/<nome>", methods=["DELETE"])
def remover_medicamento(nome):
    Medicamentos = carregar_dados()
    Medicamentos = [m for m in Medicamentos if m["nome"].lower() != nome.lower()]

    salvar_dados(Medicamentos)

    return jsonify({"mensagem": "Medicamento removido com sucesso"})


if __name__ == "__main__":
    app.run(debug=True)