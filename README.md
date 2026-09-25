<p align="center">
  <img src="DOCS/assets/dealcraft-ai-icon.png" alt="DealCraft AI" width="420">
</p>

# DealCraft AI

> Transforme oportunidades comerciais em propostas estruturadas, consistentes e prontas para decisÃ£o.

**DealCraft AI** Ã© um sistema de apoio Ã  estruturaÃ§Ã£o de oportunidades comerciais B2B e Ã  geraÃ§Ã£o controlada de propostas comerciais.

O projeto transforma informaÃ§Ãµes de um briefing comercial em uma oportunidade estruturada, avalia sua completude, identifica lacunas, valida regras comerciais e somente permite a geraÃ§Ã£o da proposta quando os requisitos necessÃ¡rios forem atendidos.

A soluÃ§Ã£o foi projetada com um princÃ­pio central:

> **A IA pode apoiar a estruturaÃ§Ã£o da oportunidade, mas nÃ£o deve inventar informaÃ§Ãµes comerciais nem substituir a decisÃ£o humana.**

---

## VisÃ£o geral

Em processos comerciais B2B, propostas frequentemente sÃ£o construÃ­das a partir de informaÃ§Ãµes dispersas em reuniÃµes, anotaÃ§Ãµes, e-mails e briefings.

Isso pode gerar problemas como:

- informaÃ§Ãµes importantes ausentes;
- propostas criadas antes do entendimento adequado da oportunidade;
- preÃ§os fora das faixas comerciais;
- descontos inconsistentes;
- prazos incompatÃ­veis com o serviÃ§o;
- ausÃªncia de informaÃ§Ãµes sobre o processo decisÃ³rio;
- geraÃ§Ã£o de propostas baseada em suposiÃ§Ãµes;
- falta de padronizaÃ§Ã£o entre diferentes oportunidades.

O DealCraft AI foi desenvolvido para organizar esse processo.

Antes de gerar qualquer documento comercial, o sistema verifica se existem informaÃ§Ãµes suficientes e se a oportunidade respeita as regras definidas pela empresa.

---

## Objetivo

O objetivo do DealCraft AI Ã© transformar:

```text
Briefing comercial
        â†“
Oportunidade estruturada
        â†“
ValidaÃ§Ã£o
        â†“
Proposta comercial
```

em um processo controlado, rastreÃ¡vel e orientado por regras.

O sistema nÃ£o tenta prever se uma venda serÃ¡ fechada.

Ele verifica se existem **informaÃ§Ãµes suficientes para estruturar corretamente a oportunidade comercial**.

---

## Arquitetura do processo

```text
                 DEALCRAFT AI
                      â”‚
               â”Œâ”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”
               â”‚             â”‚
           BRIEFING      GUIA 5 ETAPAS
               â”‚             â”‚
               â””â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”˜
                      â†“
              DATA EXTRACTION
                      â†“
            OPPORTUNITY MODEL
                      â†“
          OPPORTUNITY READINESS
                      â†“
               GAP ANALYSIS
                      â†“
           SOLUTION MATCHING
                      â†“
        COMMERCIAL RULES ENGINE
                      â†“
             EXECUTIVE SUMMARY
                      â†“
              USER APPROVAL
                      â†“
           PROPOSAL GENERATION
                      â†“
                   .DOCX
```

A arquitetura separa claramente trÃªs responsabilidades:

**estruturaÃ§Ã£o da informaÃ§Ã£o â†’ validaÃ§Ã£o comercial â†’ geraÃ§Ã£o documental**

Essa separaÃ§Ã£o reduz o risco de gerar propostas baseadas em informaÃ§Ãµes incompletas ou inconsistentes.

---

# Opportunity Model

O DealCraft AI organiza uma oportunidade comercial em cinco grupos de informaÃ§Ã£o.

## A â€” Cliente

| Campo | InformaÃ§Ã£o |
|---|---|
| A1 | RazÃ£o social |
| A2 | Setor |
| A3 | Porte |
| A4 | LocalizaÃ§Ã£o |
| A5 | Contato principal |
| A6 | Cargo |
| A7 | E-mail |
| A8 | Telefone |

---

## B â€” Oportunidade

| Campo | InformaÃ§Ã£o |
|---|---|
| B1 | CenÃ¡rio atual |
| B2 | Principal problema / dor |
| B3 | Objetivo do projeto |
| B4 | Impacto |
| B5 | UrgÃªncia |
| B6 | Prazo desejado |
| B7 | OrÃ§amento |

---

## C â€” Processo decisÃ³rio

