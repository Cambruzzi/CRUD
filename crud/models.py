"""
Módulo de Modelos (Domínio/Entidades) da aplicação.
Define a estrutura das tabelas no banco de dados utilizando o ORM do Django.
"""

from django.db import models

class Produto(models.Model):
    """
    Entidade principal que representa um Produto comercializável no sistema.
    Aplica conceitos corporativos como:
    - Soft Delete (Exclusão Lógica) para manter histórico financeiro.
    - Timestamping automático para auditoria de alterações.
    """
    
    # Identificação básica do produto
    nome = models.CharField(
        max_length=100, 
        verbose_name="Nome do Produto",
        help_text="Nome comercial que será exibido aos clientes."
    )
    codigo = models.CharField(
        max_length=50,
        verbose_name="Código (SKU)",
        help_text="Identificador único interno ou código de barras."
    )

    valor = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Valor Unitário",
        help_text="Preço de venda atual do produto."
    )
    
    # Auditoria e Controle de Estado (Soft Delete)
    # Protege a integridade referencial do banco escondendo o registro ao invés de apagá-lo.
    excluido = models.BooleanField(
        default=False,
        verbose_name="Produto Excluído"
    )
    
    # Auditoria Temporal
    # auto_now=True avisa o Django para atualizar essa data sozinho em todo .save()
    data_alteracao = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Atualização"
    )
    
    imagem = models.ImageField(
        upload_to='produtos/', 
        null=True, 
        blank=True,
        verbose_name="Foto do Produto"
    )

    class Meta:
        """
        Metadados da entidade. 
        """
        db_table = "tb_produtos" # (Opcional) Força um nome mais limpo no banco de dados
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['nome'] # Sempre que fizer um GET sem filtro, retorna em ordem alfabética

    def __str__(self):
            
        # Em vez de retornar "1", retorna "[PRD-01] Teclado Mecânico - R$ 250.00"
        return f"[{self.codigo}] {self.nome} - R$ {self.valor}"