import random

def verificar_resposta(valor):
  param = ["y", "s", "ye", "yes", "sim", "sin", "si"]
  resul = True if valor in param else False
  return resul

# entrada válida
def entrada_valida(mensagem):
    while True:
        dado = input(mensagem).strip()
        if dado:
            return dado
        print("Preencha o campo vazio.")

# verifica se usuário já existe
def verificar_existencia(usuario, cpf):
    try:
        with open("usuarios.txt", "r") as arquivo:
            for linha in arquivo:
                dados = linha.strip().split(",")
                if len(dados) == 4:
                    nome_salvo, cpf_salvo, _, _ = dados
                    if usuario == nome_salvo:
                        print("\n⚠️ Nome de usuário já existe. Escolha outro.")
                        return True
                    if cpf == cpf_salvo:
                        print("\n⚠️ CPF já cadastrado.")
                        return True
    except FileNotFoundError:
        pass
    return False

# usuário com saldo inicial
def registrar(influencer = 0):
    usuario = entrada_valida("Digite seu nome de usuário:")
    while True:
        cpf = input("Informe seu CPF:")
        verfificar_cpf = len(cpf) == 11 and cpf.isdigit()
        if verfificar_cpf:
            break
        else:
            print("CPF inválido. Informe apenas números com 11 dígitos.")

    senha = entrada_valida("Digite sua senha:")
    if verificar_existencia(usuario, cpf):
        print("\n⚠️ Cadastro não permitido. Tente novamente.\n")
        return None, None, None

    SALDO_INICIAL = 10
    if influencer != 0 and influencer != 1:
      influencer = 0

    with open("usuarios.txt", "a") as arquivo:
        arquivo.write(f"{usuario},{cpf},{senha},{SALDO_INICIAL},{influencer}\n")
    print("\n✅ Cadastro realizado com sucesso!")
    return usuario, senha, SALDO_INICIAL, influencer

# login e recuperação do saldo
def login():
    while True:
        login_usuario = entrada_valida("Digite seu nome de usuário: ")
        login_senha = entrada_valida("Digite sua senha: ")
        with open("usuarios.txt", "r") as arquivo:
            usuarios_cadastrados = arquivo.readlines()
        for linha in usuarios_cadastrados:
            dados = linha.strip().split(",")
            if len(dados) == 5:
                nome_salvo, _, senha_salva, saldo, status = dados
                if login_usuario == nome_salvo and login_senha == senha_salva:
                    print("\n✅ Login realizado com sucesso! Bem-vindo de volta!")
                    return login_usuario, float(saldo), status
        print("⚠️ Usuário ou senha incorretos. Tente novamente.")

# atualiza saldo do usuário no arquivo
def atualizar_saldo(usuario, novo_saldo):
    linhas = []
    with open("usuarios.txt", "r") as arquivo:
        for linha in arquivo:
            dados = linha.strip().split(",")
            if len(dados) == 5 and dados[0] == usuario:
                dados[3] = str(novo_saldo)
            linhas.append(",".join(dados))
    with open("usuarios.txt", "w") as arquivo:
        arquivo.write("\n".join(linhas) + "\n")

# adicionar saldo
def adicionar_saldo(saldo):
    print("\n💰 Opções para adicionar saldo: 5, 10, 20, 50 reais")
    while True:
        try:
            valor = int(input("Quanto deseja adicionar? "))
            if valor in [5, 10, 20, 50]:
                return saldo + valor
            else:
                print("Opção inválida. Escolha entre 5, 10, 20 ou 50 reais.")
        except ValueError:
            print("Digite um número válido.")

def criar_banco():
  with open("banco.txt", "a") as arquivo:
      saldo_inicial = 50000
      historico = str(saldo_inicial)
      arquivo.write(f"{saldo_inicial} - {historico}\n")

def config_banco(valor):
    resul = False
    # Lê o saldo atual e o histórico do arquivo
    with open("banco.txt", "r") as arquivo:
      linhas = arquivo.readlines()
      if linhas:
        saldo_atual, historico = linhas[0].strip().split(" - ")
        saldo_atual = float(saldo_atual)
      else:
        saldo_atual = 50000
        historico = ""

      # Atualiza o saldo e o histórico
      saldo_atual += valor
      historico += f", {valor}" if historico else str(valor)

      # Escreve o novo saldo e histórico no arquivo
      with open("banco.txt", "w") as arquivo:
        arquivo.write(f"{saldo_atual} - {historico}\n")
      resul = True
    return resul

def banco_atual():
  with open("banco.txt", "r") as arquivo:
    linhas = arquivo.readlines()
    if linhas:
      saldo_atual, _ = linhas[0].strip().split(" - ")
      saldo_atual = float(saldo_atual)
    return saldo_atual
  
