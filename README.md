# Tigrinho – Jogo de Aposta



## Introdução



O **Tigrinho** é um projeto desenvolvido para demonstrar conceitos de programação, manipulação de dados e lógica de controle em jogos de aposta. Inspirado em clássicos jogos de azar, o sistema simula um jogo de sorte que utiliza matrizes com símbolos para determinar o resultado de cada rodada. O projeto também ilustra como é possível manipular os dados de forma a permitir que apenas alguns jogadores obtenham ganhos significativos, garantindo que a empresa mantenha sua lucratividade.



## Descrição do Projeto



No Tigrinho, os usuários podem se cadastrar, fazer login, adicionar saldo e participar de rodadas de apostas. Cada rodada gera uma matriz 3x3 com símbolos aleatórios (representados por "💸", "🐅" e "🐯"). Em determinadas condições (quando o número aleatório gerado ultrapassa um limiar), o jogo força uma combinação vencedora em uma linha ou diagonal, resultando em um ganho para o jogador. Entretanto, o mecanismo de cálculo e atualização de saldo é cuidadosamente ajustado para que, a longo prazo, a empresa tenha lucro.



## Funcionalidades



- **Cadastro e Login:**  

  O sistema permite o registro de novos usuários e o login de usuários já cadastrados. São utilizados métodos para validar CPF e garantir que não haja duplicidade de cadastro.



- **Gestão de Saldo:**  

  Os usuários iniciam com um saldo padrão e podem adicionar créditos em valores pré-definidos (R$5, R$10, R$20 e R$50). O saldo é atualizado e persistido em um arquivo de texto (`usuarios.txt`).



- **Mecânica do Jogo:**  

  Em cada rodada, é gerada uma matriz com símbolos aleatórios. Em algumas situações, o jogo força a ocorrência de combinações vencedoras (diagonais ou linha central) para determinar o ganho, que é calculado por meio de um multiplicador aleatório.



- **Controle de Apostas:**  

  O sistema verifica se o saldo do usuário é suficiente para a aposta e, após cada rodada, atualiza o saldo conforme o resultado (ganho ou perda).



## Requisitos



- Python 3.7 ou superior.

- Ambiente de execução que permita entrada e saída via console.



## Estrutura do Código e Detalhamento das Funções



A seguir, uma explicação detalhada das funções e trechos principais do código:



### 1. Funções de Validação e Entrada



- **`verificar_resposta(valor)`**  

  *Propósito:*  

  Verifica se a resposta do usuário corresponde a alguma variação de “sim”.  

  *Código:*  

  ```python

  def verificar_resposta(valor):

      param = ["y", "s", "ye", "yes", "sim", "sin", "si"]

      resul = True if valor in param else False

      return resul

  ```

  

- **`entrada_valida(mensagem)`**  

  *Propósito:*  

  Garante que o usuário não deixe o campo vazio na entrada de dados.  

  *Código:*  

  ```python

  def entrada_valida(mensagem):

      while True:

          dado = input(mensagem).strip()

          if dado:

              return dado

          print("Preencha o campo vazio.")

  ```



- **`validar_cpf(cpf)`**  

  *Propósito:*  

  Realiza a validação básica do CPF, garantindo que seja composto por 11 dígitos numéricos.  

  *Código:*  

  ```python

  def validar_cpf(cpf):

      return len(cpf) == 11 and cpf.isdigit()

  ```



- **`verificar_existencia(usuario, cpf)`**  

  *Propósito:*  

  Verifica se o nome de usuário ou CPF já estão cadastrados no arquivo `usuarios.txt`, evitando duplicidade.  

  *Código:*  

  ```python

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

  ```



### 2. Cadastro, Login e Gestão de Saldo



- **`registrar()`**  

  *Propósito:*  

  Realiza o cadastro do usuário, coletando nome, CPF e senha, e registra um saldo inicial (R$10).  

  *Código:*  

  ```python

  def registrar():

      usuario = entrada_valida("Digite seu nome de usuário:")

      while True:

          cpf = input("Informe seu CPF:")

          if validar_cpf(cpf):

              break

          else:

              print("CPF inválido. Informe apenas números com 11 dígitos.")

      senha = entrada_valida("Digite sua senha:")

      if verificar_existencia(usuario, cpf):

          print("\n⚠️ Cadastro não permitido. Tente novamente.\n")

          return None, None, None

      saldo_inicial = 10

      with open("usuarios.txt", "a") as arquivo:

          arquivo.write(f"{usuario},{cpf},{senha},{saldo_inicial}\n")

      print("\n✅ Cadastro realizado com sucesso!")

      return usuario, senha, saldo_inicial

  ```



