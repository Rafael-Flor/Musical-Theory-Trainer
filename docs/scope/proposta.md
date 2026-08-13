# Proposta de Projecto

**Título:** Musical Theory Trainer 
Com Geração Procedural e Avaliação Automática   
**Estudante:** Rafael Gomes Flor · 2202933  
**Orientador:** Pedro Pestana  
**Data:** 25/03/26 
**Versão:** 1.0

---

## Sinopse

O estudo de conceitos de teoria musical constitui uma base importante para quem esteja 
interessado em aprender música pela primeira vez ou desenvolver competências 
musicais já adquiridas. Entre os conceitos teóricos e a sua aplicação prática existe um 
espaço que pode ser preenchido por métodos e ferramentas de aprendizagem que 
permitam treinar e solidificar estas competências musicais. É neste espaço que a 
presente proposta se insere. 

Pretende-se desenvolver uma aplicação que possa ser utilizada como um treinador de 
teoria musical, permitindo um utilizador praticar conceitos sob o formato de exercícios 
gerados automaticamente. A aplicação deverá apresentar uma interface gráfica e 
fornecer uma seleção de exercícios interativos, que incidam sobre certas componentes 
de teoria musical, tais como o reconhecimento de escalas e progressões harmónicas. De 
modo a permitir um melhor acompanhamento pelo utilizador, cada conjunto de 
exercícios deve terminar com uma avaliação de desempenho. 

Atualmente, existem diversas aplicações destinadas à aprendizagem musical, 
abrangendo desde as abordagens mais teóricas, como questionários sobre conceitos de 
teoria musical, até aos mais práticos, como o ensino da execução de peças musicais num 
dado instrumento. No entanto, estas soluções baseiam-se frequentemente em exercícios 
pré-definidos. A presente proposta pretende fornecer exercícios gerados 
automaticamente, possibilitando que o utilizador resolva uma maior variedade de 
exercícios e abrindo a possibilidade de personalização no processo de aprendizagem. 

Com o desenvolvimento desta aplicação pretende-se criar uma ferramenta didática, 
através da qual um utilizador deva ser capaz de aprender e praticar conceitos de teoria 
musical, segundo uma abordagem teórico-prática.



---

## MVP — Definição e critérios de aceitação


### Interface gráfica 

A aplicação deverá apresentar uma interface gráfica que permita ao utilizador navegar 
pelo conteúdo da aplicação e realizar exercícios de forma interativa.  

**Critério de aceitação:**  
Dado que o utilizador se encontra num determinado ecrã, quando o utilizador interage 
com os controlos disponibilizados pela interface, a aplicação deve exibir o ecrã correto 
e/ou executar as funcionalidades relacionadas com a opção selecionada.

### Menu para seleção de exercícios  

A interface gráfica deverá apresentar um menu que permita ao utilizador selecionar os 
tipos de exercícios que pretende fazer. As opções devem representar conjuntos de 
exercícios do mesmo tipo.  

**Critério de aceitação:**  
Dado que o utilizador se encontra no menu de seleção de exercícios, quando escolhe 
uma das opções disponíveis, a aplicação deve exibir um ecrã onde o utilizador possa 
realizar os exercícios, apresentando todo o conteúdo e controlos necessários para esse 
efeito.  

Dado que o utilizador seleciona uma das opções de exercícios, quando os exercícios são 
exibidos, a aplicação deve garantir que os exercícios fornecidos correspondem à escolha 
do utilizador. 

### Geração automática de exercícios 

A partir de formalizações e generalizações dos conceitos musicais envolvidos no 
conjunto de exercícios escolhido pelo utilizador, a aplicação deverá ser capaz de gerar 
uma série de exercícios automaticamente. 

**Critério de aceitação:**  
Dada a solicitação de um exercício pelo utilizador, este deve ser gerado 
automaticamente pela aplicação. 

Dado que o utilizador seleciona a opção de realizar exercícios, quando um exercício é 
gerado, a aplicação deve produzir e apresentar somente exercícios que respeitem os 
fundamentos teóricos e que sejam musicalmente corretos.

### Exercícios disponibilizados  

