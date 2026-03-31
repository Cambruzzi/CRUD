/**
 * Define o token no navegador para manter a sessão do usuário.
 * @param {*} token hash de autenticação recebido do backend após login ou registro.
 */
function salvarSessao(token) {
    localStorage.setItem('meuToken', token);
    mostrarTelaProdutos();
}
/**
 * função para obter o token do navegador, usado para autenticação nas requisições.
 * @returns {*}token salvo no navegador ou null se não existir.
 */
function obterToken() {
    return localStorage.getItem('meuToken');
}
/**
 * Função para realizar o login do usuário. Envia as credenciais para o backend e, se forem válidas, salva o token recebido.
 */
async function fazerLogin() {
    const user = document.getElementById('username').value;
    const pass = document.getElementById('password').value;
    const resposta = await fetch('/api/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: user, password: pass })
    });
    const dados = await resposta.json();
    if (resposta.ok) {
        salvarSessao(dados.token); 
    } else {
        document.getElementById('msg-login').innerText = "Usuário ou senha incorretos!";
    }
}
/**
 * Função para registrar um novo usuário. Envia as credenciais para o backend e, se a criação for bem-sucedida, salva o token recebido.
 */
async function registrarUsuario() {
    const user = document.getElementById('novo-username').value;
    const pass = document.getElementById('novo-password').value;
    const resposta = await fetch('/api/v1/registrar/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: user, password: pass })
    });
    const dados = await resposta.json();
    if (resposta.ok) {
        salvarSessao(dados.token);
    } else {
        document.getElementById('msg-cadastro').innerText = dados.erro || "Erro ao criar conta.";
    }
}
/**
 * Função para realizar o logout do usuário. Remove o token do navegador e redireciona para a tela de login.
 */
function sair() {
    localStorage.removeItem('meuToken');
    mostrarTelaLogin();
}