- **`login()`**  

  *Propósito:*  

  Permite o login do usuário, verificando as credenciais e recuperando o saldo atual.  

  *Código:*  

  ```python

  def login():

      while True:

          login_usuario = entrada_valida("Digite seu nome de usuário: ")

          login_senha = entrada_valida("Digite sua senha: ")

          with open("usuarios.txt", "r") as arquivo:

              usuarios_cadastrados = arquivo.readlines()

          for linha in usuarios_cadastrados:

              dados = linha.strip().split(",")

              if len(dados) == 4:

                  nome_salvo, _, senha_salva, saldo = dados

                  if login_usuario == nome_salvo and login_senha == senha_salva:

                      print("\n✅ Login realizado com sucesso! Bem-vindo de volta!")

                      return login_usuario, float(saldo)

          print("⚠️ Usuário ou senha incorretos. Tente novamente.")

  ```



- **`atualizar_saldo(usuario, novo_saldo)`**  

  *Propósito:*  

  Atualiza o saldo do usuário no arquivo `usuarios.txt`, garantindo a persistência dos dados após cada jogada.  

  *Código:*  

  ```python

  def atualizar_saldo(usuario, novo_saldo):

      linhas = []

      with open("usuarios.txt", "r") as arquivo:

          for linha in arquivo:

              dados = linha.strip().split(",")

              if len(dados) == 4 and dados[0] == usuario:

                  dados[3] = str(novo_saldo)

              linhas.append(",".join(dados))

      with open("usuarios.txt", "w") as arquivo:

          arquivo.write("\n".join(linhas) + "\n")

  ```



- **`adicionar_saldo(saldo)`**  

  *Propósito:*  

  Permite ao usuário adicionar créditos ao seu saldo, escolhendo entre valores pré-definidos.  

  *Código:*  

  ```python

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

  ```



### 3. Lógica do Jogo – O Tigrinho



- **`gerar_matriz()`**  

  *Propósito:*  

  Gera uma matriz 3x3 com símbolos aleatórios, representando o “tabuleiro” do jogo. Em determinadas condições, força a criação de combinações vencedoras (como linhas ou diagonais iguais), manipulando os resultados para que somente alguns jogadores ganhem, mantendo a lucratividade da empresa.  

  *Código:*  

  ```python

  def gerar_matriz():

      simbolos = ["💸", "🐅", "🐯"]

      matriz = [[random.choice(simbolos) for _ in range(3)] for _ in range(3)]

      sorte = random.randint(1, 10)

      if sorte > 8:

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

  ```



- **`verificar_vitoria_spin(matriz)`**  

  *Propósito:*  

  Verifica se a matriz gerada contém uma combinação vencedora nas diagonais ou na linha do meio. Retorna um valor booleano indicando vitória e a quantidade de formas vencedoras encontradas.  

  *Código:*  

  ```python

  def verificar_vitoria_spin(matriz):

      resul, quant = None, 0

      diagonal = matriz[0][0] == matriz[1][1] == matriz[2][2]

      diagonal2 = matriz[2][0] == matriz[1][1] == matriz[0][2]

      meio = matriz[1][0] == matriz[1][1] == matriz[1][2]

  

      vetor = [diagonal, diagonal2, meio]

      for valor in vetor:

          if valor == True:

              resul = True

              quant += 1

      return (resul, quant)

  ```



- **Função `calc_valor()` interna em `jogar()`**  

  *Propósito:*  

  Calcula um multiplicador para o valor apostado com base em uma combinação de números inteiros e frações, ponderados para favorecer a lucratividade da empresa.  

  *Código (resumido dentro de `jogar()`):*  

  ```python

  def calc_valor():

      numeros = [10, 20, 30, 50, 100]

      quebrados = random.randint(1, 101)

      pesos = [20, 8, 3, 2, 1]

      pesos_normalizados = [p / sum(pesos) for p in pesos]

  

      numero_aleatorio = random.choices(numeros, weights=pesos_normalizados, k=1)[0]

      numero = 1 + (numero_aleatorio + quebrados) / 100

      return float(f\"{numero:.2f}\")

  ```



