# Agno Agent Demo Constitution

## Core Principles

### I. Agno Framework First
Every AI agent implementation must use the Agno framework as the primary foundation. Agents should leverage Agno's built-in capabilities for model management, conversation handling, and tool integration. No custom implementations of core AI functionality that duplicates Agno capabilities.

### II. Multi-Model Support (NON-NEGOTIABLE)
All agents must support both OpenAI and Azure OpenAI models through configurable environment variables. Model selection should be abstracted through a unified interface. No hard-coded model dependencies that prevent switching between providers.

### III. Test-First Development (NON-NEGOTIABLE)
TDD mandatory for all agent implementations: Contract tests written → User approved → Tests fail → Then implement. Red-Green-Refactor cycle strictly enforced. Every agent feature must have corresponding test coverage.

### IV. Modular Agent Architecture
Each agent type (basic, tools, reasoning, memory) must be independently deployable and testable. Clear separation of concerns between agent capabilities. Shared utilities should be library-based, not inheritance-based.

### V. Real-Time Performance Standards
Agent response time must be < 2 seconds for basic interactions, < 5 seconds for tool-enhanced responses. Memory management must support concurrent conversations. All I/O operations must be non-blocking where possible.

## Security Requirements

### API Key Management
All API keys and sensitive configuration must be managed through environment variables. No hardcoded secrets in source code. Support for both .env files and system environment variables.

### Model Safety
AI model interactions must include appropriate content filtering and safety measures. Error handling must prevent information leakage. All model responses should be validated for safety before presentation to users.

### Data Privacy
Agent memory and conversation history must be handled according to privacy best practices. Clear data retention policies. User consent for data storage where applicable.

## Quality Standards

### Code Quality Gates
- **Simplicity Gate**: Use ≤3 projects/dependencies where possible
- **Anti-Abstraction Gate**: Use Agno framework directly, avoid unnecessary abstractions
- **Integration-First Gate**: Contract tests before implementation
- **Performance Gate**: All response time requirements must be met
- **Security Gate**: All security requirements must be validated

### Documentation Requirements
Every agent must include comprehensive README with setup instructions, usage examples, and configuration options. API documentation for all public interfaces. Architecture decision records for significant design choices.

### Testing Standards
- Unit tests: >80% code coverage
- Integration tests: All external dependencies mocked or contracted
- End-to-end tests: Complete user workflows validated
- Performance tests: Response time requirements verified

## Development Workflow

### Implementation Process
1. Create specification using /speckit.specify
2. Generate technical plan using /speckit.plan
3. Write contract tests first
4. Implement to pass tests
5. Validate against quality gates
6. Document and deploy

### Review Requirements
All code changes must pass automated testing. Peer review required for architectural changes. Performance benchmarks must be maintained. Security review for any changes to authentication or API key handling.

## Governance

This constitution supersedes all other development practices. Amendments require documentation, team approval, and migration plan. All implementations must verify compliance with these principles.

Complexity must be justified against business value. When in doubt, choose simplicity and maintainability over clever optimizations.

**Version**: 1.0.0 | **Ratified**: 2025-10-15 | **Last Amended**: 2025-10-15