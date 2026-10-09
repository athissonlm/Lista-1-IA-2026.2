class Regra:
    def __init__(self, id_regra, se_condicoes, entao_conclusao):
        self.id = id_regra
        self.se = se_condicoes  # Lista de fatos requeridos (condições)
        self.entao = entao_conclusao  # Fato deduzido (conclusão)

    def __str__(self):
        return f"Regra {self.id}: SE {' E '.join(self.se)} ENTÃO {self.entao}"


class BaseConhecimento:
    """ Editor e Armazenamento da Base de Conhecimento """
    def __init__(self):
        self.regras = []
        self.fatos = set()

    def adicionar_regra(self, id_regra, se_condicoes, entao_conclusao):
        self.regras.append(Regra(id_regra, se_condicoes, entao_conclusao))

    def excluir_regra(self, id_regra):
        # Armazena o tamanho antes de tentar excluir para verificar se a regra existia
        tamanho_anterior = len(self.regras)
        self.regras = [r for r in self.regras if r.id != id_regra]
        # Retorna True se o tamanho diminuiu (ou seja, a regra foi removida)
        return len(self.regras) < tamanho_anterior

    def adicionar_fato(self, fato):
        self.fatos.add(fato)

    def limpar_fatos(self):
        self.fatos.clear()

    def exibir(self):
        print("\n--- STATUS DA BASE DE CONHECIMENTO ---")
        print("Fatos Atuais:", list(self.fatos) if self.fatos else "Nenhum fato conhecido.")
        print("Regras Registradas:")
        for r in self.regras:
            print(f"  {r}")
        print("--------------------------------------")


class Explicacao:
    """ Módulo de Explicação (Por quê? / Como?) """
    def __init__(self):
        self.trilha_como = {}  # Mapeia: fato -> Regra que o deduziu
        self.pilha_porque = [] # Pilha de objetivos para responder "Por quê"

    def registrar_como(self, fato, regra):
        self.trilha_como[fato] = regra

    def explicar_como(self, fato):
        print("\n[EXPLICAÇÃO] O sistema analisa a trilha de inferência...")
        if fato in self.trilha_como:
            regra = self.trilha_como[fato]
            print(f"COMO conclui '{fato}'?\n=> Fato deduzido utilizando a {regra}")
        else:
            print(f"COMO conclui '{fato}'?\n=> Este fato foi informado diretamente como uma premissa inicial ou entrada do usuário.")

    def explicar_porque(self):
        print("\n[EXPLICAÇÃO] O sistema analisa o encadeamento atual...")
        if self.pilha_porque:
            objetivo_atual = self.pilha_porque[-1]
            print(f"POR QUÊ estou perguntando isso?\n=> Porque preciso dessa informação para tentar provar o objetivo principal: '{objetivo_atual}'")
        else:
            print("=> Estou apenas coletando premissas ativas.")


class EngenhoInferencia:
    """ Motor Lógico (Encadeamento para Frente, Trás e Misto) """
    def __init__(self, bc, explicacao):
        self.bc = bc
        self.explicacao = explicacao

    def encadeamento_para_frente(self):
        """ Data-driven: Deduz tudo o que for possível a partir dos fatos iniciais. """
        novos_fatos = True
        print("\n[INFERÊNCIA] Iniciando Encadeamento para Frente...")
        while novos_fatos:
            novos_fatos = False
            for regra in self.bc.regras:
                if regra.entao not in self.bc.fatos:
                    # Verifica se todas as premissas da regra constam na base de fatos
                    if all(cond in self.bc.fatos for cond in regra.se):
                        self.bc.adicionar_fato(regra.entao)
                        self.explicacao.registrar_como(regra.entao, regra)
                        print(f"  => Fato novo deduzido: '{regra.entao}' (Aplicando Regra {regra.id})")
                        novos_fatos = True

    def encadeamento_para_tras(self, objetivo, interface):
        """ Goal-driven: Tenta provar um objetivo de trás para frente. """
        # Caso base: O objetivo já foi provado?
        if objetivo in self.bc.fatos:
            return True

        self.explicacao.pilha_porque.append(objetivo)
        regras_aplicaveis = [r for r in self.bc.regras if r.entao == objetivo]

        # Se não há regras para deduzir, o sistema precisa perguntar ao usuário
        if not regras_aplicaveis:
            resposta = interface.perguntar(objetivo, self.explicacao)
            self.explicacao.pilha_porque.pop()
            if resposta:
                self.bc.adicionar_fato(objetivo)
                return True
            return False

        # Tenta aplicar as regras disponíveis
        for regra in regras_aplicaveis:
            todas_condicoes_satisfeitas = True
            for cond in regra.se:
                # Recursão
                if not self.encadeamento_para_tras(cond, interface):
                    todas_condicoes_satisfeitas = False
                    break
            
            # Se conseguiu provar todas as condições desta regra
            if todas_condicoes_satisfeitas:
                self.bc.adicionar_fato(objetivo)
                self.explicacao.registrar_como(objetivo, regra)
                self.explicacao.pilha_porque.pop()
                return True

        self.explicacao.pilha_porque.pop()
        return False

    def encadeamento_misto(self, objetivo, interface):
        """ Roda pra frente para aproveitar dados já conhecidos, depois roda pra trás no alvo. """
        print("\n[INFERÊNCIA] Executando Fase 1: Encadeamento para Frente...")
        self.encadeamento_para_frente()
        if objetivo not in self.bc.fatos:
            print("\n[INFERÊNCIA] Executando Fase 2: Encadeamento para Trás...")
            return self.encadeamento_para_tras(objetivo, interface)
        return True


