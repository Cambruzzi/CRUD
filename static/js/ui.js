/**
 * Módulo de Interface de Usuário (ui.js)
 * Responsável exclusivamente por manipular o DOM (Document Object Model).
 * Este arquivo não possui regras de negócio, apenas funções de "desenhar na tela".
 */

// =====================================================================
// GERENCIAMENTO DE ESTADO DA INTERFACE (SPA ROUTER)
// =====================================================================

/**
 * Utilitário global: Oculta todas as seções (telas) da aplicação.
 * Padrão básico de roteamento em Single Page Applications sem frameworks.
 */
function esconderTudo() {
    document.getElementById('tela-login').classList.add('escondido');
    document.getElementById('tela-cadastro').classList.add('escondido');
    document.getElementById('tela-produto').classList.add('escondido'); // Formulário de Novo Produto
    document.getElementById('tela-lista').classList.add('escondido');   // Listagem dos Produtos
    document.getElementById('tela-editar').classList.add('escondido');  // Formulário de Edição
}

function mostrarTelaLogin() {
    esconderTudo();
    document.getElementById('tela-login').classList.remove('escondido');
    document.getElementById('msg-login').innerText = ""; // Limpa erros antigos
}

function mostrarTelaCadastro() {
    esconderTudo();
    document.getElementById('tela-cadastro').classList.remove('escondido');
    document.getElementById('msg-cadastro').innerText = "";
}

function mostrarTelaProdutos() {
    esconderTudo();
    document.getElementById('tela-produto').classList.remove('escondido');
}

function mostrarTelaLista() {
    esconderTudo();
    document.getElementById('tela-lista').classList.remove('escondido');
}

function mostrarTelaEditar() {
    esconderTudo();
    document.getElementById('tela-editar').classList.remove('escondido');
    document.getElementById('msg-editar').innerText = "";
}

// =====================================================================
// RENDERIZAÇÃO DINÂMICA
// =====================================================================

/**
 * Renderiza a lista de produtos no DOM.
 * @param {Array} produtos - Array de objetos representando os produtos vindos da API.
 */
function renderizarListaProdutos(produtos) {
    const conteiner = document.getElementById('conteiner-produtos');

    // Validação de estado vazio (Empty State)
    if (produtos.length === 0) {
        conteiner.innerHTML = "<p>Nenhum produto cadastrado ainda.</p>";
        return;
    }

    let htmlAcumulado = "";

    produtos.forEach(produto => {
        let imagemHTML = "";
        
        if (produto.imagem) {
            imagemHTML = `<img src="${produto.imagem}" alt="Foto de ${produto.nome}">`;
        }

        const valorFormatado = Number(produto.valor).toLocaleString('pt-BR', { 
            minimumFractionDigits: 2, 
            maximumFractionDigits: 2 
        });

        // Constrói o componente (Card do Produto)
        htmlAcumulado += `
            <div class="produto-item">
                ${imagemHTML}
                <div><strong>${produto.nome}</strong> (Cód: ${produto.codigo}) - R$ ${valorFormatado}</div>
                <div class="produto-item-btn">
                    <button class="btn btn-warning" onclick="abrirEdicao(${produto.id}, '${produto.nome}', '${produto.codigo}', ${produto.valor})">
                        Editar
                    </button>
                    <button class="btn btn-danger" onclick="deletarProduto(${produto.id})">
                        Excluir
                    </button>
                </div>
            </div>
        `;
    });

    // Injeção única no DOM
    conteiner.innerHTML = htmlAcumulado;
}

/**
 * Exibe uma mensagem de erro padronizada caso a API falhe ao listar.
 */
function mostrarErroCarregamento() {
    document.getElementById('conteiner-produtos').innerHTML = "<p class='texto-erro'>Erro ao carregar produtos.</p>";
}

// =====================================================================
// INICIALIZAÇÃO (ENTRY POINT)
// =====================================================================

/**
 * Ocorre assim que o navegador termina de baixar o HTML.
 * Funciona como o "Main" da nossa aplicação Frontend.
 */
window.onload = function() {
    // Se a função do módulo de Autenticação achar a pulseira no navegador, pula o login!
    if (obterToken()) {
        mostrarTelaProdutos();
    } else {
        mostrarTelaLogin();
    }
};