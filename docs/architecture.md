# V-Astra Architecture

## Layers

### 1. Context Intelligence
Determines which context is relevant to the current task.

### 2. Compression Engine
Applies type-aware transformations to text, JSON, logs, terminal output, and code.

### 3. Memory
Caches reusable context and supports history summarization.

### 4. Safety
Prevents optimization when critical information may be lost.

### 5. Measurement
Tracks token counts, savings, and information retention.

### 6. Integrations
Keeps provider-specific behavior outside the core engine.

## Safety rule

Optimization is never considered successful solely because token count decreased.

A transformation must satisfy the configured retention threshold. Otherwise the engine returns the original content.