- **`jogar(nome, saldo, param = \"-s\")`**  

  *Propósito:*  

  Gerencia o fluxo principal do jogo, controlando cada rodada (ou “giro”), atualizando o saldo do jogador conforme o resultado de cada aposta. Se o jogador vence (conforme a função de verificação de vitória), o saldo é aumentado multiplicando o valor apostado; caso contrário, o valor apostado é deduzido.  

  *Destaques do fluxo:*  

  - Exibição do saldo atual e opções de adicionar saldo.  

  - Solicitação do valor a ser apostado, com verificação de saldo disponível.  

  - Loop de rodadas onde:  

    - A matriz é gerada.  

    - O resultado é avaliado (função `verificar_vitoria_spin()`).  

    - Em caso de vitória, o multiplicador é calculado e o ganho é computado.  

    - Em caso de derrota, o valor apostado é subtraído do saldo.  

    - Pergunta ao usuário se deseja continuar jogando.  

  *Código (trecho principal):*  

  ```python

  def jogar(nome, saldo, param = "-s"):

      # [Código para adicionar saldo, se necessário]

      print("\nVamos comecar a jogar!\n")

  

      rodada, win_count = 0, 0

      saldo_aposta = float(input("Digite quanto vai querer apostar: "))

      while saldo_aposta > saldo:

          saldo_aposta = float(input("Saldo insuficiente. Por favor, insira um valor coerente: "))

      while True:

          rodada += 1

          print(f"\n=== Giro {rodada} ===")

  

          matriz = gerar_matriz()

          resultado, peso = verificar_vitoria_spin(matriz)

  

          if resultado:

              valor_sorteado = calc_valor()

              print(" WIIN!!")

              if peso > 1:

                  print(f\"Parabéns!!! Você ganhou de {peso} formas diferentes. Bonificação aplicada!\")

              valor_peso = valor_sorteado

              valor_ganho = saldo_aposta * valor_peso

              print(f"Valor Ganho {valor_ganho:.2f}")

              saldo += valor_ganho - saldo_aposta

              saldo_aposta = valor_ganho

              win_count += 1

          else:

              saldo -= saldo_aposta

              print(f"Você perdeu. Saldo restante: {saldo}")

              print("Não foi dessa vez. Tente mais uma!")

  

          resposta = input("\nDeseja continuar? ").lower()

          if not verificar_resposta(resposta):

              break

          # Verifica saldo para nova aposta

          elif resposta and saldo < saldo_aposta:

              print("Saldo insuficiente. Regarregue para continuar!")

              resp = input(f"Deseja apostar os seus {saldo} reais? ")

              if verificar_resposta(resp):

                  saldo_aposta = saldo

              else:

                  break

          elif saldo == 0:

              print("Sem saldo! Recarrege para continuar.")

              break

  

      atualizar_saldo(nome, saldo)

      print("\n=== Fim dos Giros ===")

      print(f"Você obteve {win_count} giro(s) vencedor(es).")

      print(f"Seu saldo atual é R${saldo}.")

  

      continuar = input("Deseja continuar jogando? (s/n): ").strip().lower()

      if continuar == "s":

          jogar(nome, saldo, param = "-n")

      else:

          print("Obrigado por jogar! Até a próxima! 🐯")

  ```



- **`main()`**  

  *Propósito:*  

  Ponto de entrada do programa. Gerencia o fluxo de cadastro/login e inicia o jogo.  

  *Código:*  

  ```python

  def main():

      print(" Bem-vindo ao Tigrinho 🐯 ")

      while True:

          escolha = input("Você já possui cadastro? (s/n): ").strip().lower()

          if escolha == "s":

              nome, saldo = login()

              if nome:

                  break

          elif escolha == "n":

              nome, _, saldo = registrar()

              if nome:

                  nome, saldo = login()

                  if nome:

                      break

          else:

              print("Por favor, responda com 's' para sim ou 'n' para não.")

      jogar(nome, saldo)

  

  if __name__ == "__main__":

      main()

  ```



## Considerações sobre a Manipulação dos Dados



O jogo é projetado para favorecer a empresa de apostas. A manipulação ocorre em dois pontos críticos:

- **Geração da Matriz:**  

  Ao gerar a matriz de símbolos, há uma chance (quando o número aleatório `sorte` é maior que 8) de forçar uma combinação vencedora. Essa “ajuste” na geração das combinações garante que somente em situações controladas ocorra o pagamento, balanceando os ganhos e perdas.

- **Cálculo do Multiplicador:**  

  O multiplicador aplicado ao valor apostado é calculado de forma a oferecer ganhos atrativos apenas em casos de múltiplas vitórias, mantendo uma probabilidade menor de ocorrência e, assim, assegurando a margem de lucro para a empresa.



## Conclusão



O projeto **Tigrinho** serve como uma aplicação prática dos conceitos de manipulação de dados, controle de fluxo e lógica de programação. Além de demonstrar a implementação de um sistema de apostas, o projeto destaca a importância do controle das condições de vitória para garantir a sustentabilidade financeira da operação.



---



Este README destina-se a ser uma documentação completa para a apresentação do projeto na disciplina de Fundamentos da Computação, evidenciando o detalhamento de cada função e a lógica de negócio aplicada. Se houver necessidade de maiores ajustes ou acréscimos, sinta-se à vontade para propor melhorias.



