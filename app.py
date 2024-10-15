import streamlit as st
import os
import streamlit.components.v1 as components

# Configurações da página
st.set_page_config(page_title="Conversas do WhatsApp", layout="wide")

# Título da aplicação
st.title("CRM WHATSAPP")

# Caminho da pasta onde as conversas estão armazenadas
folder_path = 'conversas'

# Função para ler os arquivos de conversa
def read_conversations(folder_path):
    conversations = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                content = file.read()
                conversations.append({'name': filename.replace('.txt', ''), 'content': content})
    return conversations

# Lê as conversas da pasta
conversations = read_conversations(folder_path)

# Função para gerar HTML dos cartões de conversa com a opção "Ver mais"
def generate_conversation_cards_html(conversations):
    html_cards = ""
    for i, conv in enumerate(conversations):
        # O conteúdo será truncado para exibir apenas os 100 primeiros caracteres
        card_html = f"""
        <div class="card" draggable="true" id="conv-{i}">
            <h4>{conv['name']}</h4>
            <p id="short-{i}">{conv['content'][:100]}... <button onclick="showFullConversation({i})">Ver mais</button></p>
            <p id="full-{i}" style="display:none;">{conv['content']} <button onclick="hideFullConversation({i})">Ver menos</button></p>
        </div>
        """
        html_cards += card_html
    return html_cards

# Gerar HTML dinâmico dos cards
cards_html = generate_conversation_cards_html(conversations)

# Criando o HTML com Drag and Drop e a funcionalidade de "Ver mais" / "Ver menos"
html_code = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Drag and Drop</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Sortable/1.14.0/Sortable.min.js"></script>
    <style>
        .container {{
            display: flex;
            justify-content: space-around;
            margin-top: 20px;
        }}
        .column {{
            width: 200px;
            min-height: 300px;
            padding: 10px;
            background-color: #f4f4f4;
            border: 1px solid #ddd;
        }}
        .card {{
            background-color: #fff;
            margin-bottom: 10px;
            padding: 10px;
            border: 1px solid #ccc;
            cursor: move;
        }}
    </style>
</head>
<body>

<div class="container">
    <div class="column" id="leads">
        <h3>Leads</h3>
        {cards_html} <!-- Inserir os cartões de conversas aqui -->
    </div>
    <div class="column" id="em-aberto">
        <h3>Em aberto</h3>
    </div>
    <div class="column" id="em-andamento">
        <h3>Em andamento</h3>
    </div>
    <div class="column" id="contrato-fechado">
        <h3>Contrato fechado</h3>
    </div>
</div>

<script>
    const columns = document.querySelectorAll('.column');

    columns.forEach(column => {{
        new Sortable(column, {{
            group: 'shared',
            animation: 150
        }});
    }});

    function showFullConversation(index) {{
        document.getElementById('short-' + index).style.display = 'none';
        document.getElementById('full-' + index).style.display = 'block';
    }}

    function hideFullConversation(index) {{
        document.getElementById('short-' + index).style.display = 'block';
        document.getElementById('full-' + index).style.display = 'none';
    }}
</script>

</body>
</html>
"""

# Inserindo o HTML na aplicação Streamlit
components.html(html_code, height=600)

# Rodapé
st.markdown("<hr>", unsafe_allow_html=True)
st.write("Desenvolvido com ❤️ por [Seu Nome]")  # Personalize seu nome aqui
