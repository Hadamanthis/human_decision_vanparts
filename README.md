# Sistema de Suporte ao Cliente com Aprovação Humana

Agente de suporte ao cliente com fluxo determinístico e aprovação humana para ações sensíveis, desenvolvido com LangGraph, LangChain e FastAPI.

## O Problema

Agentes de IA tradicionais baseados em loop podem tomar decisões críticas sem validação humana — como aprovar reembolsos indevidos ou executar ações sensíveis automaticamente. Esse projeto resolve esse problema com um fluxo controlado onde ações de alto risco obrigatoriamente passam por aprovação humana antes de serem executadas.

## Arquitetura

O sistema segue um fluxo determinístico (DAG) implementado com LangGraph:

```
entrada → classificação → resolução → avaliação de risco → [low] → resposta final
                                                         → [high] → aprovação humana → resposta final
```

Cada etapa é um node isolado com responsabilidade única:

- **Classifier** — classifica a intenção do usuário: `reembolso`, `duvida`, `elogio` ou `desconhecido`
- **Resolver** — consulta a knowledge base via RAG e extrai informações estruturadas do produto
- **Risk Assessment** — avalia o risco da operação com base no valor do produto
- **Human Approval** — pausa o grafo e aguarda decisão humana para operações de alto risco
- **Final Response** — monta a resposta final ao cliente

## Stack

| Componente | Tecnologia |
|---|---|
| Framework de Agente | LangGraph |
| LLM | Groq (llama-3.1-8b-instant) |
| Orquestração LLM | LangChain |
| Knowledge Base | ChromaDB + Embeddings |
| API | FastAPI |
| Servidor | Uvicorn |

## Estrutura do Projeto

```
suporte-cliente-agent/
├── data/
│   └── knowledge_base/
│       ├── politicas.txt
│       ├── produtos.txt
│       └── servicos.txt
├── src/
│   ├── agents/
│   │   ├── classifier.py
│   │   ├── final_response.py
│   │   ├── human_approval.py
│   │   ├── resolver.py
│   │   └── risk_assessment.py
│   ├── api/
│   │   └── route.py
│   ├── services/
│   │   ├── knowledge_base.py
│   │   └── llm_client.py
│   ├── graph.py
│   ├── main.py
│   └── state.py
├── .env
├── .gitignore
├── pyproject.toml
└── requirements.txt
```

## Como Rodar

**1. Clone o repositório e crie o ambiente virtual:**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

**2. Instale as dependências:**
```bash
pip install -r requirements.txt
pip install -e .
```

**3. Configure o `.env`:**
```
GROQ_API_KEY=sua_chave_aqui
```

**4. Suba o servidor:**
```bash
python src/main.py
```

**5. Acesse a documentação interativa:**
```
http://localhost:8000/docs
```

## Endpoints

### `POST /message`
Recebe a mensagem do cliente e inicia o fluxo.

```json
{
  "thread_id": "cliente-001",
  "user_message": "Quero reembolso do radiador que comprei."
}
```

Resposta:
```json
{
  "thread_id": "cliente-001",
  "final_message": null,
  "awaiting_approval": true
}
```

### `POST /approve/{thread_id}`
Submete a decisão humana para operações pausadas.

```json
{
  "approved": true
}
```

### `GET /status/{thread_id}`
Retorna o estado atual da conversa.

## Conceitos Aplicados

- **DAG determinístico** com LangGraph — controle total do fluxo sem loops imprevisíveis
- **Human-in-the-loop** — pausa e retomada do grafo via checkpointer
- **RAG** — recuperação de contexto segmentado por domínio na knowledge base
- **Structured Output** — extração de dados estruturados do LLM via Pydantic
- **Engenharia defensiva** — validação de saídas do modelo e fallbacks em cada etapa

## Dívidas Técnicas

- [ ] Extrair system prompts para `src/prompts/`
- [ ] Migrar intenções de string literal para `Enum`
- [ ] Migrar `app.state` para `Depends()` no FastAPI
- [ ] Criar modelos de resposta Pydantic para os endpoints
- [ ] Avaliar `product` e `price` como objeto `Item`
- [ ] Migrar `classifier` para structured output
- [ ] Ajustar `n_results` no resolver para dúvidas
- [ ] Gerar `thread_id` automaticamente como UUID
- [ ] Migrar sintaxe de genéricos para Python 3.12+
