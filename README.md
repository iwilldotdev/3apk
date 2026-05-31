# 3APK — AI-Augmented Agile Planning Kit

Kit de planejamento ágil aumentado por IA para **micro times de desenvolvimento** (2–5 pessoas). Combina **skills portáteis** (prompt chains com aprovação humana), um **hub Notion** (backlog, DoR, planning, métricas) e **exportação manual** para Jira ou Trello.

Desenvolvido no contexto de um Projeto de Extensão (PEX) Descomplica, alinhado ao **ODS 9** (Indústria, inovação e infraestrutura). O piloto documenta a aplicação do kit em um **projeto de desenvolvimento de software** conduzido pela **RODRIGO HERPICH MULLER LTDA**.

---

## Para quem é este repositório

| Papel | O que você faz aqui |
|-------|---------------------|
| **Membro do time** | Roda skills no seu chat/IDE, cola resultados no Notion, executa o sprint no Jira/Trello |
| **Facilitador** | Monta o Notion, conduz baseline e workshops com o time, coleta métricas |
| **Reutilização** | Copia apenas as skills em `kit/skills/` e adapta o Notion ao seu fluxo |

---

## O que contém o kit

Tudo que você precisa para usar o 3APK está em [`kit/`](kit/):

| Área | Caminho | Conteúdo |
|------|---------|----------|
| **Skills** | [`kit/skills/`](kit/skills/) | 5 skills modulares (4 refinement + 1 planning) |
| **Notion** | [`kit/notion/`](kit/notion/) | Guia de setup + JSON Schemas |
| **Exportação** | [`kit/exports/`](kit/exports/) | CSV canônico + receitas Jira/Trello |
| **Fixtures** | [`kit/fixtures/`](kit/fixtures/) | Exemplos JSON/CSV de referência |

**Princípios:**

- **Human-in-the-loop** — nenhuma estimativa ou critério de aceite entra no sprint sem aprovação explícita do time.
- **LLM-agnóstico** — skills em Markdown; funcionam em Cursor, Claude, ChatGPT, Copilot Chat, etc.
- **Sem SaaS novo** — Notion + ferramentas atuais; export manual para Jira/Trello.

Índice detalhado: [`kit/README.md`](kit/README.md).

---

## Pré-requisitos

- Conta **Notion** (plano gratuito)
- Qualquer **chat com LLM** ou IDE com agente
- **Jira** ou **Trello** (opcional) — para levar o sprint plano à execução
- ~30 minutos para montar o Notion seguindo o guia

**Não precisa:** servidor, API, build ou assinatura de ferramenta específica.

---

## Início rápido

### 1. Montar o hub no Notion

Siga [`kit/notion/SPEC.md`](kit/notion/SPEC.md) e crie os quatro bancos:

1. **Backlog** — histórias, DoR, status  
2. **Sprints** — capacidade, datas  
3. **Planning Worksheet** — compromisso do sprint (view: só DoR aprovado)  
4. **Metrics** — KPIs por sprint  

Os campos devem seguir os schemas em [`kit/notion/schema/`](kit/notion/schema/).

### 2. Instalar as skills

Copie as pastas de `kit/skills/` para onde seu agente lê skills, **ou** anexe o `SKILL.md` no chat:

| Ordem | Skill | Arquivo |
|-------|-------|---------|
| 1 | Refinar pedido → user story | [`3apk-refine-story/SKILL.md`](kit/skills/3apk-refine-story/SKILL.md) |
| 2 | User story → critérios de aceite | [`3apk-refine-ac/SKILL.md`](kit/skills/3apk-refine-ac/SKILL.md) |
| 3 | AC → faixa de estimativa (hint) | [`3apk-refine-estimate/SKILL.md`](kit/skills/3apk-refine-estimate/SKILL.md) |
| 4 | Dependências e riscos | [`3apk-refine-risks/SKILL.md`](kit/skills/3apk-refine-risks/SKILL.md) |
| 5 | Planejamento de sprint | [`3apk-plan-sprint/SKILL.md`](kit/skills/3apk-plan-sprint/SKILL.md) |

### 3. Configurar exportação

