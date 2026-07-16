import os
import json
from datetime import datetime

ARQUIVO_DADOS = 'tasks.json'

class GerenciadorDados:
    """Classe responsável pelo salvamento e leitura dos dados em arquivo JSON."""
    @staticmethod
    def carregar_dados():
        if os.path.exists(ARQUIVO_DADOS):
            try:
                with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        return {'usuarios': [], 'tarefas': [], 'usuario_logado': None}

    @staticmethod
    def salvar_dados(dados):
        with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)


class SistemaLogisticaCore:
    """Classe contendo a lógica de negócios (Login, Cadastro, CRUD e Mudança de Escopo)."""
    def __init__(self):
        self.dados = GerenciadorDados.carregar_dados()
        # Garante reinicialização limpa de sessão ao abrir o sistema
        self.dados['usuario_logado'] = None
        GerenciadorDados.salvar_dados(self.dados)

    def cadastrar_usuario(self, username, email, senha):
        if not username or not email or not senha:
            return False, "Preencha todos os campos."
        
        # Validação de e-mail duplicado
        for u in self.dados['usuarios']:
            if u['email'] == email:
                return False, "E-mail já cadastrado."
        
        novo_id = len(self.dados['usuarios']) + 1
        self.dados['usuarios'].append({
            'id': novo_id,
            'username': username,
            'email': email,
            'senha': senha
        })
        GerenciadorDados.salvar_dados(self.dados)
        return True, "Usuário cadastrado com sucesso!"

    def fazer_login(self, email, senha):
        for user in self.dados['usuarios']:
            if user['email'] == email and user['senha'] == senha:
                self.dados['usuario_logado'] = user
                GerenciadorDados.salvar_dados(self.dados)
                return True, user
        return False, "E-mail ou senha inválidos."

    def deslogar(self):
        self.dados['usuario_logado'] = None
        GerenciadorDados.salvar_dados(self.dados)

    def criar_tarefa(self, titulo, descricao, prioridade):
        """CRUD: Create"""
        if not titulo:
            return False, "O título da tarefa é obrigatório."
        
        if not self.dados['usuario_logado']:
            return False, "Usuário precisa estar logado."

        novo_id = len(self.dados['tarefas']) + 1
        nova_t = {
            'id': novo_id,
            'titulo': titulo,
            'descricao': descricao,
            'status': 'todo', # todo, in_progress, done
            'prioridade': prioridade.lower(), # alta, media, baixa
            'motorista': "Não atribuído", # [MUDANÇA DE ESCOPO ADICIONADA]
            'usuario_id': self.dados['usuario_logado']['id'],
            'criada_em': datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        self.dados['tarefas'].append(nova_t)
        GerenciadorDados.salvar_dados(self.dados)
        return True, "Tarefa registrada com sucesso."

    def listar_tarefas_usuario(self):
        """CRUD: Read"""
        if not self.dados['usuario_logado']:
            return []
        user_id = self.dados['usuario_logado']['id']
        return [t for t in self.dados['tarefas'] if t['usuario_id'] == user_id]

    def atualizar_status_tarefa(self, tarefa_id, novo_status):
        """CRUD: Update (Mover de coluna no Kanban)"""
        for t in self.dados['tarefas']:
            if t['id'] == tarefa_id:
                t['status'] = novo_status
                GerenciadorDados.salvar_dados(self.dados)
                return True
        return False

    def editar_tarefa(self, tarefa_id, novo_titulo, nova_desc):
        """CRUD: Update (Editar texto da tarefa)"""
        if not novo_titulo:
            return False, "O título não pode ser vazio."
        for t in self.dados['tarefas']:
            if t['id'] == tarefa_id:
                t['titulo'] = novo_titulo
                t['descricao'] = nova_desc
                GerenciadorDados.salvar_dados(self.dados)
                return True
        return False

    def deletar_tarefa(self, tarefa_id):
        """CRUD: Delete"""
        for t in self.dados['tarefas']:
            if t['id'] == tarefa_id:
                self.dados['tarefas'].remove(t)
                GerenciadorDados.salvar_dados(self.dados)
                return True
        return False

    def atribuir_motorista_tarefa(self, tarefa_id, nome_motorista):
        """[MUDANÇA DE ESCOPO] Permite vincular um motorista à entrega logística."""
        if not nome_motorista:
            nome_motorista = "Não atribuído"
        for t in self.dados['tarefas']:
            if t['id'] == tarefa_id:
                t['motorista'] = nome_motorista
                GerenciadorDados.salvar_dados(self.dados)
                return True
        return False