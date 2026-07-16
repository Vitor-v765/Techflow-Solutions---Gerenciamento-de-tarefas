import tkinter as tk
from tkinter import messagebox, ttk
from src.core import SistemaLogisticaCore

class InterfaceGraficaLogistica:
    def __init__(self, root):
        self.root = root
        self.root.title("TechFlow Solutions - Logística Ágil")
        self.root.geometry("1000x650")
        self.root.configure(bg="#f3f4f6")
        
        # Instancia a lógica de negócios
        self.core = SistemaLogisticaCore()
        
        self.container = tk.Frame(self.root, bg="#f3f4f6")
        self.container.pack(fill=tk.BOTH, expand=True)
        
        self.tela_login()

    def limpar_tela(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def tela_login(self):
        self.limpar_tela()
        
        card = tk.Frame(self.container, bg="white", padx=30, pady=30, highlightthickness=1, highlightbackground="#e5e7eb")
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        tk.Label(card, text="🚀 TechFlow Solutions", font=("Arial", 20, "bold"), bg="white", fg="#1e3d59").pack(pady=5)
        tk.Label(card, text="Mapeamento de Rotas Logísticas", font=("Arial", 10), bg="white", fg="#6b7280").pack(pady=5)
        
        tk.Label(card, text="E-mail:", font=("Arial", 9, "bold"), bg="white", fg="#374151").pack(anchor="w", pady=(10, 2))
        ent_email = tk.Entry(card, width=32, font=("Arial", 11), bd=1, relief="solid")
        ent_email.pack(ipady=4)
        
        tk.Label(card, text="Senha:", font=("Arial", 9, "bold"), bg="white", fg="#374151").pack(anchor="w", pady=(10, 2))
        ent_senha = tk.Entry(card, show="*", width=32, font=("Arial", 11), bd=1, relief="solid")
        ent_senha.pack(ipady=4)
        
        def entrar():
            sucesso, resposta = self.core.fazer_login(ent_email.get().strip(), ent_senha.get().strip())
            if sucesso:
                self.tela_kanban()
            else:
                messagebox.showerror("Acesso Negado", resposta)

        tk.Button(card, text="Fazer Login", bg="#1e3d59", fg="white", font=("Arial", 10, "bold"),
                  command=entrar, bd=0, cursor="hand2").pack(fill=tk.X, ipady=6, pady=(20, 5))
                  
        tk.Button(card, text="Criar Nova Conta", bg="white", fg="#10b981", font=("Arial", 9, "bold"),
                  command=self.tela_cadastro, bd=0, cursor="hand2").pack(fill=tk.X)

    def tela_cadastro(self):
        self.limpar_tela()
        
        card = tk.Frame(self.container, bg="white", padx=30, pady=30, highlightthickness=1, highlightbackground="#e5e7eb")
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        tk.Label(card, text="📝 Registro de Operador", font=("Arial", 16, "bold"), bg="white", fg="#1e3d59").pack(pady=10)
        
        tk.Label(card, text="Nome Completo:", font=("Arial", 9, "bold"), bg="white", fg="#374151").pack(anchor="w", pady=(5, 2))
        ent_nome = tk.Entry(card, width=32, font=("Arial", 11), bd=1, relief="solid")
        ent_nome.pack(ipady=4)

        tk.Label(card, text="E-mail Corporativo:", font=("Arial", 9, "bold"), bg="white", fg="#374151").pack(anchor="w", pady=(5, 2))
        ent_email = tk.Entry(card, width=32, font=("Arial", 11), bd=1, relief="solid")
        ent_email.pack(ipady=4)
        
        tk.Label(card, text="Senha de Acesso:", font=("Arial", 9, "bold"), bg="white", fg="#374151").pack(anchor="w", pady=(5, 2))
        ent_senha = tk.Entry(card, show="*", width=32, font=("Arial", 11), bd=1, relief="solid")
        ent_senha.pack(ipady=4)
        
        def registrar():
            sucesso, msg = self.core.cadastrar_usuario(ent_nome.get().strip(), ent_email.get().strip(), ent_senha.get().strip())
            if sucesso:
                messagebox.showinfo("Sucesso!", msg)
                self.tela_login()
            else:
                messagebox.showerror("Falha no Registro", msg)

        tk.Button(card, text="Cadastrar Operador", bg="#10b981", fg="white", font=("Arial", 10, "bold"),
                  command=registrar, bd=0, cursor="hand2").pack(fill=tk.X, ipady=6, pady=(20, 5))
                  
        tk.Button(card, text="Voltar ao Login", bg="white", fg="#4b5563", font=("Arial", 9),
                  command=self.tela_login, bd=0, cursor="hand2").pack(fill=tk.X)

    def tela_kanban(self):
        self.limpar_tela()
        
        # Cabeçalho Superior
        header = tk.Frame(self.container, bg="#1e3d59", pady=10)
        header.pack(fill=tk.X)
        
        info = f"👤 Operador: {self.core.dados['usuario_logado']['username']}"
        tk.Label(header, text="🚚 TECHFLOW - GESTÃO LOGÍSTICA", font=("Arial", 12, "bold"), bg="#1e3d59", fg="white").pack(side=tk.LEFT, padx=15)
        tk.Label(header, text=info, font=("Arial", 10, "bold"), bg="#1e3d59", fg="#10b981").pack(side=tk.LEFT, padx=20)
        
        def logout():
            self.core.deslogar()
            self.tela_login()
            
        tk.Button(header, text="Logoff", bg="#ef4444", fg="white", font=("Arial", 9, "bold"), command=logout, bd=0, cursor="hand2", padx=10, pady=3).pack(side=tk.RIGHT, padx=15)
        tk.Button(header, text="➕ Adicionar Rota", bg="#10b981", fg="white", font=("Arial", 9, "bold"), command=self.janela_nova_tarefa, bd=0, cursor="hand2", padx=10, pady=3).pack(side=tk.RIGHT, padx=5)

        # Quadro de Trabalho (Kanban)
        board = tk.Frame(self.container, bg="#f3f4f6")
        board.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        colunas = [
            ("todo", "📋 A FAZER (TO DO)", "#eff6ff", "#1e3a8a"),
            ("in_progress", "🔄 EM TRÂNSITO (IN PROGRESS)", "#fffbeb", "#78350f"),
            ("done", "✅ ENTREGUE (DONE)", "#ecfdf5", "#065f46")
        ]
        
        self.listboxes = {}
        tarefas = self.core.listar_tarefas_usuario()
        
        for status, txt, bg_col, fg_col in colunas:
            col_frame = tk.Frame(board, bg=bg_col, bd=1, relief="solid", highlightthickness=0)
            col_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
            
            tk.Label(col_frame, text=txt, font=("Arial", 10, "bold"), bg=bg_col, fg=fg_col, pady=8).pack(fill=tk.X)
            
            listbox = tk.Listbox(col_frame, font=("Arial", 10), bd=0, bg=bg_col, selectbackground=fg_col, selectforeground="white", highlightthickness=0)
            listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            self.listboxes[status] = listbox
            
            # Adiciona as tarefas correspondentes na coluna
            tarefas_status = [t for t in tarefas if t['status'] == status]
            for t in tarefas_status:
                icon_prio = {'alta': '🔴', 'media': '🟡', 'baixa': '🟢'}.get(t['prioridade'], '⚪')
                # Exibe ID, Prioridade, Título e Motorista (Mudança de escopo visível!)
                listbox.insert(tk.END, f"ID: {t['id']} | {icon_prio} {t['titulo']} ({t['motorista']})")

        # Painel de Controle Inferior
        controles = tk.Frame(self.container, bg="white", pady=12, highlightthickness=1, highlightbackground="#e5e7eb")
        controles.pack(fill=tk.X)
        
        tk.Label(controles, text="Ações de Rota:", font=("Arial", 9, "bold"), bg="white", fg="#4b5563").pack(pady=(0, 5))
        
        btn_frame = tk.Frame(controles, bg="white")
        btn_frame.pack()
        
        tk.Button(btn_frame, text="Mover Status", bg="#f59e0b", fg="white", font=("Arial", 9, "bold"), command=self.janela_mover_status, bd=0, cursor="hand2", padx=12, pady=5).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Editar Detalhes", bg="#3b82f6", fg="white", font=("Arial", 9, "bold"), command=self.janela_editar, bd=0, cursor="hand2", padx=12, pady=5).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Atribuir Motorista [MUDANÇA]", bg="#8b5cf6", fg="white", font=("Arial", 9, "bold"), command=self.janela_atribuir_motorista, bd=0, cursor="hand2", padx=12, pady=5).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Excluir Rota", bg="#ef4444", fg="white", font=("Arial", 9, "bold"), command=self.acao_excluir, bd=0, cursor="hand2", padx=12, pady=5).pack(side=tk.LEFT, padx=5)

    def obter_selecao(self):
        for status, lbox in self.listboxes.items():
            sel = lbox.curselection()
            if sel:
                txt = lbox.get(sel[0])
                id_t = int(txt.split(" | ")[0].replace("ID: ", ""))
                tarefas = self.core.listar_tarefas_usuario()
                return next((t for t in tarefas if t['id'] == id_t), None)
        return None

    def janela_nova_tarefa(self):
        top = tk.Toplevel(self.root)
        top.title("Registrar Rota")
        top.geometry("340x280")
        top.resizable(False, False)
        
        tk.Label(top, text="📍 Destino / Título:", font=("Arial", 9, "bold")).pack(anchor="w", padx=15, pady=(15, 2))
        ent_tit = tk.Entry(top, width=35, font=("Arial", 10))
        ent_tit.pack(padx=15)
        
        tk.Label(top, text="📝 Notas de Entrega (Desc):", font=("Arial", 9, "bold")).pack(anchor="w", padx=15, pady=(10, 2))
        ent_desc = tk.Entry(top, width=35, font=("Arial", 10))
        ent_desc.pack(padx=15)
        
        tk.Label(top, text="⚡ Criticidade / Prioridade:", font=("Arial", 9, "bold")).pack(anchor="w", padx=15, pady=(10, 2))
        combo_prio = ttk.Combobox(top, values=["Alta", "Média", "Baixa"], state="readonly", width=15)
        combo_prio.set("Média")
        combo_prio.pack(anchor="w", padx=15)
        
        def salvar():
            sucesso, msg = self.core.criar_tarefa(ent_tit.get().strip(), ent_desc.get().strip(), combo_prio.get())
            if sucesso:
                self.tela_kanban()
                top.destroy()
            else:
                messagebox.showwarning("Alerta", msg)
                
        tk.Button(top, text="Salvar Nova Rota", bg="#10b981", fg="white", font=("Arial", 10, "bold"), command=salvar, bd=0, cursor="hand2").pack(fill=tk.X, padx=15, ipady=5, pady=20)

    def janela_mover_status(self):
        tarefa = self.obter_selecao()
        if not tarefa:
            messagebox.showwarning("Aviso", "Selecione uma rota no Kanban primeiro.")
            return
            
        top = tk.Toplevel(self.root)
        top.title("Mover Status")
        top.geometry("260x160")
        
        tk.Label(top, text=f"Mover: {tarefa['titulo']}", font=("Arial", 9, "bold")).pack(pady=10)
        combo = ttk.Combobox(top, values=["A Fazer", "Em Progresso", "Concluído"], state="readonly")
        mapa_inverso = {'todo': 'A Fazer', 'in_progress': 'Em Progresso', 'done': 'Concluído'}
        combo.set(mapa_inverso[tarefa['status']])
        combo.pack(pady=5)
        
        def mover():
            mapa = {"A Fazer": "todo", "Em Progresso": "in_progress", "Concluído": "done"}
            self.core.atualizar_status_tarefa(tarefa['id'], mapa[combo.get()])
            self.tela_kanban()
            top.destroy()
            
        tk.Button(top, text="Confirmar Mudança", bg="#f59e0b", fg="white", font=("Arial", 9, "bold"), command=mover, bd=0, cursor="hand2").pack(fill=tk.X, padx=20, ipady=4, pady=15)

    def janela_editar(self):
        tarefa = self.obter_selecao()
        if not tarefa:
            messagebox.showwarning("Aviso", "Selecione uma rota para editar.")
            return
            
        top = tk.Toplevel(self.root)
        top.title("Editar Rota")
        top.geometry("340x220")
        
        tk.Label(top, text="Título:", font=("Arial", 9, "bold")).pack(anchor="w", padx=15, pady=(15, 2))
        ent_t = tk.Entry(top, width=35, font=("Arial", 10))
        ent_t.insert(0, tarefa['titulo'])
        ent_t.pack(padx=15)
        
        tk.Label(top, text="Descrição:", font=("Arial", 9, "bold")).pack(anchor="w", padx=15, pady=(10, 2))
        ent_d = tk.Entry(top, width=35, font=("Arial", 10))
        ent_d.insert(0, tarefa['descricao'])
        ent_d.pack(padx=15)
        
        def atualizar():
            self.core.editar_tarefa(tarefa['id'], ent_t.get().strip(), ent_d.get().strip())
            self.tela_kanban()
            top.destroy()
            
        tk.Button(top, text="Atualizar Dados", bg="#3b82f6", fg="white", font=("Arial", 9, "bold"), command=atualizar, bd=0, cursor="hand2").pack(fill=tk.X, padx=15, ipady=4, pady=15)

    def janela_atribuir_motorista(self):
        """[TELA DA MUDANÇA DE ESCOPO] Abre caixa para atribuir motoristas."""
        tarefa = self.obter_selecao()
        if not tarefa:
            messagebox.showwarning("Aviso", "Selecione a rota para vincular o motorista.")
            return
            
        top = tk.Toplevel(self.root)
        top.title("Alocar Motorista")
        top.geometry("300x180")
        
        tk.Label(top, text=f"Alocar motorista para:\n{tarefa['titulo']}", font=("Arial", 9, "bold"), justify=tk.CENTER).pack(pady=10)
        
        ent_moto = tk.Entry(top, width=28, font=("Arial", 10))
        ent_moto.insert(0, tarefa['motorista'] if tarefa['motorista'] != "Não atribuído" else "")
        ent_moto.pack(pady=5)
        
        def salvar():
            nome_moto = ent_moto.get().strip()
            self.core.atribuir_motorista_tarefa(tarefa['id'], nome_moto)
            self.tela_kanban()
            top.destroy()
            
        tk.Button(top, text="Alocar Colaborador", bg="#8b5cf6", fg="white", font=("Arial", 9, "bold"), command=salvar, bd=0, cursor="hand2").pack(fill=tk.X, padx=20, ipady=4, pady=10)

    def acao_excluir(self):
        tarefa = self.obter_selecao()
        if not tarefa:
            messagebox.showwarning("Aviso", "Selecione uma rota para excluir.")
            return
            
        confirma = messagebox.askyesno("Excluir Rota", f"Tem certeza que deseja apagar a rota para '{tarefa['titulo']}'?")
        if confirma:
            self.core.deletar_tarefa(tarefa['id'])
            self.tela_kanban()