| Campo | InformaÃ§Ã£o |
|---|---|
| C1 | Decisor |
| C2 | Influenciadores |
| C3 | CritÃ©rios de decisÃ£o |
| C4 | Concorrentes |
| C5 | PrÃ³ximo passo comercial |
| C6 | Data do prÃ³ximo contato |

---

## D â€” SoluÃ§Ã£o

| Campo | InformaÃ§Ã£o |
|---|---|
| D1 | ServiÃ§o(s) recomendado(s) |
| D2 | Escopo |
| D3 | Prazo |
| D4 | Investimento por serviÃ§o |
| D5 | Desconto |
| D6 | Premissas |
| D7 | ExclusÃµes |

---

## E â€” Controle interno

| Campo | InformaÃ§Ã£o |
|---|---|
| E1 | NÃºmero da proposta |
| E2 | Consultor |
| E3 | E-mail do consultor |
| E4 | Data de emissÃ£o |
| E5 | Idioma |
| E6 | ObservaÃ§Ãµes |

---

# Opportunity Readiness

Um dos componentes centrais do DealCraft AI Ã© o **Opportunity Readiness**.

Ele Ã© um diagnÃ³stico determinÃ­stico de completude da oportunidade.

NÃ£o representa:

- probabilidade de fechamento;
- lead scoring;
- previsÃ£o de receita;
- previsÃ£o de conversÃ£o.

O objetivo Ã© responder:

> **Temos informaÃ§Ãµes suficientes para estruturar esta oportunidade de maneira responsÃ¡vel?**

SÃ£o avaliadas oito dimensÃµes:

| DimensÃ£o | CritÃ©rio |
|---|---|
| Cliente | Cliente identificado |
| Problema | Problema comercial definido |
| Objetivo | Objetivo do projeto definido |
| Impacto | Impacto conhecido |
| Decisor | Processo decisÃ³rio identificado |
| OrÃ§amento | OrÃ§amento informado |
| Prazo | Prazo conhecido |
| SoluÃ§Ã£o | SoluÃ§Ã£o definida |

Cada dimensÃ£o recebe:

```text
1 = informaÃ§Ã£o disponÃ­vel
0 = informaÃ§Ã£o ausente
```

O cÃ¡lculo Ã©:

```text
Opportunity Readiness =
dimensÃµes disponÃ­veis / 8 Ã— 100
```

ClassificaÃ§Ã£o:

| Resultado | ClassificaÃ§Ã£o |
|---|---|
| 0â€“49% | BAIXA COMPLETUDE |
| 50â€“74% | COMPLETUDE PARCIAL |
| 75â€“99% | BOA COMPLETUDE |
| 100% | COMPLETUDE TOTAL |

O indicador mede **completude da oportunidade**, e nÃ£o chance de venda.

---

# Gap Analysis

ApÃ³s estruturar a oportunidade, o sistema identifica informaÃ§Ãµes obrigatÃ³rias ausentes.

Exemplos:

```text
A7 â€” E-mail
B3 â€” Objetivo do projeto
B5 â€” UrgÃªncia
D1 â€” ServiÃ§o recomendado
D2 â€” Escopo
D3 â€” Prazo
D4 â€” Investimento
E1 â€” NÃºmero da proposta
E4 â€” Data de emissÃ£o
```

Quando existem lacunas obrigatÃ³rias, o fluxo Ã© interrompido.

O sistema nÃ£o deve completar esses campos por inferÃªncia.

---

# CatÃ¡logo de serviÃ§os

O DealCraft AI utiliza um catÃ¡logo estruturado de serviÃ§os.

| ServiÃ§o | Prazo | Faixa de investimento |
|---|---:|---:|
| DiagnÃ³stico de TransformaÃ§Ã£o Digital | 10â€“20 dias | R$ 12.000â€“25.000 |
| CRM & AutomaÃ§Ã£o Comercial | 30â€“60 dias | R$ 30.000â€“70.000 |
| Marketing & Growth Intelligence | 30â€“60 dias | R$ 25.000â€“60.000 |
| Data Analytics & BI | 30â€“75 dias | R$ 35.000â€“85.000 |
| AutomaÃ§Ã£o com IA | 30â€“90 dias | R$ 40.000â€“120.000 |
| Agentes de IA para NegÃ³cios | 30â€“75 dias | R$ 45.000â€“110.000 |
| IntegraÃ§Ã£o de Sistemas & Dados | 30â€“90 dias | R$ 40.000â€“100.000 |
| CapacitaÃ§Ã£o & AI Enablement | 5â€“20 dias | R$ 10.000â€“30.000 |