- Colunas CSV: [`kit/exports/COLUMNS.md`](kit/exports/COLUMNS.md)  
- **Jira:** [`kit/exports/jira-recipe.md`](kit/exports/jira-recipe.md)  
- **Trello:** [`kit/exports/trello-recipe.md`](kit/exports/trello-recipe.md)  
- **Outras ferramentas:** [`kit/exports/generic-fallback.md`](kit/exports/generic-fallback.md)  

Referência: [`kit/fixtures/sample-worksheet-export.csv`](kit/fixtures/sample-worksheet-export.csv).

### 4. Validar o setup

Use os exemplos em [`kit/fixtures/`](kit/fixtures/) e, se disponível, rode:

```bash
python3 kit/fixtures/validate_fixtures.py
python3 kit/exports/test_export_recipes.py
```

---

## Uso no dia a dia

### Refinar um item (nova feature, bug, melhoria)

**Uma skill por vez**, com **aprovação humana** antes de avançar:

```
Pedido bruto
  → 3apk-refine-story    → aprovar user story
  → 3apk-refine-ac       → aprovar critérios de aceite
  → 3apk-refine-estimate → aprovar faixa de estimativa (hint)
  → 3apk-refine-risks    → aprovar deps/riscos + DoR
  → colar no Notion      → DoR_Pass ou DoR_Fail
```

- Uma pergunta por mensagem (múltipla escolha quando possível).  
- A IA **não** fecha estimativa final — o time ajusta no planning.  
- Itens com DoR reprovado **não entram** no sprint.

Exemplos: [`kit/fixtures/refine-story-example.md`](kit/fixtures/refine-story-example.md) e demais `refine-*-example.md`.

### Planejar um sprint

1. View **Sprint Candidates** no Notion (só `DoR_Pass`).  
2. Registrar sprint em **Sprints** com `capacity_hours`.  
3. Invocar **`3apk-plan-sprint`** com histórias + capacidade.  
4. Preencher `human_adjustment_log` para cada estimativa alterada.  
5. Aprovar o sprint draft (Sprint Lock).  
6. Exportar CSV e importar no Jira/Trello.

Exemplo: [`kit/fixtures/plan-sprint-example.md`](kit/fixtures/plan-sprint-example.md).

### Registrar métricas

Após cada sprint, uma linha em **Metrics**:

| KPI | Definição resumida |
|-----|-------------------|
| **EAR** | Soma(horas reais) / Soma(horas estimadas), ≥5 histórias |
| **DoR %** | Histórias com 4 gates / total planejadas |
| **Planning (min)** | Duração × participantes (refinement + planning) |
| **Reopens** | Histórias reabertas por lacuna de AC/escopo |

Schema completo: [`kit/notion/schema/metric-snapshot.json`](kit/notion/schema/metric-snapshot.json).

---

## Piloto sugerido (4–8 semanas)

| Fase | Semanas | Atividades |
|------|---------|------------|
| **Prep** | 0 | Montar Notion; distribuir skills |
| **Baseline** | 1 | 1 ciclo **sem** o kit; congelar KPIs |
| **Intervenção** | 2–5 | Skills + DoR + planning a cada 1–2 semanas |
| **Evidências** | 6–8 | Comparar antes/depois; consolidar resultados |

Relatório PEX de referência (acadêmico): [`docs/relatorio-pex/relatorio-pex-ads-iii-william-santos-goncalves.pdf`](docs/relatorio-pex/relatorio-pex-ads-iii-william-santos-goncalves.pdf).

---

## Estrutura do repositório

```
3APK/
├── kit/
│   ├── skills/       # 5 skills modulares
│   ├── notion/       # SPEC.md + JSON Schemas
│   ├── exports/      # COLUMNS.md + receitas Jira/Trello
│   └── fixtures/     # exemplos JSON/CSV
├── docs/
│   └── relatorio-pex/   # relatório PEX (PDF + HTML)
└── README.md
```

---

## Referências

- [Guia PEX Descomplica](https://pexguiadefinitivo.vercel.app/)
- ODS 9 — [Indústria, inovação e infraestrutura (ONU)](https://www.un.org/sustainabledevelopment/infrastructure-industrialization/)

---

## Licença e uso

Material de extensão universitária e kit aberto para adaptação em times pequenos. Ao reutilizar, mantenha o protocolo de aprovação humana em cada etapa do refinamento.
