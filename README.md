Segue abaixo o README atualizado, com as novas funcionalidades e explicações detalhadas:

---

# Tigrinho – Jogo de Aposta

## Introdução

O **Tigrinho** é um projeto desenvolvido para demonstrar conceitos de programação, manipulação de dados e lógica de controle em jogos de aposta. Inspirado em clássicos jogos de azar, o sistema simula um jogo de sorte em que os jogadores apostam em rodadas baseadas em matrizes de símbolos. O projeto ainda ilustra como a manipulação dos dados pode ser ajustada para favorecer a lucratividade da empresa, permitindo que apenas alguns jogadores obtenham ganhos significativos.

Adicionalmente, o sistema agora incorpora uma funcionalidade de _influencer_, que possibilita condições diferenciadas para certos usuários, além de um módulo robusto de gerenciamento do banco da empresa, que controla o saldo total e mantém um histórico das transações.

## Descrição do Projeto

No Tigrinho, os usuários podem:

- **Cadastrar-se** e **realizar login** com validação de CPF e verificação de duplicidade.
- **Adicionar saldo** e acompanhar seu saldo atualizado, armazenado em um arquivo de texto.
- Jogar rodadas de apostas onde é gerada uma matriz 3x3 com símbolos aleatórios ("💸", "🐅" e "🐯").
- Ganhar ou perder conforme a combinação dos símbolos e o cálculo de um multiplicador aleatório, ajustado para preservar a margem de lucro da empresa.
- Contar com um **módulo de gerenciamento do banco**, que registra o saldo total da empresa e um histórico de todas as transações financeiras.

Além disso, foi incorporada uma funcionalidade para **influencers** – um status especial que pode alterar a probabilidade de vitórias. Usuários com status _influencer_ (representado por `1`) terão condições de jogo diferenciadas, refletidas na geração da matriz de símbolos e na probabilidade de ocorrer combinações vencedoras.

## Funcionalidades

- **Cadastro e Login com Status Influencer:**  
  O cadastro foi atualizado para incluir um parâmetro `influencer`, que pode ser `0` (usuário normal) ou `1` (influencer). No login, o sistema agora recupera e retorna esse status para ajustar posteriormente as condições de jogo.

- **Gestão de Saldo dos Usuários:**  
  Cada usuário inicia com um saldo padrão e pode adicionar créditos (valores pré-definidos: R$5, R$10, R$20 e R$50). O saldo é atualizado em um arquivo `usuarios.txt`.

- **Mecânica do Jogo – Geração da Matriz e Cálculo de Ganhos:**  
  A cada rodada, uma matriz 3x3 é gerada. Em certas condições – determinadas por um número aleatório e ajustadas pelo status do usuário e pelo saldo atual do banco – uma combinação vencedora é forçada (na diagonal ou na linha do meio). O ganho é calculado a partir de um multiplicador que também depende da quantidade de formas vencedoras.

- **Controle de Apostas e Atualização do Banco:**  
  Se o jogador ganhar, o sistema desconta o valor do ganho do banco (para preservar a margem de lucro). Se perder, o valor apostado é creditado ao banco. Todas as transações são registradas e o saldo do banco é atualizado e consultado através do módulo de gerenciamento.

- **Gerenciamento do Banco:**  
  Possui funções para:  
  - Criar e inicializar o banco com um saldo pré-definido (R$50.000).  
  - Atualizar o saldo do banco e manter um histórico de transações.  
  - Consultar o saldo atual do banco.

## Requisitos

- Python 3.7 ou superior.
- Ambiente de execução com suporte a entrada e saída via console.

## Estrutura do Código e Detalhamento das Funções

### 1. Funções de Validação e Entrada

- **`verificar_resposta(valor)`**  
  Verifica se a resposta do usuário é uma variação de “sim” para continuar a execução.  
  ```python
  def verificar_resposta(valor):
      param = ["y", "s", "ye", "yes", "sim", "sin", "si"]
      resul = True if valor in param else False
      return resul
  ```

- **`entrada_valida(mensagem)`**  
  Garante que o usuário não deixe o campo vazio na entrada de dados.  
  ```python
  def entrada_valida(mensagem):
      while True:
          dado = input(mensagem).strip()
          if dado:
              return dado
          print("Preencha o campo vazio.")
  ```

- **`validar_cpf(cpf)`**  
  Realiza a validação básica do CPF (11 dígitos numéricos).  
  ```python
  def validar_cpf(cpf):
      return len(cpf) == 11 and cpf.isdigit()
  ```

- **`verificar_existencia(usuario, cpf)`**  
  Verifica se o nome de usuário ou CPF já foram cadastrados no arquivo `usuarios.txt`, evitando duplicidades.  
  ```python
  def verificar_existencia(usuario, cpf):
      try:
          with open("usuarios.txt", "r") as arquivo:
              for linha in arquivo:
                  dados = linha.strip().split(",")
                  if len(dados) >= 4:
                      nome_salvo, cpf_salvo, _, _ = dados[:4]
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

### 2. Cadastro e Login com Status Influencer

- **`registrar(influencer=0)`**  
  *Propósito:*  
  Realiza o cadastro do usuário, coletando nome, CPF, senha e o status _influencer_. Caso o usuário seja influencer, o valor `1` é registrado; caso contrário, `0`. O usuário inicia com saldo padrão de R$10.  
  *Código:*  
  ```python
  def registrar(influencer=0):
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
  ```

- **`login()`**  
  *Propósito:*  
  Permite o login do usuário, validando as credenciais e retornando o saldo atual e o status _influencer_ (armazenado no arquivo).  
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
              if len(dados) == 5:
                  nome_salvo, _, senha_salva, saldo, status = dados
                  if login_usuario == nome_salvo and login_senha == senha_salva:
                      print("\n✅ Login realizado com sucesso! Bem-vindo de volta!")
                      return login_usuario, float(saldo), status
          print("⚠️ Usuário ou senha incorretos. Tente novamente.")
  ```

