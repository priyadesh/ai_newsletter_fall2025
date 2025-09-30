# 🏗️ System Architecture

## Multi-Agent Workflow Diagram

```mermaid
graph TD
    A[User Request] --> B[FastAPI Server]
    B --> C{Cache Check}
    C -->|Hit| D[Return Cached Data]
    C -->|Miss| E[Reporter Agent]
    
    E --> F[SerpAPI]
    E --> G[Mock Data Fallback]
    F --> H[Raw Articles]
    G --> H
    
    H --> I[Editor Agent]
    I --> J[OpenAI GPT-4]
    J --> K[Summaries & Titles]
    
    K --> L[Senior Editor Agent]
    L --> M[OpenAI GPT-4]
    M --> N[Editorial Article]
    
    N --> O[Newsletter Data]
    O --> P[Cache Storage]
    O --> Q[React Frontend]
    
    Q --> R[Landing Page]
    Q --> S[Article Page]
    
    style E fill:#e1f5fe
    style I fill:#f3e5f5
    style L fill:#e8f5e8
    style Q fill:#fff3e0
```

## Component Architecture

```mermaid
graph LR
    subgraph "Frontend Layer"
        A[React App]
        B[Tailwind CSS]
        C[Vanilla JS]
    end
    
    subgraph "API Layer"
        D[FastAPI Server]
        E[Jinja2 Templates]
        F[Static Files]
    end
    
    subgraph "Service Layer"
        G[Newsletter Service]
        H[News Service]
        I[AI Service]
        J[Cache Service]
    end
    
    subgraph "Data Layer"
        K[Pydantic Models]
        L[TTLCache]
        M[Environment Config]
    end
    
    subgraph "External APIs"
        N[OpenAI API]
        O[SerpAPI]
    end
    
    A --> D
    B --> A
    C --> A
    D --> E
    D --> F
    D --> G
    G --> H
    G --> I
    G --> J
    H --> O
    I --> N
    J --> L
    G --> K
    D --> M
    
    style A fill:#61dafb
    style D fill:#009688
    style G fill:#ff9800
    style K fill:#9c27b0
```

## Data Flow Diagram

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant A as API
    participant C as Cache
    participant R as Reporter Agent
    participant E as Editor Agent
    participant S as Senior Editor Agent
    participant O as OpenAI
    participant N as SerpAPI
    
    U->>F: Request Newsletter
    F->>A: GET /api/v1/newsletter
    A->>C: Check Cache
    C-->>A: Cache Miss
    
    A->>R: Fetch Articles
    R->>N: API Request
    N-->>R: Raw Articles
    R-->>A: Validated Articles
    
    A->>E: Process Articles
    E->>O: Generate Summaries
    O-->>E: AI Summaries
    E-->>A: Processed Summaries
    
    A->>S: Create Editorial
    S->>O: Generate Editorial
    O-->>S: Editorial Content
    S-->>A: Complete Newsletter
    
    A->>C: Store in Cache
    A-->>F: Newsletter Data
    F-->>U: Display Newsletter
```

## Deployment Architecture

```mermaid
graph TB
    subgraph "Development Environment"
        A[Local Machine]
        B[Python 3.12]
        C[uv Package Manager]
        D[FastAPI Server]
        E[React Frontend]
    end
    
    subgraph "External Services"
        F[OpenAI API]
        G[SerpAPI]
    end
    
    subgraph "Configuration"
        H[Environment Variables]
        I[.env File]
        J[pyproject.toml]
    end
    
    A --> B
    B --> C
    C --> D
    D --> E
    D --> F
    D --> G
    D --> H
    H --> I
    C --> J
    
    style A fill:#4caf50
    style F fill:#ff5722
    style G fill:#2196f3
```

## API Endpoint Structure

```mermaid
graph TD
    A[FastAPI App] --> B[Main Routes]
    A --> C[API Routes]
    A --> D[Static Files]
    A --> E[Templates]
    
    B --> F[GET /]
    B --> G[GET /article/{id}]
    B --> H[Error Handlers]
    
    C --> I[GET /api/v1/newsletter]
    C --> J[GET /api/v1/newsletter/{id}]
    C --> K[GET /api/v1/health]
    C --> L[GET /api/v1/cache/status]
    C --> M[DELETE /api/v1/cache]
    
    D --> N[CSS Files]
    D --> O[JS Files]
    D --> P[Images]
    
    E --> Q[index.html]
    E --> R[article.html]
    E --> S[404.html]
    E --> T[500.html]
    
    style A fill:#009688
    style C fill:#ff9800
    style E fill:#9c27b0
```