O catÃ¡logo possui uma representaÃ§Ã£o estruturada em JSON utilizada pelo mecanismo de validaÃ§Ã£o.

---

# Commercial Rules Engine

Antes da geraÃ§Ã£o da proposta, o DealCraft AI verifica as regras comerciais da operaÃ§Ã£o.

Entre as regras implementadas estÃ£o:

- moeda padrÃ£o em BRL;
- validade da proposta de 30 dias corridos;
- investimento dentro da faixa definida no catÃ¡logo;
- prazo dentro da faixa permitida para o serviÃ§o;
- desconto permitido apenas para contrataÃ§Ã£o de dois ou mais serviÃ§os;
- faixa de desconto permitida entre 5% e 15%;
- oportunidades a partir de R$ 200.000 exigem revisÃ£o comercial;
- serviÃ§os inexistentes no catÃ¡logo nÃ£o podem ser inventados;
- informaÃ§Ãµes ausentes nÃ£o podem ser preenchidas artificialmente.

---

# CondiÃ§Ãµes de pagamento

O padrÃ£o comercial utilizado pelo projeto Ã©:

```text
30% â€” contrataÃ§Ã£o
40% â€” marco intermediÃ¡rio
30% â€” entrega
```

O sistema calcula automaticamente os valores absolutos de cada parcela.

Exemplo para uma proposta de R$ 60.000:

```text
30% = R$ 18.000
40% = R$ 24.000
30% = R$ 18.000
```

---

# Estados da oportunidade

ApÃ³s as validaÃ§Ãµes, o DealCraft AI pode retornar os seguintes estados:

```text
APROVADO PARA RESUMO EXECUTIVO
REQUER INFORMAÃ‡Ã•ES
REQUER VALIDAÃ‡ÃƒO HUMANA
BLOQUEADO
```

Somente oportunidades elegÃ­veis seguem para a etapa de resumo executivo.

---

# Human-in-the-Loop

A geraÃ§Ã£o da proposta possui uma etapa explÃ­cita de aprovaÃ§Ã£o humana.

Mesmo depois de todas as validaÃ§Ãµes automÃ¡ticas, o documento nÃ£o Ã© criado imediatamente.

Primeiro, o DealCraft AI apresenta um **Resumo Executivo da Oportunidade**.

Depois, o usuÃ¡rio precisa confirmar explicitamente:

```text
APROVAR
```

Somente apÃ³s essa confirmaÃ§Ã£o o documento `.docx` Ã© gerado.

Esse mecanismo mantÃ©m a decisÃ£o comercial final sob responsabilidade humana.

---

# Guardrails contra alucinaÃ§Ã£o

O DealCraft AI foi projetado para evitar a criaÃ§Ã£o artificial de informaÃ§Ãµes comerciais.

O sistema nÃ£o deve inventar:

- clientes;
- orÃ§amento;
- impacto;
- concorrentes;
- decisores;
- necessidades;
- serviÃ§os;
- preÃ§os;
- descontos;
- prazos;
- resultados esperados.

Quando uma informaÃ§Ã£o nÃ£o existe, ela deve ser tratada como:

```text
nÃ£o informado
```

Se o campo for obrigatÃ³rio, o sistema solicita complementaÃ§Ã£o ou bloqueia o fluxo.

---

# GeraÃ§Ã£o da proposta

ApÃ³s a validaÃ§Ã£o e aprovaÃ§Ã£o humana, o DealCraft AI gera automaticamente uma proposta comercial profissional em formato:

```text
.docx
```

Estrutura do documento:

```text
CAPA

01 â€” Contexto e oportunidade

02 â€” SoluÃ§Ã£o proposta

03 â€” Escopo e entregÃ¡veis

04 â€” Cronograma

05 â€” Investimento

06 â€” PrÃ³ximos passos
```

O documento inclui:

- identidade visual;
- dados do cliente;
- contexto da oportunidade;
- soluÃ§Ã£o proposta;
- escopo;
- cronograma;
- investimento;
- condiÃ§Ãµes de pagamento;
- validade da proposta;
- prÃ³ximo passo comercial;
- responsÃ¡vel pela proposta;
- paginaÃ§Ã£o automÃ¡tica.

---

# Identidade visual

A empresa fictÃ­cia utilizada no projeto Ã©:

## NEXORA CONSULTING

**Data Â· AI Â· Growth Â· Automation**

Paleta principal:

