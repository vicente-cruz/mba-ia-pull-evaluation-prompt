# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

Projeto do MBA em Engenharia de Software com IA — Full Cycle. Implementa o pull de um prompt inicial, sua otimização em YAML, a publicação no LangSmith Prompt Hub e a avaliação de User Stories geradas a partir de relatos de bugs.

**Resultado registrado em 27/09/2026:** três iterações avaliadas com 15 exemplos cada; a versão escolhida obteve média geral **0,9136 (91,36%)**, com as cinco métricas agregadas acima de 0,8. Os sete testes de validação passaram.

- Autor e handle do Hub: **Vicente Cruz / `vicente-cruz`**.
- [Repositório desta implementação](https://github.com/vicente-cruz/mba-ia-pull-evaluation-prompt).
- [Repositório base](https://github.com/devfullcycle/mba-ia-pull-evaluation-prompt).
- [Dataset público e experimentos](https://smith.langchain.com/public/a8b0113b-56e7-4d9d-9849-0156f68fb3ac/d).
- [Enunciado original preservado](docs/enunciado-original.md).

## Implementação

| Arquivo | Responsabilidade |
| --- | --- |
| `src/pull_prompts.py` | Baixa `leonanluppi/bug_to_user_story_v1`, valida as mensagens e salva o YAML local. |
| `prompts/bug_to_user_story_v1.yml` | Prompt inicial, preservado como base de comparação. |
| `prompts/bug_to_user_story_v2.yml` | Prompt otimizado com Few-shot e Role Prompting; revisão final `iteration-03`. |
| `src/push_prompts.py` | Valida o YAML, monta o `ChatPromptTemplate` e publica o prompt com descrição, tags e metadados. |
| `tests/test_prompts.py` | Seis testes exigidos e um teste adicional de separação das mensagens e preservação de `bug_report`. |
| `src/evaluate.py` | Avaliação e gravação do experimento e feedbacks no LangSmith; fornecido pelo desafio. |
| `src/metrics.py` | Implementação das métricas; fornecido pelo desafio. |
| `src/utils.py` | Configuração de modelos e funções auxiliares; fornecido pelo desafio. |
| `datasets/bug_to_user_story.jsonl` | Dataset original com 15 exemplos: 5 simples, 7 médios e 3 complexos. |
| `docs/evidencias/` | Logs, screenshots e índice dos exemplos inspecionados. |

O avaliador, as métricas, as funções auxiliares e o dataset foram mantidos sem alterações. A otimização foi realizada no prompt. O suporte original a OpenAI e Gemini foi preservado; os experimentos documentados utilizaram OpenAI.

O pull utiliza `Client.pull_prompt(..., include_model=False, dangerously_pull_public_prompt=True)` para o prompt público indicado no enunciado. O push utiliza `Client.push_prompt(..., is_public=True)`. Nenhuma dessas duas etapas precisa gerar respostas com um LLM.

## Técnicas Aplicadas (Fase 2)

### Few-shot Learning

**Por que usar:** demonstrar concretamente o formato, a profundidade e o comportamento esperado costuma ser mais claro do que apenas descrever regras abstratas.

O `system_prompt` contém três pares autorais de entrada e saída, diferentes dos exemplos do dataset de avaliação:

1. **Favoritos em um catálogo de biblioteca:** demonstra uma história curta, critérios verificáveis e contexto breve para um defeito simples.
2. **Reservas de salas:** demonstra cobertura separada de concorrência, cache e geração de comprovantes, com propostas técnicas relacionadas às evidências.
3. **“Deu problema. Não funciona.”:** demonstra como solicitar informações quando não há um defeito identificável, sem inventar uma história.

Trecho do primeiro exemplo:

> Entrada: No catálogo da biblioteca, clico em "Favoritar" no livro 876, mas ele não aparece na minha lista de favoritos após atualizar a página.
>
> Saída: Como um leitor do catálogo, eu quero salvar livros nos meus favoritos, para que eu possa encontrá-los novamente quando quiser consultá-los.

Na segunda iteração, foram removidos desse exemplo os cenários adicionais de duplicação e erro ao salvar. A intenção foi ensinar concisão para relatos simples também pelo exemplo, não apenas pelas instruções.

### Role Prompting

**Por que usar:** estabelecer o papel, o público e a responsabilidade do modelo ao transformar sintomas em requisitos úteis para produto, desenvolvimento e testes.

O prompt começa com:

> Você é um Product Manager com experiência em análise de requisitos e qualidade de software.

O papel é acompanhado de regras concretas: preservar os fatos do relato, explicitar o benefício para o usuário, escrever critérios observáveis, separar sugestões técnicas de requisitos e não inventar tecnologias, causas confirmadas, prazos ou SLAs.

As duas técnicas estão registradas no YAML:

```yaml
version: "v2"
revision: "iteration-03"
techniques_applied: ["few-shot", "role-prompting"]
```

A organização em seções de Markdown é uma regra de formato; não foi contabilizada como uma terceira técnica.

### Separação de mensagens e casos excepcionais

O **System Prompt** contém persona, regras, formato e exemplos. O **User Prompt** contém uma única ocorrência de `{bug_report}`, delimitada por `<relato_de_bug>`. Isso elimina a duplicação do relato que existia em v1.

O prompt também orienta a tratar relatos vazios, informação insuficiente, contradições, dados sensíveis e instruções maliciosas dentro do relato. Metas numéricas não informadas devem ser confirmadas, e comportamentos complementares devem ser identificados como propostas. Essas são instruções de comportamento, não garantias de que o modelo sempre as seguirá.

## Processo de otimização

Foram executadas três revisões de `bug_to_user_story_v2`. Cada revisão foi validada com pytest, publicada no Hub e avaliada contra o mesmo dataset, mantendo os mesmos modelos.

| Iteração | Commit do prompt no Hub | Alteração e motivação |
| --- | --- | --- |
| `iteration-01` | `45bfd126` | Introdução de persona, três exemplos, formato Markdown, critérios de aceitação e regras para casos excepcionais. A análise do caso do carrinho revelou expansão excessiva, perguntas dispensáveis e cenários não necessários. |
| `iteration-02` | `6d8f8e65` | Redução de detalhes em casos simples, revisão do exemplo Few-shot e critérios que exigem a correção funcionando. A inspeção dos casos de relatório e modal mostrou necessidade de melhorar a cobertura técnica. |
| `iteration-03` | `bda84afa` | Distinção explícita entre relatos simples e técnicos, separação entre timeout e meta de desempenho, critérios observáveis e propostas de interação e acessibilidade em modais. Selecionada para a entrega. |

Esses identificadores são commits do **Prompt Hub**, não commits do GitHub. As três revisões mantêm o nome `vicente-cruz/bug_to_user_story_v2`; o campo `revision` distingue as iterações no YAML e é incluído nos metadados e na descrição do commit publicado.

### Comparação entre v1 e v2

| Aspecto | Prompt original v1 | Prompt otimizado v2 | Motivo |
| --- | --- | --- | --- |
| Papel | Assistente genérico | Product Manager com contexto e limites de atuação | Orientar a transformação do bug em requisitos. |
| Entrada | `bug_report` em System e User | Entrada somente na mensagem User | Separar instruções de dados e evitar repetição. |
| Formato | Pedido genérico de User Story | História, critérios, contexto e seções condicionais | Produzir respostas mais organizadas e verificáveis. |
| Exemplos | Ausentes | Três pares de entrada/saída | Demonstrar comportamentos esperados. |
| Profundidade | Sem orientação | Respostas proporcionais à complexidade | Evitar excesso nos casos simples e omissões nos técnicos. |
| Incertezas | Sem regras explícitas | Separação entre fatos, propostas e pontos a confirmar | Reduzir afirmações sem suporte no relato. |
| Casos excepcionais | Sem tratamento explícito | Regras para insuficiência, contradições e instruções no relato | Orientar respostas em situações problemáticas. |

**Não foi executada uma avaliação numérica de v1.** A comparação v1/v2 é qualitativa. As três avaliações abaixo são revisões de v2; os números ilustrativos do enunciado não são resultados deste projeto.

## Resultados Finais

### Comparação dos experimentos

| Métrica | Iteração 1 | Iteração 2 | Iteração 3 selecionada | Mínimo |
| --- | ---: | ---: | ---: | ---: |
| Helpfulness | 0,90 | 0,90 | **0,92** | 0,80 |
| Correctness | 0,90 | 0,90 | **0,92** | 0,80 |
| F1-Score | 0,88 | 0,88 | **0,89** | 0,80 |
| Clarity | 0,87 | 0,88 | **0,90** | 0,80 |
| Precision | 0,93 | 0,93 | **0,94** | 0,80 |
| **Média geral** | **0,8969** | **0,8989** | **0,9136** | **0,80** |
| Status do script | Aprovado | Aprovado | **Aprovado** | |

As cinco métricas estão exibidas com duas casas decimais, como no CLI. A média geral é calculada pelo script com os valores agregados antes dessa formatação, por isso não deve ser reconstruída a partir dos números arredondados da tabela.

**[Abrir dataset público com os três experimentos](https://smith.langchain.com/public/a8b0113b-56e7-4d9d-9849-0156f68fb3ac/d)**

![Comparação dos três experimentos, com 15 execuções cada e médias das cinco métricas](docs/evidencias/comparacao-iteracoes.png)

![Resultados dos 15 exemplos e médias da terceira iteração](docs/evidencias/avaliacao-final.png)

Identificação dos experimentos e seus logs:

| Iteração | Experimento | Registro CLI |
| --- | --- | --- |
| 1 | `vicente-cruz-bug_to_user_story_v2-39448e02` | [Log 1](docs/evidencias/avaliacao-iteration-01.txt) |
| 2 | `vicente-cruz-bug_to_user_story_v2-a02d4b05` | [Log 2](docs/evidencias/avaliacao-iteration-02.txt) |
| 3 | `vicente-cruz-bug_to_user_story_v2-d0395f7a` | [Log 3](docs/evidencias/avaliacao-iteration-03.txt) |

[Prompt selecionado, commit bda84afa](https://smith.langchain.com/prompts/bug_to_user_story_v2/bda84afa?organizationId=346b3f12-c922-4a0e-be23-db374b3ca87e).

### Como as métricas são calculadas

O código original usa LLMs como avaliadores. F1, Clarity e Precision são métricas base; Helpfulness e Correctness são derivadas:

```text
F1-Score = 2 × precisão × recall / (precisão + recall)
Helpfulness = (Clarity + Precision) / 2
Correctness = (F1-Score + Precision) / 2
```

No F1, precisão e recall são estimados pelo juiz a partir da resposta e da referência. A precisão interna desse cálculo não é necessariamente igual à métrica separada `precision`, que tem sua própria avaliação. Clarity considera organização, linguagem, ausência de ambiguidade e concisão; Precision considera alucinações, foco e correção factual.

Para cada exemplo, as cinco notas e os comentários são gravados como feedback no LangSmith. O script calcula a média de cada métrica nos resultados e aprova somente quando **cada uma das cinco médias é pelo menos 0,8**, além da média geral. Não basta uma média geral alta compensar uma métrica abaixo do limite.

### Evidências de três exemplos

As capturas registram entradas, saídas e feedbacks de três exemplos da terceira iteração. Os números das linhas identificam a tabela capturada; não são identificadores permanentes do dataset.

| Exemplo | Helpfulness | Correctness | F1-Score | Clarity | Precision |
| --- | ---: | ---: | ---: | ---: | ---: |
| Relatório de vendas — linha 4 | 0,875 | 0,835 | 0,80 | 0,88 | 0,87 |
| Adicionar ao carrinho — linha 5 | 0,875 | 0,9237 | 0,9474 | 0,85 | 0,90 |
| Sincronização offline — linha 7 | 0,925 | 0,9244 | 0,9189 | 0,92 | 0,93 |

**[Ver capturas organizadas por exemplo](docs/evidencias/README.md).** As evidências incluem a árvore de chamadas dos três exemplos, com `Target`, `RunnableSequence`, `ChatPromptTemplate` e `ChatOpenAI`, o modelo `gpt-4.1-mini-2025-04-14`, duração e as cinco notas. As capturas complementares detalham entradas, saídas e justificativas dos avaliadores. O tracing registra mensagens, respostas e chamadas, não o pensamento interno do modelo.

### Limitações observadas

- **Aprovação agregada não significa aprovação de cada exemplo.** Na terceira iteração, o modal de exclusão obteve F1 de **0,7677** e Correctness de **0,7989**, embora as cinco médias do experimento tenham sido aprovadas. Arredondar 0,7989 para 0,80 não o torna maior ou igual ao limite.
- **As referências contêm detalhes ausentes das entradas.** Exemplos: prazo inferior a 30 segundos para o relatório; largura de 90% para o modal; lotes de 50 itens, checkpoints de 5 MB, limite de 500 MB e tecnologias específicas para sincronização. A ausência desses detalhes pode reduzir notas mesmo quando o modelo evita inventar requisitos. O dataset e os avaliadores foram preservados.
- **O avaliador também pode errar.** No caso do carrinho, houve penalização pela presença de uma User Story, embora esse seja o objetivo da aplicação. As justificativas foram lidas criticamente, sem alterar as notas.
- **O modelo não cumpriu integralmente todas as regras.** Na resposta final do relatório, ainda adotou menos de 120 segundos e “sem lentidão perceptível”, apesar da orientação para distinguir timeout de meta. Na sincronização, a resposta enfatizou o timestamp do cliente, enquanto o prompt orienta não depender apenas de relógios de dispositivos para ordem causal. As notas não substituem revisão técnica.
- **O resultado vale para este conjunto e estas execuções.** Foram usados os mesmos 15 exemplos para avaliar as iterações, sem conjunto separado de teste. Uma execução por revisão não demonstra significância estatística nem garante desempenho em novos bugs. Temperatura zero e versões fixas ajudam na comparação, mas não garantem respostas idênticas.

## Como Executar

### Pré-requisitos

- Git e Python. O enunciado pede Python 3.10+; para reproduzir o ambiente de dependências desta entrega, utilize Python 3.11 ou superior em versão estável.
- Conta no LangSmith, API key, acesso ao workspace e handle público configurado para publicar prompts.
- API key da OpenAI com acesso aos modelos e faturamento disponível para as chamadas.

As execuções registradas pelo autor usaram Linux, Python **3.11.0rc1**, `langsmith==0.13.0` e `pytest==9.1.1`. A versão de Python usada era uma prévia de lançamento. Outras dependências utilizadas incluem `langchain-core==1.2.16`, `langchain-openai==1.1.10`, `langchain-google-genai==4.2.1`, `PyYAML==6.0.3` e `python-dotenv==1.2.1`.

O `requirements.txt` registra o ambiente via `pip freeze` e inclui pacotes além dos usados diretamente neste desafio. `python -m pip check` foi executado sem conflitos reportados no ambiente do autor.

### 1. Clonar e preparar o ambiente

```bash
git clone https://github.com/vicente-cruz/mba-ia-pull-evaluation-prompt.git
cd mba-ia-pull-evaluation-prompt
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
python -m pip check
```

No Windows PowerShell, a ativação é `venv\Scripts\Activate.ps1`. Se já houver um ambiente virtual configurado, use-o em vez de criar outro.

### 2. Configurar o arquivo .env

Para uma instalação nova:

```bash
cp .env.example .env
```

Preencha localmente as chaves e o seu próprio handle:

```dotenv
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=sua_chave_langsmith
LANGSMITH_PROJECT=mba-ia-pull-evaluation-prompt
USERNAME_LANGSMITH_HUB=seu_handle_publico

LLM_PROVIDER=openai
OPENAI_API_KEY=sua_chave_openai
LLM_MODEL=gpt-4.1-mini-2025-04-14
EVAL_MODEL=gpt-4.1-2025-04-14
```

Nesta entrega, o handle é `vicente-cruz`. Para publicar em outra conta, substitua-o pelo handle dessa conta, sem URL ou nome de prompt. O enunciado orienta criar o handle ao tornar um prompt próprio público pela primeira vez, em **Prompts → Make Public**. Ele não é a API key nem necessariamente o usuário do GitHub.

Não versione `.env` nem chaves reais. Preserve apenas os nomes e exemplos de variáveis em `.env.example`.

### 3. Fazer pull do prompt inicial

```bash
python src/pull_prompts.py
```

O resultado é salvo em `prompts/bug_to_user_story_v1.yml`, preservando a variável `bug_report`. A autorização de pull público é explícita para o prompt semente do desafio. No ambiente inicial, `langsmith==0.7.7` não expunha esse parâmetro; a atualização para `0.13.0` resolveu a incompatibilidade. O cliente é instanciado como `client = Client()`, sem `with Client()`.

### 4. Inspecionar o prompt otimizado e executar os testes

O arquivo `prompts/bug_to_user_story_v2.yml` já contém a revisão final. Para novas iterações, edite esse arquivo e atualize o campo `revision`.

```bash
python -m pytest tests/test_prompts.py -v
```

Resultado registrado: **7 passed**. Os testes não fazem chamadas a LLMs. Eles verificam System Prompt, persona, formato, exemplos Few-shot, ausência de marcadores inacabados, duas técnicas nos metadados e preservação de `bug_report` na mensagem User. Esses testes validam a estrutura; a qualidade das respostas é medida na etapa de avaliação.

### 5. Publicar o prompt

```bash
python src/push_prompts.py
```

O script publica `{USERNAME_LANGSMITH_HUB}/bug_to_user_story_v2` como público, com descrição, tags e metadados das técnicas e da revisão. Ao final, imprime o link do commit no Hub.

### 6. Executar a avaliação

```bash
python src/evaluate.py
```

O avaliador cria ou reutiliza o dataset `<LANGSMITH_PROJECT>-eval`, carrega o prompt **do Hub**, gera as respostas e registra um novo experimento. Portanto, publique novamente depois de cada alteração no YAML: editar somente o arquivo local não altera o prompt avaliado.

Uma avaliação completa dos 15 exemplos normalmente envolve 15 chamadas de geração e 45 chamadas aos três juízes, sem contar novas tentativas. Helpfulness e Correctness são calculadas a partir das notas base, sem chamadas adicionais. Essas chamadas consomem a API; o custo total não foi auditado nesta entrega.

Os modelos usados foram escolhidos após consulta à documentação oficial: [GPT-4.1 mini](https://developers.openai.com/api/docs/models/gpt-4.1-mini) para geração e [GPT-4.1](https://developers.openai.com/api/docs/models/gpt-4.1) para avaliação. Os nomes com data fixam as versões utilizadas. A escolha considerou custo da geração, capacidade do avaliador e compatibilidade com o código fornecido. Verifique a disponibilidade dos modelos na sua conta ao reproduzir o experimento.

### 7. Consultar e compartilhar evidências

O endereço impresso pelo avaliador é do workspace. Para consultar esta entrega sem depender desse acesso, use o [dataset público já compartilhado](https://smith.langchain.com/public/a8b0113b-56e7-4d9d-9849-0156f68fb3ac/d). Não é necessário compartilhá-lo novamente.

Para compartilhar uma nova execução em seu próprio dataset, execute uma vez e guarde a URL retornada:

```bash
python - <<'PY'
import os
from dotenv import load_dotenv
from langsmith import Client

load_dotenv(".env")
dataset_name = f"{os.environ['LANGSMITH_PROJECT']}-eval"
print(Client().share_dataset(dataset_name=dataset_name)["url"])
PY
```

O comando torna o dataset compartilhado por link. Conforme o enunciado, repetir o compartilhamento pode mudar o endereço; preserve o link usado na documentação.