### 3. Lógica do Jogo

- **`gerar_matriz(status)`**  
  *Propósito:*  
  Gera uma matriz 3x3 com símbolos aleatórios e, dependendo do status do usuário (_influencer_) e do saldo atual do banco, ajusta a probabilidade de gerar uma combinação vencedora (diagonais ou linha central).  
  *Detalhes:*  
  - Converte o parâmetro `status` para inteiro e define a variável `influencer` como `True` se for igual a 1.  
  - Consulta o saldo atual do banco para ajustar a variável `K`, que determina a chance de vitória.  
    - Se o usuário for influencer, `K` inicia em 4; caso contrário, em 7.  
    - Se o saldo do banco for menor ou igual a R$40.000, `K` é incrementado (mais para influencers).  
  - Se um número aleatório (`sorte`) for maior que `K`, o jogo força uma combinação vencedora.  
  *Código:*  
  ```python
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
          formato = "  " if i != 1 else "->"
          print(formato, " | ".join(linha).strip())
      print("-" * 20)
  
      return matriz
  ```

- **`jogar(nome, saldo, status, param="-s")`**  
  *Propósito:*  
  Gerencia o fluxo do jogo, controlando cada rodada e atualizando tanto o saldo do jogador quanto o saldo do banco conforme o resultado.  
  *Detalhes:*  
  - Exibe o saldo atual e oferece a opção de adicionar saldo.  
  - Solicita o valor a ser apostado e valida se o saldo do jogador é suficiente.  
  - Em cada rodada, gera a matriz chamando `gerar_matriz(status)`, verifica o resultado e calcula o ganho usando um multiplicador (função `calc_valor()` interna).  
  - Se o jogador ganhar, o valor ganho é subtraído do banco (usando `config_banco(-valor_ganho)`); se perder, o valor apostado é creditado ao banco (usando `config_banco(saldo_aposta)`).  
  - Atualiza o saldo do usuário e pergunta se deseja continuar jogando.  
  *Código (trecho principal):*  
  ```python
  def jogar(nome, saldo, status, param="-s"):
      def calc_valor():
          numeros = [10, 20, 30, 50, 100]
          quebrados = random.randint(1, 101)
          pesos = [20, 8, 3, 2, 1]
          pesos_normalizados = [p / sum(pesos) for p in pesos]
  
          numero_aleatorio = random.choices(numeros, weights=pesos_normalizados, k=1)[0]
          numero = 1 + (numero_aleatorio + quebrados) / 100
          format_valor = f"{numero:.2f}"
          return float(format_valor)
  
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
          jogar(nome, saldo, status, param="-n")
      else:
          print("Obrigado por jogar! Até a próxima! 🐯")
  ```

### 4. Gerenciamento do Banco

Para garantir a sustentabilidade financeira da empresa, o módulo do banco controla o saldo total e mantém um histórico das transações.

- **`criar_banco()`**  
  Inicializa o banco com um saldo pré-definido de R$50.000 e grava o histórico inicial.  
  ```python
  def criar_banco():
      with open("banco.txt", "a") as arquivo:
          saldo_inicial = 50000
          historico = str(saldo_inicial)
          arquivo.write(f"{saldo_inicial} - {historico}\n")
  ```

- **`config_banco(valor)`**  
  Atualiza o saldo do banco somando (ou subtraindo) o valor recebido e registra o histórico de alterações.  
  ```python
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
  ```

- **`banco_atual()`**  
  Retorna o saldo atual do banco, conforme registrado no arquivo.  
  ```python
  def banco_atual():
      with open("banco.txt", "r") as arquivo:
          linhas = arquivo.readlines()
          if linhas:
              saldo_atual, _ = linhas[0].strip().split(" - ")
              saldo_atual = float(saldo_atual)
          return saldo_atual
  ```

### 5. Função Principal

- **`main()`**  
  Gerencia o fluxo de cadastro (com opção de registro para influencers), login e inicia o jogo. Também chama a função de criação do banco para garantir que o sistema financeiro esteja inicializado.  
  ```python
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
  ```

## Considerações sobre a Manipulação dos Dados

- **Geração da Matriz:**  
  A função `gerar_matriz(status)` ajusta a chance de vitória com base no status do usuário (influencer) e no saldo do banco. Isso permite condições de jogo diferenciadas que podem favorecer jogadores especiais, mas também protege a margem de lucro da empresa.

- **Cálculo do Multiplicador:**  
  A função interna `calc_valor()` em `jogar()` determina um multiplicador que pode aumentar significativamente os ganhos, especialmente quando múltiplas formas vencedoras são identificadas na matriz.

- **Gerenciamento do Banco:**  
  Todas as transações (ganhos ou perdas) são refletidas no saldo do banco por meio das funções `config_banco(valor)` e `banco_atual()`, permitindo monitorar e ajustar a sustentabilidade financeira do sistema.

## Conclusão

O projeto **Tigrinho** demonstra de forma prática conceitos avançados de programação e manipulação de dados em um sistema de apostas. Com as novas atualizações, o sistema incorpora a funcionalidade de _influencer_, condições diferenciadas de vitória e um módulo de gerenciamento financeiro robusto, garantindo transparência e sustentabilidade para a operação.