A aplicação deverá disponibilizar os seguintes tipos de exercícios: 

•   Reconhecimento de intervalos no contexto de uma escala musical – O utilizador é 
informado da escala sobre a qual o exercício incide. São reproduzidos dois sons, o 
primeiro corresponderá à tónica da escala e o próximo a qualquer outra nota da 
escala. O utilizador deve identificar o intervalo entre as duas notas musicais no 
contexto dessa escala. 

•   Reconhecimento de progressões harmónicas- Deve ser reproduzido o áudio de uma 
certa progressão harmónica e ser pedido ao utilizador para identificar o tipo de 
progressão. 

**Critério de aceitação:** 
Dado que o utilizador tenha solicitado um exercício de reconhecimento de intervalos, 
quando o exercício é apresentado, os sons das notas que constituem o exercício devem 
ser reproduzidos, devendo também ser fornecidos controlos para reproduzir o áudio 
novamente e para submeter a resposta num formato de escolha múltipla. 

Dado que o utilizador tenha solicitado um exercício de reconhecimento de progressões 
harmónicas, quando o exercício é apresentado, deve ser reproduzido o áudio da 
progressão, devendo também ser fornecidos controlos para reproduzir o áudio 
novamente e escolha de uma resposta em formato de escolha múltipla.   

Dado que o utilizador esteja a realizar um exercício, quando submete a resposta, deve 
ser indicado se a resposta se encontra correta ou errada.  

Dado que a resposta está incorreta, após o utilizador submeter uma resposta, deve ser 
indicada a solução correta do exercício em conjunto com uma explicação. 

### Avaliação do desempenho  

No final da realização dos vários exercícios da opção selecionada, deve ser fornecido ao 
utilizador uma avaliação de desempenho. Esta avaliação deve representar o desempenho 
conjunto nos exercícios realizados.  

**Critério de aceitação:** 
Dado que o utilizador termina de realizar um conjunto de exercícios, após terminar o 
último exercício, é fornecida uma avaliação que resume o seu desempenho, indicando o 
número de exercícios certos e errados. 

---

## Calendário individual detalhado

| Semanas | Datas | Conteúdo planeado |
|---------|-------|------------------|
| Sem. 1–2 | 16–29 mar  | Apresentação da proposta de projeto (até 25 de março) |
| Sem. 3–4 | 30 mar–12 abr  |  Levantamento de requisitos (MoSCoW). Modelação da arquitetura (C4 nível 1 e 2). Conceção do modelo de dados preliminar.   | 
| Sem. 5–6 | 13–26 abr  | Protótipo de navegação. Elaboração de ADRs das principais decisões de arquitetura. Início de implementação do núcleo.  | 
| Sem. 7 | 27 abr–3 mai  | Finalização de tarefas pendentes. Ponto de situação e demo interna com o orientador. Validação de âmbito para o intercalar.   | 
| Sem. 8 | 4–6 mai | Submissão do relatório intermédio: (até dia 6 de maio) - Capítulos 1 (Introdução) e 2 (Desenho) completos. Estado de implementação documentado no Cap. 3.  | 
| Sem. 8–9 | 7–17 mai  | Implementação das funcionalidades secundárias. Testes unitários e de integração do núcleo. Identificação e documentação de limitações. | 
| Sem. 10–11 | 18–31 mai  | Implementação completa do MVP. Testes de funcionalidade e desempenho. Capturas de ecrã e exemplos de execução para Cap. 4.  | 
| Sem. 12 | 1–7 jun  | Revisão geral do sistema. Polimento de interface. Validação dos critérios de aceitação definidos na proposta.  | 
| Sem. 13 | 8–14 jun  | Redação dos Capítulos 4 (Testes) e 5 (Conclusões).  Revisão bibliográfica e formatação APA.  Preparação dos anexos. | 
| Sem. 14 | 15–21 jun  | Reunião de preparação para defesa com o orientador. Revisão final do relatório e verificação de coerência com o repositório.  |
| Sem. 15 | 22-24 jun  | Submissão do Relatório final, código e demo. (até 24 de junho)  | 
