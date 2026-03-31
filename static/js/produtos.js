/**
 * Módulo de Domínio de Produtos (produtos.js)
 * Responsável por todas as operações de CRUD conectadas à API do backend.
 */

/**
 * Busca a lista de produtos na API e delega a renderização para a UI.
 * Requer que o usuário esteja autenticado.
 */
async function carregarListaProdutos() {
    mostrarTelaLista();
    const conteiner = document.getElementById('conteiner-produtos');
    conteiner.innerHTML = "Carregando...";

    try {
        const resposta = await fetch('/api/v1/produtos/', {
            method: 'GET',
            headers: { 
                'Authorization': 'Token ' + obterToken() 
            }
        });

        if (resposta.ok) {
            const produtos_do_banco = await resposta.json();
            renderizarListaProdutos(produtos_do_banco);
        } else {
            mostrarErroCarregamento(); // 
        }
    } catch (erro) {
        console.error("Erro de rede ao carregar produtos:", erro);
        conteiner.innerHTML = "<p class='texto-erro'>Erro de conexão com o servidor.</p>";
    }
}

/**
 * Coleta os dados do formulário de criação e envia para a API.
 * Suporta envio de arquivos físicos (imagens) usando o padrão FormData (Multipart).
 */
async function cadastrarProduto() {
    const msgElement = document.getElementById('msg-produto');
    const formData = new FormData();
    
    formData.append('nome', document.getElementById('nome-produto').value);
    formData.append('codigo', document.getElementById('codigo-produto').value);
    formData.append('valor', document.getElementById('valor-produto').value);
    
    const arquivoFoto = document.getElementById('imagem-produto').files[0];
    if (arquivoFoto) {
        formData.append('imagem', arquivoFoto);
    }

    try {
        const resposta = await fetch('/api/v1/produtos/', {
            method: 'POST',
            headers: { 
                'Authorization': 'Token ' + obterToken()
            },
            body: formData
        });

        if (resposta.ok) {
            // Usa as classes do nosso Design System ao invés de CSS inline
            msgElement.className = "texto-sucesso";
            msgElement.innerText = "Produto salvo com sucesso no banco!";
            
            // UX: Limpa os campos após o sucesso para facilitar um novo cadastro
            document.getElementById('nome-produto').value = "";
            document.getElementById('codigo-produto').value = "";
            document.getElementById('valor-produto').value = "";
            document.getElementById('imagem-produto').value = "";
        } else {
            msgElement.className = "texto-erro";
            msgElement.innerText = "Erro ao salvar os dados. Verifique os campos.";
        }
    } catch (erro) {
        console.error("Erro de rede ao cadastrar produto:", erro);
        msgElement.className = "texto-erro";
        msgElement.innerText = "Falha de comunicação com o servidor.";
    }
}

/**
 * Envia as atualizações parciais de um produto existente para a API.
 */
async function salvarAlteracao() {
    const msgElement = document.getElementById('msg-editar');
    const id = document.getElementById('edit-id').value;
    const formData = new FormData();
    
    formData.append('nome', document.getElementById('edit-nome').value);
    formData.append('codigo', document.getElementById('edit-codigo').value);
    formData.append('valor', document.getElementById('edit-valor').value);
    
    const arquivoFoto = document.getElementById('edit-imagem').files[0];
    if (arquivoFoto) {
        formData.append('imagem', arquivoFoto);
    }
    
    try {
        const resposta = await fetch(`/api/v1/produtos/${id}/`, {
            method: 'PUT',
            headers: { 
                'Authorization': 'Token ' + obterToken()
            },
            body: formData
        });

        if (resposta.ok) {
            document.getElementById('edit-imagem').value = "";
            carregarListaProdutos(); 
        } else {
            msgElement.className = "texto-erro";
            msgElement.innerText = "Erro ao atualizar o produto.";
        }
    } catch (erro) {
        console.error("Erro de rede ao atualizar produto:", erro);
        msgElement.className = "texto-erro";
        msgElement.innerText = "Falha de comunicação com o servidor.";
    }
}

/**
 * Solicita a exclusão lógica (Soft Delete) de um produto na API.
 * @param {number} id - O identificador único do produto.
 */
async function deletarProduto(id) {
    const confirmacao = confirm("Tem certeza que deseja excluir este produto?");
    
    if (!confirmacao) return;

    try {
        const resposta = await fetch(`/api/v1/produtos/${id}/`, {
            method: 'DELETE',
            headers: { 
                'Authorization': 'Token ' + obterToken()
            }
        });

        if (resposta.ok) {
            carregarListaProdutos(); 
        } else {
            alert("Erro ao tentar excluir o produto. Permissão negada ou erro interno.");
        }
    } catch (erro) {
        console.error("Erro de rede ao deletar produto:", erro);
        alert("Falha de conexão. Verifique sua internet.");
    }
}

/**
 * Prepara o formulário de edição com os dados atuais do produto.
 * * @param {number} id - ID do produto.
 * @param {string} nome - Nome do produto.
 * @param {string} codigo - Código (SKU) do produto.
 * @param {number} valor - Preço do produto.
 */
function abrirEdicao(id, nome, codigo, valor) {
    mostrarTelaEditar();

    // 2. Popula os inputs (DOM) com os dados em memória para o usuário alterar
    document.getElementById('edit-id').value = id;
    document.getElementById('edit-nome').value = nome;
    document.getElementById('edit-codigo').value = codigo;
    document.getElementById('edit-valor').value = valor;
}