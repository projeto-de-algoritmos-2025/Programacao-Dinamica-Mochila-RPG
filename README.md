# Mochila RPG

**Conteúdo da Disciplina**: Programação Dinâmica

## Alunos

<table>
  <tr>
    <td align="center"><a href="https://github.com/luanasoares0901"><img style="border-radius: 60%;" src="https://github.com/luanasoares0901.png" width="200px;" alt=""/><br /><sub><b>Luana Ribeiro</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/MMcLovin"><img style="border-radius: 60%;" src="https://github.com/MMcLovin.png" width="200px;" alt=""/><br /><sub><b>Gabriel Fernando de Jesus Silva</b></sub></a><br /></td>
  </tr>
</table>

## Sobre

Este projeto tem como objetivo desenvolver uma aplicação interativa que apresenta um algoritmo para solucionar o Knapsack Problem através de Programação Dinâmica em um contexto de jogos RPG. Inspirado no jogo Skyrim, as diferentes espécies de personagens (elfos, orcs, khajiit) podem preencher seu arsenal com os itens disponíveis. No entanto, cada item possui um valor e peso, além de possuir afinidade ou não com a espécie citada, por exemplo: caso o personagem seja um orc ou nord, que possuem suas habilidades atreladas à espadas e escudos de defesa, não faz sentido que ele escolha um arco omo item de seu arsenal. Dessa forma, o algoritmo escolhe os itens ideais para o personagem baseados no peso e valor dos mesmos. Ademais, é possível escoher explorar a dungeon e verificar quais itens foram utilizados e quais foram encontrados, executando o Knapsack de forma inversa descartando itens pesados da mochila caso sejam encontrados itens mais valiosos. 


### Exemplo grade e planejamento gerados com o algoritmo

![Inventário](/assets/inventario.png)
![Dungeon](/assets/dungeon.png)

## Linguagem e Bibliotecas

* **Linguagem**: Python
* **Principais Bibliotecas utilizadas**: Flet (para criação de interfaces web interativas)

## Apresentação

A apresentação do projeto pode ser acessada [aqui](https://www.youtube.com/watch?v=lM9NoJa0Y-k).

## Guia de instalação 

### Pré-requisitos

- Git (versão 2.40 ou superior);
- Python (versão 3.12 ou superior);

### Clonando o repositório

- O primeiro passo é clonar o repositório do projeto do GitHub.

```bash
git clone https://github.com/projeto-de-algoritmos-2025/Programacao-Dinamica-Mochila-RPG.git

cd Programacao-Dinamica-Mochila-RPG
```

### Executando o projeto

- Recomendamos criar e ativar um ambiente virtual novo para o projeto. Para isso, utilize os comandos abaixo:

```bash
python -m venv env
.\env\Scripts\activate
```

- Em seguida, instale as dependências:

```bash
pip install flet
```

- Após instalar as dependências, execute o comando a partir da raiz do projeto (`rpg_knapsack`):

```bash
python app.py
```