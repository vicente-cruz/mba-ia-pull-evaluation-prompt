# Evidências da avaliação

Registros das três iterações e detalhes de três exemplos da iteração final, experimento `vicente-cruz-bug_to_user_story_v2-d0395f7a`, commit do Prompt Hub `bda84afa`.

[Voltar ao README do projeto](../../README.md) · [Dataset público e experimentos](https://smith.langchain.com/public/a8b0113b-56e7-4d9d-9849-0156f68fb3ac/d)

Os arquivos de imagem foram preservados sem edição. As linhas 4, 5 e 7 correspondem à ordenação da tabela capturada, não a identificadores permanentes. As capturas mostram entrada, resposta e feedback, além da árvore de chamadas de geração dos três exemplos: `Target`, `RunnableSequence`, `ChatPromptTemplate` e `ChatOpenAI`. As visões de trace identificam o modelo, a duração e as cinco notas; não representam o pensamento interno do modelo.

## Visão geral

![Comparação das três iterações](comparacao-iteracoes.png)

![Quinze exemplos e médias da iteração final](avaliacao-final.png)

## Logs de execução

- [Iteração 1](avaliacao-iteration-01.txt)
- [Iteração 2](avaliacao-iteration-02.txt)
- [Iteração 3 selecionada](avaliacao-iteration-03.txt)

## Linha 4 — Relatório de vendas

![Árvore de chamadas e feedbacks — linha 4](l4-trace.png)

Helpfulness: 0,875; Correctness: 0,835; F1: 0,80; Clarity: 0,88; Precision: 0,87.

<details>
<summary>Entrada — 1 captura(s)</summary>

![Linha 4 — Entrada — l4-input.png](l4-input.png)

</details>

<details>
<summary>Resposta gerada — 2 captura(s)</summary>

![Linha 4 — Resposta gerada — l4-output01.png](l4-output01.png)

![Linha 4 — Resposta gerada — l4-output02.png](l4-output02.png)

</details>

<details>
<summary>Notas e justificativas — 5 captura(s)</summary>

![Linha 4 — Notas e justificativas — l4-nota01.png](l4-nota01.png)

![Linha 4 — Notas e justificativas — l4-nota02.png](l4-nota02.png)

![Linha 4 — Notas e justificativas — l4-nota03.png](l4-nota03.png)

![Linha 4 — Notas e justificativas — l4-nota04.png](l4-nota04.png)

![Linha 4 — Notas e justificativas — l4-nota05.png](l4-nota05.png)

</details>

## Linha 5 — Adicionar ao carrinho

![Árvore de chamadas e feedbacks — linha 5](l5-trace.png)

Helpfulness: 0,875; Correctness: 0,9237; F1: 0,9474; Clarity: 0,85; Precision: 0,90.

<details>
<summary>Entrada — 1 captura(s)</summary>

![Linha 5 — Entrada — l5-input.png](l5-input.png)

</details>

<details>
<summary>Resposta gerada — 1 captura(s)</summary>

![Linha 5 — Resposta gerada — l5-output.png](l5-output.png)

</details>

<details>
<summary>Notas e justificativas — 2 captura(s)</summary>

![Linha 5 — Notas e justificativas — l5-nota01_02_03.png](l5-nota01_02_03.png)

![Linha 5 — Notas e justificativas — l5-nota04_05.png](l5-nota04_05.png)

</details>

<details>
<summary>Resposta de referência — 1 captura(s)</summary>

![Linha 5 — Resposta de referência — l5-reference-output.png](l5-reference-output.png)

</details>

## Linha 7 — Sincronização offline

![Árvore de chamadas e feedbacks — linha 7](l7-trace.png)

Helpfulness: 0,925; Correctness: 0,9244; F1: 0,9189; Clarity: 0,92; Precision: 0,93.

<details>
<summary>Entrada — 3 captura(s)</summary>

![Linha 7 — Entrada — l7-input01.png](l7-input01.png)

![Linha 7 — Entrada — l7-input02.png](l7-input02.png)

![Linha 7 — Entrada — l7-input03.png](l7-input03.png)

</details>

<details>
<summary>Resposta gerada — 3 captura(s)</summary>

![Linha 7 — Resposta gerada — l7-output01.png](l7-output01.png)

![Linha 7 — Resposta gerada — l7-output02.png](l7-output02.png)

![Linha 7 — Resposta gerada — l7-output03.png](l7-output03.png)

</details>

<details>
<summary>Notas e justificativas — 2 captura(s)</summary>

![Linha 7 — Notas e justificativas — l7-nota01_02_03.png](l7-nota01_02_03.png)

![Linha 7 — Notas e justificativas — l7-nota04_05.png](l7-nota04_05.png)

</details>

<details>
<summary>Resposta de referência — 7 captura(s)</summary>

![Linha 7 — Resposta de referência — l7-reference-output01.png](l7-reference-output01.png)

![Linha 7 — Resposta de referência — l7-reference-output02.png](l7-reference-output02.png)

![Linha 7 — Resposta de referência — l7-reference-output03.png](l7-reference-output03.png)

![Linha 7 — Resposta de referência — l7-reference-output04.png](l7-reference-output04.png)

![Linha 7 — Resposta de referência — l7-reference-output05.png](l7-reference-output05.png)

![Linha 7 — Resposta de referência — l7-reference-output06.png](l7-reference-output06.png)

![Linha 7 — Resposta de referência — l7-reference-output07.png](l7-reference-output07.png)

</details>

## Leitura dos resultados

As cinco médias do experimento final superaram 0,8. Isso não significa que todas as notas individuais superaram esse limite. As limitações da avaliação, incluindo os resultados do modal e detalhes presentes apenas nas referências, estão descritas no README principal.

As respostas de referência são alvos do dataset fornecido pelo desafio. Elas não são respostas geradas pelo prompt desta entrega. Os comentários dos avaliadores são evidências do julgamento realizado e também podem conter inconsistências.
