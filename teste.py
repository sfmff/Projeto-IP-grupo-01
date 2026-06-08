# apresentação e nome

print("Olá, eu sou o BMO! Prazer em te conhecer, estranho!")
print("Qual é o seu nome?")
nome = input()
if nome == "Jake" or nome == "Finn":
  print("Caramba, que coincidência! Você tem o mesmo nome de um amigo meu!")
print("Gostei do seu nome!")

# idade

print("Quantos anos você tem?")
idade = int(input())
if idade == 12:
  print("Nossa, você tem a mesma idade do meu amigo Finn")
print("Entendi!")

# princesa bonita

print("Ei, qual princesa desse mundo é a mais bonita pra você?")
princesa = input()
if princesa == "Princesa de Fogo" or princesa == "Princesa Jujuba":
  print("Meu amigo Finn vai ficar com ciúmes de você!")

# despedida

print("Finalmente chegamos!")
print(f'Foi um prazer te conhecer, {nome}! Boa sorte para encontrar a {princesa} :)')
