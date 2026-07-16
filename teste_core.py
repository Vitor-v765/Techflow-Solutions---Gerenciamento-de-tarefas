import pytest
import os
import json
from src.core import SistemaLogisticaCore, ARQUIVO_DADOS

@pytest.fixture(autouse=True)
def setup_e_teardown():
    """Garante que cada teste rode com um banco de dados temporário limpo."""
    if os.path.exists(ARQUIVO_DADOS):
        os.remove(ARQUIVO_DADOS)
    yield
    if os.path.exists(ARQUIVO_DADOS):
        os.remove(ARQUIVO_DADOS)

def test_fluxo_cadastro_e_login():
    core = SistemaLogisticaCore()
    
    # Testa Cadastro
    sucesso, msg = core.cadastrar_usuario("Lucas Operador", "lucas@techflow.com", "12345")
    assert sucesso is True
    assert len(core.dados['usuarios']) == 1
    
    # Testa Login Válido
    login_ok, user = core.fazer_login("lucas@techflow.com", "12345")
    assert login_ok is True
    assert user['username'] == "Lucas Operador"
    
    # Testa Login Inválido
    login_errado, msg_err = core.fazer_login("lucas@techflow.com", "senha_errada")
    assert login_errado is False

def test_crud_tarefas_com_mudanca_de_escopo():
    core = SistemaLogisticaCore()
    core.cadastrar_usuario("Lucas Operador", "lucas@techflow.com", "12345")
    core.fazer_login("lucas@techflow.com", "12345")
    
    # Teste: Create (Criar Rota)
    sucesso, msg = core.criar_tarefa("Rota de Entrega - Zona Sul", "Levar container 4", "Alta")
    assert sucesso is True
    
    tarefas = core.listar_tarefas_usuario()
    assert len(tarefas) == 1
    tarefa = tarefas[0]
    assert tarefa['titulo'] == "Rota de Entrega - Zona Sul"
    assert tarefa['motorista'] == "Não atribuído" # Valor padrão da mudança de escopo
    
    # Teste: Update Status
    core.atualizar_status_tarefa(tarefa['id'], "in_progress")
    assert core.listar_tarefas_usuario()[0]['status'] == "in_progress"
    
    # Teste: Mudança de Escopo (Atribuir Motorista)
    core.atribuir_motorista_tarefa(tarefa['id'], "Carlos Silva")
    assert core.listar_tarefas_usuario()[0]['motorista'] == "Carlos Silva"
    
    # Teste: Delete (Remover Rota)
    core.deletar_tarefa(tarefa['id'])
    assert len(core.listar_tarefas_usuario()) == 0