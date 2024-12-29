from flask import Flask, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da API OpenAI
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Configuração da porta
port = int(os.getenv('PORT', 8080))
env = os.getenv('FLASK_ENV', 'production')

# Inicializar Flask
app = Flask(__name__)
app.config['ENV'] = env

# Configurar logging do Flask
app.logger.handlers = []
app.logger.addHandler(logging.StreamHandler())
app.logger.setLevel(logging.DEBUG)

@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "message": "Service is running"
    })

@app.route('/generate-itinerary', methods=['POST'])
def generate_itinerary():
    try:
        # Verificar se há dados JSON na requisição
        if not request.is_json:
            return jsonify({
                "success": False,
                "error": "Request must be JSON"
            }), 400

        # Receber dados do usuário com validação
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "Empty request body"
            }), 400

        # Validar campos obrigatórios
        destination = data.get("destination")
        if not destination:
            return jsonify({
                "success": False,
                "error": "Destination is required"
            }), 400

        # Pegar outros campos com valores padrão
        days = data.get("days", 3)
        budget = data.get("budget", "médio")
        interests = data.get("interests", "turismo geral")

        # Estrutura de mensagens para a API
        messages = [
            {"role": "system", "content": "Você é um planejador de viagens experiente. Crie respostas em JSON estruturado."},
            {"role": "user", "content": f"Crie um itinerário de viagem detalhado para {days} dias em {destination}. Orçamento: {budget}. Interesses principais: {interests}. O resultado deve ser JSON com um plano diário estruturado."}
        ]

        # Chamada para a API OpenAI
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )

        # Extração do texto gerado
        itinerary_text = response.choices[0].message.content.strip()

        try:
            import json
            itinerary_json = json.loads(itinerary_text)
        except json.JSONDecodeError:
            return jsonify({
                "success": False,
                "error": "Failed to parse OpenAI response as JSON",
                "raw_output": itinerary_text
            }), 500

        return jsonify({
            "success": True,
            "destination": destination,
            "itinerary": itinerary_json
        })

    except Exception as e:
        logger.exception("Error in generate_itinerary")
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500

# Garantir que a aplicação está pronta para o Gunicorn
application = app

if __name__ == '__main__':
    if env == 'development':
        app.run(host='0.0.0.0', port=port, debug=True)
    else:
        app.run(host='0.0.0.0', port=port, debug=False)