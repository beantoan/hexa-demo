# Product CRUD API with Hexagonal Architecture

## Overview

A Flask-based REST API implementing CRUD operations for products using Hexagonal Architecture (Ports and Adapters
pattern).

## Hexagonal Architecture

### Definition

Hexagonal Architecture is a software design pattern that promotes:

- Separation of business logic from external concerns
- Dependency inversion through ports and adapters
- Framework independence
- Testability

### Core Components

1. **Domain Layer (Center)**
    - Business entities
    - Business rules
    - Domain interfaces (ports)

2. **Application Layer**
    - Use case implementations
    - Orchestration of domain objects
    - Application services

3. **Infrastructure Layer (Edge)**
    - External adapters (REST, Database)
    - Framework integrations
    - Technical implementations

### Comparison with MVC

#### MVC Architecture

```
Controller → Service → Model → Database
     ↓
    View
```

#### Hexagonal Architecture

```
                    → REST Adapter
Domain ← Application ← MySQL Adapter
                    ← CSV Adapter
```

#### Advantages over MVC

1. Better separation of concerns
    - Business logic is completely isolated
    - Framework can be changed without affecting core logic
    - Multiple persistence options without domain changes

2. Enhanced testability
    - Core logic can be tested without infrastructure
    - Easy mocking through interfaces
    - Clearer test organization

3. Flexibility
    - Multiple UI interfaces can be added easily
    - Database technology can be switched with minimal impact
    - Better support for different delivery mechanisms

#### Disadvantages vs MVC

1. More initial setup required
2. More interfaces and classes to maintain
3. Steeper learning curve for developers
4. Can be overkill for simple CRUD applications

## Project Structure

```
src/
├── domain/           # Core business logic
├── application/      # Use cases
└── infrastructure/   # External adapters
```

### Key Features

1. **Clear Boundaries**
    - Domain logic isolation
    - Interface-based communication
    - Dependency inversion

2. **Multiple Repositories**
    - MySQL implementation
    - CSV implementation
    - Easy to add new storage solutions

3. **Error Handling**
    - Domain-specific exceptions
    - Application-level errors
    - Infrastructure error mapping

4. **Testing Strategy**
    - Unit tests for domain logic
    - Integration tests for adapters
    - In-memory database for testing

## Getting Started

1. Clone repository
2. Install dependencies:
   ```bash
   pipenv install --dev
   ```
3. Run with Docker:
   ```bash
   docker-compose up --build
   ```

## Testing

Run tests:

```bash
pytest tests/ -v
```

You can run REST API tests using Jetbrains HTTP Client in `tests/rest/products.http`.

## API Endpoints

- POST /products - Create product
- GET /products - List all products
- GET /products/{id} - Get single product
- PUT /products/{id} - Update product
- DELETE /products/{id} - Delete product

## Dependencies

- Flask 3.1.0
- SQLAlchemy 2.0.25
- PyMySQL 1.1.1
- Python-dotenv 1.0.0
- Pytest 7.4.3
- Cryptography 42.0.4