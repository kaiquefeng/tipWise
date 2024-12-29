from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da API OpenAI

# Inicializar Flask
app = Flask(__name__)

@app.route('/generate-itinerary', methods=['POST'])
def generate_itinerary():
    try:
        # Receber dados do usuário
        data = request.json
        destination = data.get("destination", "Desconhecido")
        days = data.get("days", 3)
        budget = data.get("budget", "médio")
        interests = data.get("interests", "turismo geral")

        # Estrutura de mensagens para a API
        messages = [
            {"role": "system", "content": "Você é um planejador de viagens experiente. Crie respostas em JSON estruturado."},
            {"role": "user", "content": f"Crie um itinerário de viagem detalhado para {days} dias em {destination}. Orçamento: {budget}. Interesses principais: {interests}. O resultado deve ser JSON com um plano diário estruturado."}
        ]

        # Chamada para a API OpenAI
        response = openai.chat.completions.create(
            model="gpt-4",  # ou "gpt-3.5-turbo"
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )

        # Extração do texto gerado
        itinerary_text = response.choices[0].message.content.strip()

        try:
            itinerary_json = eval(itinerary_text)  # Use eval ou json.loads se o texto for um JSON válido
        except Exception:
            itinerary_json = {"error": "A saída da OpenAI não estava no formato JSON esperado.", "raw_output": itinerary_text}

        return jsonify({
            "success": True,
            "destination": destination,
            "itinerary": itinerary_json
        })

    except openai.error.OpenAIError as oe:
        return jsonify({
            "success": False,
            "error": f"Erro na API OpenAI: {str(oe)}"
        }), 500
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Erro interno: {str(e)}"
        }), 500

# Rodar o servidor
if __name__ == '__main__':
    app.run(debug=True)