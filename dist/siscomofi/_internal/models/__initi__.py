# Importa os componentes principais da base para que fiquem acessíveis
from .base import Session, engine, init_db

# Importa os modelos para que possamos usá-los em outras partes do app
from .cliente import Cliente
# from .lancamento import Lancamento # Descomente quando criar este arquivo

# Importa as funções CRUD para que as rotas possam chamá-las
from .cliente import (
    adicionar_cliente,
    atualizar_cliente,
    get_clientes_paginados,
    get_cliente_por_id,
    count_total_clientes,
    deletar_cliente,
)
# from .lancamento import add_lancamento, ... # Descomente quando criar