| Elemento | Cor |
|---|---|
| Navy | `#14213D` |
| Blue | `#2563EB` |
| Cyan | `#06B6D4` |
| Graphite | `#1F2937` |
| Slate | `#64748B` |
| Cloud | `#F8FAFC` |
| Border | `#E2E8F0` |

Tipografia principal:

```text
Aptos
```

Fallback:

```text
Arial
Calibri
```

---

# Estrutura do projeto

```text
DealCraft-AI/
â”‚
â”œâ”€â”€ DOCS/
â”‚   â”œâ”€â”€ brand-book.json
â”‚   â”œâ”€â”€ business-rules.md
â”‚   â”œâ”€â”€ catalogo-servicos-dealcraft.md
â”‚   â”œâ”€â”€ catalogo-servicos.json
â”‚   â””â”€â”€ template-proposta.docx
â”‚
â”œâ”€â”€ examples/
â”‚   â”œâ”€â”€ briefing-completo.txt
â”‚   â””â”€â”€ briefing-incompleto.txt
â”‚
â”œâ”€â”€ outputs/
â”‚   â””â”€â”€ propostas geradas
â”‚
â”œâ”€â”€ skill/
â”‚   â””â”€â”€ SKILL.md
â”‚
â”œâ”€â”€ build_template.py
â”œâ”€â”€ dealcraft_validator.py
â”œâ”€â”€ dealcraft_summary.py
â”œâ”€â”€ dealcraft_proposal.py
â””â”€â”€ README.md
```

---

# Componentes

## `dealcraft_validator.py`

ResponsÃ¡vel por:

- extraÃ§Ã£o das informaÃ§Ãµes;
- construÃ§Ã£o do Opportunity Model;
- identificaÃ§Ã£o de campos ausentes;
- Opportunity Readiness;
- leitura do catÃ¡logo;
- validaÃ§Ã£o de preÃ§os;
- validaÃ§Ã£o de prazos;
- validaÃ§Ã£o de descontos;
- condiÃ§Ãµes de pagamento;
- regras comerciais;
- definiÃ§Ã£o do status da oportunidade.

---

## `dealcraft_summary.py`

ResponsÃ¡vel por:

- criaÃ§Ã£o do resumo executivo;
- apresentaÃ§Ã£o das informaÃ§Ãµes validadas;
- preparaÃ§Ã£o da oportunidade para decisÃ£o humana;
- solicitaÃ§Ã£o explÃ­cita de aprovaÃ§Ã£o.

---

## `dealcraft_proposal.py`

ResponsÃ¡vel por:

- executar a validaÃ§Ã£o;
- apresentar o resumo executivo;
- solicitar aprovaÃ§Ã£o;
- gerar a proposta;
- aplicar identidade visual;
- construir tabelas;
- controlar paginaÃ§Ã£o;
- gerar o arquivo `.docx`.

---

## `build_template.py`

ResponsÃ¡vel pela construÃ§Ã£o do template documental utilizado como referÃªncia do projeto.

---

# Requisitos

O projeto utiliza Python.

DependÃªncia principal:

```text
python-docx
```

InstalaÃ§Ã£o:

```bash
pip install python-docx
```

---

# Como executar

Clone o repositÃ³rio:

```bash
git clone https://github.com/SEU-USUARIO/DealCraft-AI.git
```

Entre no diretÃ³rio:

```bash
cd DealCraft-AI
```

Instale a dependÃªncia:

```bash
pip install python-docx
```

---

## Validar uma oportunidade

```bash
python dealcraft_validator.py examples/briefing-completo.txt
```

Para visualizar o modelo extraÃ­do:

```bash
python dealcraft_validator.py examples/briefing-completo.txt --debug
```

---

## Gerar resumo executivo

```bash
python dealcraft_summary.py examples/briefing-completo.txt
```

---

## Executar o fluxo completo

```bash
python dealcraft_proposal.py examples/briefing-completo.txt
```

O sistema:

```text
valida
   â†“
estrutura
   â†“
calcula readiness
   â†“
verifica regras
   â†“
gera resumo
   â†“
solicita aprovaÃ§Ã£o
   â†“
gera proposta
```

Quando solicitado, digite:

```text
APROVAR
```

---

# CenÃ¡rios de teste

O projeto possui dois briefings de referÃªncia.

## CenÃ¡rio positivo

```text
examples/briefing-completo.txt
```

Resultado esperado:

```text
Opportunity Readiness: 100%
Campos obrigatÃ³rios: 17/17
Status: APROVADO PARA RESUMO EXECUTIVO
```

ApÃ³s aprovaÃ§Ã£o humana:

