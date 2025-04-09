from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/avaliar', methods=['POST'])
def avaliar_personalidade():
    dados = request.get_json()
    respostas = dados.get('respostas', [])

    categorias = {
        "abertura": [],
        "consciencia": [],
        "extroversao": [],
        "amabilidade": [],
        "neuroticismo": []
    }

    for resposta in respostas:
        categoria = resposta.get("categoria")
        valor = resposta.get("valor")
        if categoria in categorias:
            categorias[categoria].append(valor)

    resultados = {cat: sum(valores) / len(valores) if valores else 0 for cat, valores in categorias.items()}

    interpretacoes = {
        "abertura": {
            "alta": "Você é uma pessoa criativa, curiosa e aberta a novas ideias e experiências.",
            "media": "Você aprecia novas ideias, mas também valoriza a tradição.",
            "baixa": "Você prefere o que é familiar e tende a evitar mudanças."
        },
        "consciencia": {
            "alta": "Você é uma pessoa organizada, responsável e cumpre seus compromissos.",
            "media": "Você se esforça para ser organizada, mas também sabe ser flexível.",
            "baixa": "Você pode ter dificuldades com organização e prazos."
        },
        "extroversao": {
            "alta": "Você é uma pessoa sociável, enérgica e gosta de estar com outras pessoas.",
            "media": "Você se sente confortável tanto em grupos quanto sozinha.",
            "baixa": "Você é mais reservada e prefere ambientes calmos."
        },
        "amabilidade": {
            "alta": "Você é uma pessoa gentil, empática e valoriza o bem-estar dos outros.",
            "media": "Você é geralmente cooperativa, mas sabe se impor quando necessário.",
            "baixa": "Você pode ser mais direta, competitiva ou cética em relação aos outros."
        },
        "neuroticismo": {
            "alta": "Você tende a experimentar emoções intensas, como ansiedade ou irritação.",
            "media": "Você sente emoções negativas ocasionalmente, mas lida bem com elas.",
            "baixa": "Você é emocionalmente estável e raramente se sente sobrecarregado."
        }
    }

    dicas = {
        "abertura": {
            "alta": "Continue explorando novas ideias e experiências, mas cuidado para não perder o foco.",
            "media": "Experimente sair um pouco da rotina com atividades criativas ou culturais.",
            "baixa": "Tente se expor gradualmente a novas experiências ou pontos de vista diferentes."
        },
        "consciencia": {
            "alta": "Mantenha sua organização, mas permita-se ser flexível quando necessário.",
            "media": "Use listas ou metas curtas para manter o foco sem se sobrecarregar.",
            "baixa": "Experimente usar planejadores ou alarmes para ajudar na organização do dia a dia."
        },
        "extroversao": {
            "alta": "Continue se conectando com os outros, mas lembre-se de respeitar os momentos de silêncio.",
            "media": "Equilibre momentos sociais e de introspecção para manter seu bem-estar.",
            "baixa": "Tente participar de grupos pequenos ou ambientes seguros para socializar aos poucos."
        },
        "amabilidade": {
            "alta": "Continue sendo gentil, mas estabeleça limites quando necessário.",
            "media": "Seja empática, mas firme ao comunicar suas necessidades.",
            "baixa": "Pratique escuta ativa e empatia em conversas simples no dia a dia."
        },
        "neuroticismo": {
            "alta": "Considere técnicas de respiração, mindfulness ou buscar apoio terapêutico.",
            "media": "Continue cuidando da sua saúde mental com equilíbrio e autocuidado.",
            "baixa": "Use sua estabilidade emocional para apoiar os outros em momentos difíceis."
        }
    }

    perfil_completo = {}

    for cat, media in resultados.items():
        percentual = (media / 5) * 100  # Convertendo para porcentagem (0-100%)
        if media >= 4:
            nivel = "alta"
        elif media >= 2.5:
            nivel = "media"
        else:
            nivel = "baixa"
        perfil_completo[cat] = {
            "pontuacao": round(percentual, 1),  # Ex: 80.0%
            "interpretacao": interpretacoes[cat][nivel],
            "dica": dicas[cat][nivel]
        }

    top_2 = dict(sorted(perfil_completo.items(), key=lambda item: item[1]["pontuacao"], reverse=True)[:2])
    return jsonify({"perfil_destacado": top_2})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
