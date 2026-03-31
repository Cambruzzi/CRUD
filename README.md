# 📦 Sistema de Gestão de Produtos (CRUD API + SPA)

Um sistema completo de gerenciamento de produtos (CRUD) com autenticação, upload de imagens e persistência em banco de dados. Desenvolvido com foco em **Arquitetura Limpa** e boas práticas de mercado.

## 🎯 O Desafio
Criar um CRUD de cadastro de produto, com autenticação e persistência no banco de dados, contendo os seguintes campos obrigatórios: `nome`, `código`, `valor`, `excluído`, `data de alteração` e `imagem`. O sistema deve expor endpoints REST e estar disponível online.

## Site online
```bash
https://leocambruzzi.pythonanywhere.com/
```

## ✨ Funcionalidades
* **Autenticação:** Login e Registro com geração de Token de Acesso (Bearer Token).
* **Gestão de Produtos:** Criação, Listagem, Edição e Deleção de itens.
* **Soft Delete:** Exclusão lógica (o registro é inativado e ocultado da interface, mantendo a integridade do histórico no banco de dados).
* **Upload de Mídia:** Suporte nativo para envio de fotos dos produtos via requisições Multipart (FormData).
* **Frontend SPA:** Single Page Application construída com Vanilla JavaScript (sem frameworks), consumindo a API de forma assíncrona.
* **Documentação Automática:** Swagger/OpenAPI integrado para testes e documentação dos endpoints.

## 🏗️ Arquitetura e Padrões
Este projeto foi estruturado simulando um ambiente corporativo robusto:
* **Camada de Apresentação (Views):** Responsável apenas por receber o tráfego HTTP, rotear e devolver respostas JSON.
* **Camada de Regras de Negócio (Services):** Onde a lógica real acontece, totalmente isolada do banco de dados e do framework web.
* **Camada de Acesso a Dados (Gateways/Repositories):** Única parte do sistema que interage com o ORM do banco de dados.
* **Frontend Modular:** Separação estrita entre Autenticação (`auth.js`), Interface/DOM (`ui.js`) e Domínio (`produtos.js`). CSS implementado com variáveis globais (Design System Básico).

## 🛠️ Tecnologias Utilizadas
* **Backend:** Python, Django, Django REST Framework
* **Frontend:** HTML5 Semântico, CSS3 Moderno, JavaScript (ES6+ com async/await e Fetch API)
* **Banco de Dados:** SQLite (Configurado para persistência)
* **Documentação:** drf-spectacular (Swagger UI)

## 🚀 Como executar o projeto localmente

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git](https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git)
   cd NOME_DA_PASTA
   ```
2. **Crie e ative o ambiente virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Linux/Mac
    venv\Scripts\activate     # No Windows
    ```
3. **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4. **Prepare o Banco de Dados:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
5. **Execute o servidor:**
    ```bash
    python manage.py runserver    
    ```

## 📚 Documentação da API

Com o servidor rodando, acesse a documentação interativa da API (Swagger) em:
http://localhost:8000/api/docs/