```text
PROPOSTA GERADA COM SUCESSO
```

---

## CenÃ¡rio negativo

```text
examples/briefing-incompleto.txt
```

O sistema identifica campos obrigatÃ³rios ausentes e interrompe o processo.

Resultado esperado:

```text
REQUER INFORMAÃ‡Ã•ES
```

Nenhuma proposta deve ser gerada.

---

# Exemplo validado

Durante os testes do projeto foi utilizada uma oportunidade fictÃ­cia da empresa:

```text
TechNova DistribuiÃ§Ã£o Ltda.
```

ServiÃ§o:

```text
CRM & AutomaÃ§Ã£o Comercial
```

Investimento:

```text
R$ 60.000
```

Prazo:

```text
60 dias
```

Opportunity Readiness:

```text
8/8 dimensÃµes
100%
COMPLETUDE TOTAL
```

O fluxo completo foi validado:

```text
Briefing
   â†“
ExtraÃ§Ã£o
   â†“
Opportunity Model
   â†“
Opportunity Readiness
   â†“
Gap Analysis
   â†“
Commercial Rules Engine
   â†“
Executive Summary
   â†“
Human Approval
   â†“
DOCX
```

---

# PrincÃ­pios do projeto

O DealCraft AI foi construÃ­do com cinco princÃ­pios:

### 1. NÃ£o inventar dados comerciais

InformaÃ§Ãµes inexistentes permanecem inexistentes.

### 2. Validar antes de gerar

A proposta Ã© consequÃªncia da validaÃ§Ã£o, nÃ£o o inÃ­cio do processo.

### 3. Separar completude de previsÃ£o

Opportunity Readiness nÃ£o representa probabilidade de fechamento.

### 4. Aplicar regras determinÃ­sticas

PreÃ§o, prazo, desconto e condiÃ§Ãµes comerciais sÃ£o controlados por regras explÃ­citas.

### 5. Manter decisÃ£o humana

A proposta sÃ³ Ã© criada apÃ³s aprovaÃ§Ã£o explÃ­cita do usuÃ¡rio.

---

# Roadmap

PossÃ­veis evoluÃ§Ãµes futuras:

```text
Interface web com Streamlit
        â†“
PersistÃªncia das oportunidades
        â†“
Suporte avanÃ§ado a mÃºltiplos serviÃ§os
        â†“
HistÃ³rico de aprovaÃ§Ãµes
        â†“
Brand Book totalmente dinÃ¢mico
        â†“
Templates comerciais configurÃ¡veis
        â†“
IntegraÃ§Ã£o com CRM
        â†“
LLM para extraÃ§Ã£o semÃ¢ntica
        â†“
RAG sobre catÃ¡logo e regras comerciais
        â†“
API
        â†“
Analytics comercial
```

Essas funcionalidades nÃ£o fazem parte do nÃºcleo validado da versÃ£o atual.

---

# Tecnologias

- Python
- python-docx
- JSON
- Markdown
- Microsoft Word / DOCX
- Git
- GitHub

---

# Contexto de desenvolvimento

O DealCraft AI foi desenvolvido como projeto prÃ¡tico de aplicaÃ§Ã£o de conceitos de **Agentes de IA para NegÃ³cios**, combinando automaÃ§Ã£o, engenharia de regras, estruturaÃ§Ã£o de dados, validaÃ§Ã£o comercial e Human-in-the-Loop.

O projeto parte de um problema real de processos comerciais B2B: transformar informaÃ§Ãµes nÃ£o estruturadas de uma oportunidade em uma proposta comercial consistente sem permitir que automaÃ§Ã£o ou IA preencham lacunas com informaÃ§Ãµes nÃ£o verificadas.

---

# Autor

**Marcus Guedes**

Marketing Â· GestÃ£o Â· InteligÃªncia Artificial Â· Data Analytics Â· Projetos Â· TransformaÃ§Ã£o Digital

GitHub: `MCLG1661`

---

## Status do projeto

**DealCraft AI v1.0 â€” NÃºcleo tÃ©cnico concluÃ­do e validado.**

```text
Opportunity Model        âœ…
Opportunity Readiness    âœ…
Gap Analysis             âœ…
Service Catalog          âœ…
Commercial Rules Engine  âœ…
Executive Summary        âœ…
Human Approval           âœ…
DOCX Generation          âœ…
Positive E2E Test        âœ…
Negative E2E Test        âœ…
```

---

**DealCraft AI**

*Transforme oportunidades comerciais em propostas estruturadas, consistentes e prontas para decisÃ£o.*

