```mermaid
flowchart TD
    subgraph User Interface [Web UI (Flask/HTML/JS)]
        UI[Input Form & Response Display]
    end

    subgraph Backend [Flask Application Layer]
        APP[app.py<br/>- Routes:<br/>• index()<br/>- State:<br/>• Session<br/>• Request Data]
    end

    subgraph AI_Persona_Engine [AI Persona Engine (ai_persona.py)]
        AI[ai_persona.py<br/>- Public:<br/>• persona_response(journalist, pitch_text, conv_history)<br/>- Private:<br/>• extract_topics(pitch_text)]
    end

    subgraph NLP_Module [NLP & Summarization]
        SPACY[spaCy NER<br/>(en_core_web_sm)]
        SUMM[HuggingFace Transformers<br/>Summarizer]
    end

    subgraph Database [Persistence Layer (SQLite via SQLAlchemy)]
        DB[(SQLite DB)]
        MODELS[models.py<br/>- Journalist<br/>- Interaction<br/>- Public:<br/>• ORM queries<br/>- State:<br/>• Journalist Data<br/>• Interaction History]
    end

    subgraph Knowledge_Graph [Knowledge Graph (Personas)]
        KG[Knowledge Graph<br/>(Journalist Table)]
    end

    %% UI <-> Backend
    UI -->|POST pitch & journalist_id| APP
    APP -->|Render Template, Show Response| UI

    %% Backend <-> DB
    APP <--> |ORM CRUD<br/>(add/query interactions, journalists)| MODELS
    MODELS <--> |SQL| DB

    %% Knowledge Graph <-> DB
    KG <--> |Journalist ORM| MODELS

    %% Backend <-> AI Persona Engine
    APP -->|Call persona_response(...)| AI

    %% AI Persona Engine <-> NLP
    AI -->|extract_topics(pitch_text)| SPACY
    AI -->|summarizer(pitch_text)| SUMM

    %% Data Flows
    MODELS -.->|Journalist Object| AI
    MODELS -.->|Journalist List| APP

    %% State & Methods
    classDef module fill:#f9f,stroke:#333,stroke-width:1px;
    classDef data fill:#bbf,stroke:#333,stroke-width:1px;
    classDef nlp fill:#bfb,stroke:#333,stroke-width:1px;
    class MODELS,DB,KG data;
    class SPACY,SUMM nlp;

    %% Exposed & Private Methods
    click AI "https://github.com/indoria/your-repo/blob/main/ai_persona.py" "ai_persona.py"
    click MODELS "https://github.com/indoria/your-repo/blob/main/models.py" "models.py"

    %% Legend
    subgraph Legend [Legend]
        direction LR
        A1[Module/Component]:::module
        A2[Data/State]:::data
        A3[NLP/ML]:::nlp
    end
```