def gerar_matriz(status):
  simbolos = ["💸", "🐅", "🐯"]
  matriz = [[random.choice(simbolos) for _ in range(3)] for _ in range(3)]

  sorte = random.randint(1, 10)
  influencer = int(status) == 1
  saldoAtual_bando = banco_atual()

  K = 4 if influencer else 7
  if saldoAtual_bando <= 40000:
    K += 3 if influencer else 2

  if sorte > K:
    modo_ganho = random.choice(["diagonal1", "diagonal2", "meio"])
    item = random.choice(["💸", "🐅", "🐯"])
    if modo_ganho == "meio":
      matriz[1][0], matriz[1][1], matriz[1][2] = item, item, item
    elif modo_ganho == "diagonal1":
      matriz[0][0], matriz[1][1], matriz[2][2] = item, item, item
    else:
      matriz[2][0], matriz[1][1], matriz[0][2] = item, item, item

  print("-" * 20)
  for i, linha in enumerate(matriz):
    format = "  " if i != 1 else "->"
    print(format, " | ".join(linha).strip())
  print("-" * 20)

  return matriz


def verificar_vitoria_spin(matriz):
  resul, quant = None, 0
  # diagonal
  ###diagonal = [matriz[row_i][col_i] for row_i, row in enumerate(matriz) for col_i, _ in enumerate(row) if col_i == row_i]
  diagonal = matriz[0][0] == matriz[1][1] == matriz[2][2]
  diagonal2 = matriz[2][0] == matriz[1][1] == matriz[0][2]

  # meio
  meio = matriz[1][0] == matriz[1][1] == matriz[1][2]

  vetor = [diagonal, diagonal2, meio]
  for valor in vetor:
    if valor == True:
      resul = True
      quant += 1
  return (resul, quant)

# jogo
def jogar(nome, saldo, status, param = "-s"):
    def calc_valor():
      numeros = [10, 20, 30, 50, 100]
      quebrados = random.randint(1, 101)
      pesos = [20, 8, 3, 2, 1]
      pesos_normalizados = [p / sum(pesos) for p in pesos]

      numero_aleatorio = random.choices(numeros, weights=pesos_normalizados, k=1)[0]
      numero = 1 + (numero_aleatorio + quebrados) / 100
      format = f"{numero:.2f}"
      return float(format)

    if param == "-s":
      while True:
          print(f"\n💵 Saldo atual: R${saldo}")
          opcao = input("Deseja adicionar saldo? (s/n): ").strip().lower()
          if opcao == "s":
              saldo = adicionar_saldo(saldo)
              atualizar_saldo(nome, saldo)
              continue
          elif opcao == "n":
              break
          else:
            print("Digite 's' para sim ou 'n' para não.")

    print("\nVamos comecar a jogar!\n")

    rodada, win_count = 0, 0
    saldo_aposta = float(input("Digite quanto vai querer apostar: "))
    while saldo_aposta > saldo:
      saldo_aposta = float(input("Saldo insuficiente. Por favor, insira um valor coerente: "))
    while True:
        rodada += 1
        print(f"\n=== Giro {rodada} ===")

        matriz = gerar_matriz(status)
        resultado, peso = verificar_vitoria_spin(matriz)

        if resultado:
          valor_sorteado = calc_valor()
          format_valor = float(f"{valor_sorteado:.2f}")

          print(" WIIN!!")
          if peso > 1:
            print(f"Parabéns!!! Você ganhou de {peso} formas diferentes. Ganhará uma bonificação encima do valor sorteado - {format_valor}")
          valor_peso = float(format_valor * (1 + peso / 10))
          valor_ganho = saldo_aposta * valor_peso
          config_banco(-valor_ganho)
          print(f"Valor Ganho {valor_ganho:.2f}")
          saldo += valor_ganho - saldo_aposta
          saldo_aposta = valor_ganho
          win_count += 1
        else:
          config_banco(saldo_aposta)
          saldo -= saldo_aposta
          print(f"Você perdeu. Saldo restante: {saldo}")
          print("Não foi dessa vez. Tente mais uma!")

        resposta = input("\nDeseja continuar? ").lower()
        if not verificar_resposta(resposta):
          break
        elif saldo == 0:
          print("Sem saldo! Recarrege para continuar.")
          break
        elif resposta and saldo < saldo_aposta:
          print("Saldo insuficiente. Regarregue para continuar!")
          resp = input(f"Deseja apostar os seus {saldo} reais? ")
          if verificar_resposta(resp):
            saldo_aposta = saldo
          else:
            break

    atualizar_saldo(nome, saldo)
    print("\n=== Fim dos Giros ===")
    print(f"Você obteve {win_count} giro(s) vencedor(es).")
    print(f"Seu saldo atual é R${saldo:.2f}.")

    continuar = input("Deseja continuar jogando? (s/n): ").strip().lower()
    if continuar == "s":
        jogar(nome, saldo, param = "-n")
    else:
        print("Obrigado por jogar! Até a próxima! 🐯")

def main():
    print(" Bem-vindo ao Tigrinho 🐯 ")
    criar_banco()
    while True:
        escolha = input("Você já possui cadastro? (s/n): ").strip().lower()
        if escolha == "s":
            nome, saldo, status = login()
            if nome:
                break
        elif escolha == "n":
            nome, _, saldo, status = registrar()
            if nome:
                nome, saldo, status = login()
                if nome:
                    break
        else:
            print("Por favor, responda com 's' para sim ou 'n' para não.")
    jogar(nome, saldo, status)

if __name__ == "__main__":
    main()