class Interface:
    """ Módulo de Interface em Linguagem Natural """
    def __init__(self):
        self.bc = BaseConhecimento()
        self.explicacao = Explicacao()
        self.engenho = EngenhoInferencia(self.bc, self.explicacao)

    def perguntar(self, fato, explicacao):
        while True:
            resp = input(f"\n[SISTEMA PERGUNTA] É verdade que '{fato}'? (sim/nao/porque): ").strip().lower()
            if resp in ['s', 'sim', 'y', 'yes']:
                return True
            elif resp in ['n', 'nao', 'não', 'no']:
                return False
            elif resp in ['porque', 'por que', 'pq', 'why']:
                explicacao.explicar_porque()
            else:
                print("Resposta não compreendida. Digite 'sim', 'nao' ou 'porque'.")

    def executar(self):
        """ Loop do Menu Principal do Shell """
        while True:
            print("\n=============================================")
            print(" SHELL DO SISTEMA BASEADO EM CONHECIMENTO ")
            print("=============================================")
            print("1. Adicionar Fato (Editor)")
            print("2. Adicionar Regra (Editor)")
            print("3. Exibir Base de Conhecimento")
            print("4. Rodar Encadeamento Misto (Testar Hipótese)")
            print("5. Explicar como um Fato foi deduzido (Como?)")
            print("6. Limpar Fatos")
            print("7. Excluir Regra (Editor)")
            print("0. Sair")
            opcao = input("\nEscolha uma opção: ").strip()

            if opcao == '1':
                fato = input("Digite o fato (ex: tem_pelos): ").strip()
                self.bc.adicionar_fato(fato)
                print(f"Fato '{fato}' adicionado à base.")
            
            elif opcao == '2':
                id_regra = input("ID da Regra (ex: R1): ").strip()
                condicoes = input("Condições SE (separadas por vírgula): ").split(',')
                condicoes = [c.strip() for c in condicoes]
                conclusao = input("Conclusão ENTÃO: ").strip()
                self.bc.adicionar_regra(id_regra, condicoes, conclusao)
                print("Regra salva com sucesso.")
            
            elif opcao == '3':
                self.bc.exibir()
            
            elif opcao == '4':
                if not self.bc.regras:
                    print("A Base de Conhecimento está vazia! Crie regras primeiro.")
                    continue
                hipotese = input("\nQual hipótese você quer testar/deduzir?: ").strip()
                sucesso = self.engenho.encadeamento_misto(hipotese, self)
                if sucesso:
                    print(f"\n>>> CONCLUSÃO: A hipótese '{hipotese}' é VERDADEIRA! <<<")
                else:
                    print(f"\n>>> CONCLUSÃO: A hipótese '{hipotese}' NÃO PÔDE SER PROVADA. <<<")
            
            elif opcao == '5':
                fato = input("Qual fato você quer investigar?: ").strip()
                self.explicacao.explicar_como(fato)
            
            elif opcao == '6':
                self.bc.limpar_fatos()
                self.explicacao.trilha_como.clear()
                print("Memória de trabalho (fatos) reiniciada.")
                
            elif opcao == '7':
                id_regra = input("Digite o ID da Regra a ser excluída (ex: R1): ").strip()
                removida = self.bc.excluir_regra(id_regra)
                if removida:
                    print(f"Regra '{id_regra}' excluída com sucesso da Base de Conhecimento.")
                else:
                    print(f"Erro: Regra '{id_regra}' não encontrada.")
            
            elif opcao == '0':
                print("Encerrando a ferramenta. Até logo!")
                break
            else:
                print("Opção inválida.")

# Inicializa o Shell
if __name__ == "__main__":
    shell = Interface()
    
    # Exemplo: Carregando uma base genérica de exemplo de Animais direto no código para poupar digitação
    # O Shell independe disso, mas facilita a demonstração.
    shell.bc.adicionar_regra("R1", ["tem_pelos"], "e_mamifero")
    shell.bc.adicionar_regra("R2", ["da_leite"], "e_mamifero")
    shell.bc.adicionar_regra("R3", ["e_mamifero", "come_carne"], "e_carnivoro")
    shell.bc.adicionar_regra("R4", ["e_carnivoro", "tem_cor_fulva", "tem_manchas_escuras"], "e_leopardo")
    shell.bc.adicionar_regra("R5", ["e_carnivoro", "tem_cor_fulva", "tem_listras_pretas"], "e_tigre")
    
    shell.executar()