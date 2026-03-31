# DSPy.rb

> Build LLM apps like you build software — type-safe, modular, testable Ruby framework for programmatic prompts.

## When to Use

- Implementing LLM-powered features in a Ruby/Rails application
- Creating type-safe signatures and modules for AI tasks
- Configuring language model providers in Ruby
- Building agent systems with tools and toolsets
- Optimizing prompts with real data (MIPROv2, GEPA)
- Testing LLM-powered functionality without fragile prompt strings

## Inputs

- Description of the LLM task to implement (classification, extraction, generation, etc.)
- Existing code to extend or refactor
- Provider preference (OpenAI, Anthropic, Gemini, multi-provider via RubyLLM)

## Methodology

### Core Concepts

#### 1. Signatures — Type-Safe Interfaces

Define inputs/outputs with Sorbet types. The signature communicates structure to the LLM via JSON Schema:

```ruby
class EmailClassifier < DSPy::Signature
  description "Classify customer support emails by category and priority"

  class Priority < T::Enum
    enums do
      Low = new('low')
      Medium = new('medium')
      High = new('high')
      Urgent = new('urgent')
    end
  end

  input do
    const :email_content, String
    const :sender, String
  end

  output do
    const :category, String
    const :priority, Priority  # Type-safe enum
    const :confidence, Float
  end
end
```

**Keep description concise** — state the goal, not field details. Field details go in `description:` kwargs on individual fields.

**Schema vs. description decision:**
- Use `T::Struct`/`T::Enum` for: multi-field outputs with specific types, enums the LLM must pick from, nested structures, arrays of typed objects, outputs consumed by code
- Use string descriptions for: simple single-field String outputs, natural language generation, constraint guidance (e.g., `"YYYY-MM-DD format"`)
- Rule of thumb: if you'd write a `case` on the output → `T::Enum`; if you'd call `.each` → `T::Array[SomeStruct]`

#### 2. Modules — Composable Workflows

- **Predict** — Basic LLM calls with signatures
- **ChainOfThought** — Step-by-step reasoning
- **ReAct** — Tool-using agents
- **CodeAct** — Dynamic code generation agents (install `dspy-code_act` gem)

#### 3. Tools & Toolsets

Type-safe tools for agents with Sorbet support:

```ruby
class CalculatorTool < DSPy::Tools::Base
  tool_name 'calculator'
  tool_description 'Performs arithmetic operations'

  class Operation < T::Enum
    enums do
      Add = new('add')
      Subtract = new('subtract')
      Multiply = new('multiply')
      Divide = new('divide')
    end
  end

  sig { params(operation: Operation, num1: Float, num2: Float).returns(T.any(Float, String)) }
  def call(operation:, num1:, num2:)
    case operation
    when Operation::Add then num1 + num2
    when Operation::Divide
      return "Error: Division by zero" if num2 == 0
      num1 / num2
    end
  end
end
```

Multi-tool toolset:
```ruby
class DataToolset < DSPy::Tools::Toolset
  toolset_name "data_processing"
  tool :convert, description: "Convert data between formats"
  tool :validate, description: "Validate data structure"

  def convert(data:, from:, to:) = "Converted from #{from.serialize} to #{to.serialize}"
  def validate(data:, format:) = { valid: true, format: format.serialize }
end
```

#### 4. Type System

- **Automatic `_type` field injection** — DSPy adds discriminator fields to structs
- **Union type support** — `T.any()` automatically disambiguated by `_type`
- **Reserved:** never define your own `_type` fields in structs
- **Recursive types** — supported via JSON Schema `$defs` (e.g., `T::Array[TreeNode]` self-reference)
- **Field descriptions** on `T::Struct` fields via `description:` kwarg — flow to JSON Schema

**When to use field descriptions:** complex semantics, enum-like strings, constrained values, ambiguous nested struct names. **Skip:** self-explanatory fields like `name`, `id`, `url`, boolean flags.

#### 5. Optimization

- **MIPROv2** — Advanced multi-prompt optimization with bootstrap sampling and Bayesian optimization
- **GEPA** — Genetic-Pareto Reflective Prompt Evolution with reflection-driven instruction rewrites, feedback maps, experiment tracking
- **Evaluation** — `DSPy::Evals` with built-in and custom metrics, batch processing

---

### Quick Start

```ruby
gem 'dspy'

DSPy.configure do |c|
  c.lm = DSPy::LM.new('openai/gpt-4o-mini', api_key: ENV['OPENAI_API_KEY'])
end

class SentimentAnalysis < DSPy::Signature
  description "Analyze sentiment of text"
  input  { const :text, String }
  output { const :sentiment, String; const :score, Float }
end

analyzer = DSPy::Predict.new(SentimentAnalysis)
result = analyzer.call(text: "This product is amazing!")
# result.sentiment => "positive", result.score => 0.92
```

---

### Provider Adapters

#### Per-Provider (direct SDK access)

```ruby
gem 'dspy'
gem 'dspy-openai'    # OpenAI, OpenRouter, Ollama
gem 'dspy-anthropic' # Claude
gem 'dspy-gemini'    # Gemini
```

#### Unified via RubyLLM (recommended for multi-provider)

```ruby
gem 'dspy'
gem 'dspy-ruby_llm'
gem 'ruby_llm'

DSPy.configure do |c|
  c.lm = DSPy::LM.new('ruby_llm/gemini-2.5-flash', structured_outputs: true)
  # c.lm = DSPy::LM.new('ruby_llm/claude-sonnet-4-20250514', structured_outputs: true)
  # c.lm = DSPy::LM.new('ruby_llm/gpt-4o-mini', structured_outputs: true)
end
```

**LM resolution hierarchy:** Instance-level LM → Fiber-local LM (`DSPy.with_lm`) → Global LM (`DSPy.configure`)

---

### Events System

Module-scoped subscriptions (preferred for agents):
```ruby
class MyAgent < DSPy::Module
  subscribe 'lm.tokens', :track_tokens, scope: :descendants
  def track_tokens(_event, attrs) = @total_tokens += attrs.fetch(:total_tokens, 0)
end
```

Global subscriptions (for observability):
```ruby
DSPy.events.subscribe('score.create') { |event, attrs| Langfuse.export_score(attrs) }
DSPy.events.subscribe('llm.*') { |name, attrs| puts "[#{name}] tokens=#{attrs[:total_tokens]}" }
```

Event names use dot-separated namespaces. Every event includes module metadata (`module_path`, `module_leaf`, `module_scope.ancestry_token`).

---

### Lifecycle Callbacks

Rails-style hooks on every `DSPy::Module`:
- **`before`** — setup (metrics, context loading)
- **`around`** — wraps forward, call `yield`
- **`after`** — cleanup or persistence

```ruby
class InstrumentedModule < DSPy::Module
  before :setup_metrics
  around :manage_context
  after :log_metrics

  def forward(question:) = @predictor.call(question: question)

  private
  def setup_metrics = @start_time = Time.now
  def manage_context
    load_context
    result = yield
    save_context
    result
  end
  def log_metrics = Rails.logger.info "Prediction in #{Time.now - @start_time}s"
end
```

Execution order: `before` → `around` (before yield) → `forward` → `around` (after yield) → `after`.
Callbacks inherited from parent classes, execute in registration order.

---

### Fiber-Local LM Context

```ruby
fast_model = DSPy::LM.new("openai/gpt-4o-mini", api_key: ENV['OPENAI_API_KEY'])
DSPy.with_lm(fast_model) do
  result = classifier.call(text: "test")  # Uses fast_model
end
# Back to global LM outside block
```

Fine-grained control over agent internals:
```ruby
agent.configure { |c| c.lm = default_model }
agent.configure_predictor('thought_generator') { |c| c.lm = powerful_model }
```

---

### Evaluation Framework

```ruby
metric = DSPy::Metrics.exact_match(field: :answer, case_sensitive: false)
evaluator = DSPy::Evals.new(predictor, metric: metric)
result = evaluator.evaluate(test_examples, display_table: true)
puts "Pass Rate: #{(result.pass_rate * 100).round(1)}%"
```

Built-in metrics: `exact_match`, `contains`, `numeric_difference`, `composite_and`.
Custom metrics return `true`/`false` or a `DSPy::Prediction` with `score:` and `feedback:`.

---

### GEPA Optimization

```ruby
gem 'dspy-gepa'

teleprompter = DSPy::Teleprompt::GEPA.new(
  metric: metric,
  reflection_lm: DSPy::ReflectionLM.new('openai/gpt-4o-mini', api_key: ENV['OPENAI_API_KEY']),
  feedback_map: feedback_map,
  config: { max_metric_calls: 600, minibatch_size: 6 }
)

result = teleprompter.compile(program, trainset: train, valset: val)
optimized_program = result.optimized_program
```

Metric must return `DSPy::Prediction.new(score:, feedback:)` so reflection model can reason about failures.

---

### Schema Formats

| Format | Mode | Notes |
|--------|------|-------|
| JSON Schema | default | Works with `structured_outputs: true` |
| BAML | Enhanced Prompting (`structured_outputs: false`) | 84% token reduction; requires `sorbet-baml` gem |
| TOON | Enhanced Prompting only | Table-oriented for both schemas and data |

---

### Storage System

```ruby
storage = DSPy::Storage::ProgramStorage.new(storage_path: "./dspy_storage")
storage.save_program(result.optimized_program, result, metadata: { optimizer: 'MIPROv2' })
```

Supports checkpoint management, optimization history tracking, import/export between environments.

---

### Rails Integration

#### Directory Structure

```
app/
  entities/          # T::Struct types shared across signatures
  signatures/        # DSPy::Signature definitions
  tools/             # DSPy::Tools::Base implementations
    concerns/        # Shared tool behaviors (error handling, etc.)
  modules/           # DSPy::Module orchestrators
  services/          # Plain Ruby services composing DSPy modules
config/
  initializers/
    dspy.rb          # DSPy + provider configuration
    feature_flags.rb # Model selection per role
spec/
  signatures/        # Schema validation tests
  tools/             # Tool unit tests
  modules/           # Integration tests with VCR
  vcr_cassettes/     # Recorded HTTP interactions
```

#### Initializer

```ruby
# config/initializers/dspy.rb
Rails.application.config.after_initialize do
  next if Rails.env.test? && ENV["DSPY_ENABLE_IN_TEST"].blank?

  RubyLLM.configure do |config|
    config.gemini_api_key = ENV["GEMINI_API_KEY"] if ENV["GEMINI_API_KEY"].present?
    config.anthropic_api_key = ENV["ANTHROPIC_API_KEY"] if ENV["ANTHROPIC_API_KEY"].present?
    config.openai_api_key = ENV["OPENAI_API_KEY"] if ENV["OPENAI_API_KEY"].present?
  end

  model = ENV.fetch("DSPY_MODEL", "ruby_llm/gemini-2.5-flash")
  DSPy.configure do |config|
    config.lm = DSPy::LM.new(model, structured_outputs: true)
    config.logger = Rails.logger
  end

  if ENV["LANGFUSE_PUBLIC_KEY"].present? && ENV["LANGFUSE_SECRET_KEY"].present?
    DSPy::Observability.configure!
  end
end
```

#### Feature-Flagged Model Selection

```ruby
module FeatureFlags
  SELECTOR_MODEL = ENV.fetch("DSPY_SELECTOR_MODEL", "ruby_llm/gemini-2.5-flash-lite")
  SYNTHESIZER_MODEL = ENV.fetch("DSPY_SYNTHESIZER_MODEL", "ruby_llm/gemini-2.5-flash")
end

class ClassifyTool < DSPy::Tools::Base
  def call(query:)
    predictor = DSPy::Predict.new(ClassifyQuery)
    predictor.configure { |c| c.lm = DSPy::LM.new(FeatureFlags::SELECTOR_MODEL, structured_outputs: true) }
    predictor.call(query: query)
  end
end
```

---

### Schema-Driven Signatures

Define reusable entities in `app/entities/` and reference across signatures:

```ruby
class ScoredItem < T::Struct
  const :id, String
  const :score, Float, description: "Relevance score 0.0-1.0"
  const :verdict, String, description: "relevant, maybe, or irrelevant"
  const :reason, String, default: ""
end

class RankResults < DSPy::Signature
  description "Score and rank search results by relevance"
  input  { const :query, String; const :items, T::Array[T::Hash[String, T.untyped]] }
  output { const :scored_items, T::Array[ScoredItem] }
end
```

Use `default: []` over `T::Nilable` arrays for OpenAI structured outputs compatibility.

---

### Tool Patterns

#### Tools That Wrap Predictions

```ruby
class RerankTool < DSPy::Tools::Base
  MAX_ITEMS = 200
  MIN_ITEMS_FOR_LLM = 5

  def call(query:, items: [])
    return { scored_items: items, reranked: false } if items.size < MIN_ITEMS_FOR_LLM

    capped_items = items.first(MAX_ITEMS)
    predictor = DSPy::Predict.new(RerankSignature)
    predictor.configure { |c| c.lm = DSPy::LM.new(FeatureFlags::SYNTHESIZER_MODEL, structured_outputs: true) }

    result = predictor.call(query: query, items: capped_items)
    { scored_items: result.scored_items, reranked: true }
  rescue => e
    Rails.logger.warn "[RerankTool] LLM rerank failed: #{e.message}"
    { error: "Rerank failed: #{e.message}", scored_items: items, reranked: false }
  end
end
```

Key patterns: short-circuit LLM for trivial cases, cap input size to prevent token overflow, per-tool model selection, graceful error handling with fallback data.

#### Error Handling Concern

```ruby
module ErrorHandling
  extend ActiveSupport::Concern
  private
    def safe_predict(signature_class, **inputs)
      predictor = DSPy::Predict.new(signature_class)
      yield predictor if block_given?
      predictor.call(**inputs)
    rescue Faraday::Error, Net::HTTPError => e
      Rails.logger.error "[#{self.class.name}] API error: #{e.message}"
      nil
    rescue JSON::ParserError => e
      Rails.logger.error "[#{self.class.name}] Invalid LLM output: #{e.message}"
      nil
    end
end
```

---

### Observability

Tracing with spans:
```ruby
result = DSPy::Context.with_span(
  operation: "tool_selector.select",
  "dspy.module" => "ToolSelector"
) do
  @predictor.call(query: query, context: context)
end
```

Langfuse setup:
```ruby
gem 'dspy-o11y'
gem 'dspy-o11y-langfuse'
# env: LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, DSPY_TELEMETRY_BATCH_SIZE=5
```

Score reporting:
```ruby
DSPy.score(name: "relevance", value: 0.85, trace_id: current_trace_id)
```

---

### Testing

#### VCR Setup

```ruby
VCR.configure do |config|
  config.cassette_library_dir = "spec/vcr_cassettes"
  config.hook_into :webmock
  config.configure_rspec_metadata!
  config.filter_sensitive_data('<GEMINI_API_KEY>') { ENV['GEMINI_API_KEY'] }
end
```

#### Signature Schema Tests (no LLM required)

```ruby
RSpec.describe ClassifyResearchQuery do
  it "has required input fields" do
    schema = described_class.input_json_schema
    expect(schema[:required]).to include("query")
  end
  it "has typed output fields" do
    schema = described_class.output_json_schema
    expect(schema[:properties]).to have_key(:search_strategy)
  end
end
```

#### Tool Tests

```ruby
RSpec.describe RerankTool do
  it "skips LLM for small result sets" do
    expect(DSPy::Predict).not_to receive(:new)
    result = described_class.new.call(query: "test", items: [{ id: "1" }])
    expect(result[:reranked]).to be false
  end

  it "calls LLM for large result sets", :vcr do
    items = 10.times.map { |i| { id: i.to_s, title: "Item #{i}" } }
    result = described_class.new.call(query: "relevant items", items: items)
    expect(result[:reranked]).to be true
  end
end
```

---

### 9 Coding Guidelines

1. **Schema over prose** — `T::Struct` and `T::Enum`, not string descriptions, for structured outputs
2. **Entities in `app/entities/`** — extract shared types so signatures stay thin
3. **Per-tool model selection** — `predictor.configure { |c| c.lm = ... }` per task
4. **Short-circuit LLM calls** — skip for trivial cases (small data, cached results)
5. **Cap input sizes** — limit array sizes before sending to LLM
6. **Test schemas without LLM** — validate `input_json_schema`/`output_json_schema` in unit tests
7. **VCR for integration tests** — record real HTTP interactions, never mock LLM responses by hand
8. **Trace with spans** — wrap tool calls in `DSPy::Context.with_span` for observability
9. **Graceful degradation** — always rescue LLM errors and return fallback data

---

### Typed Context Pattern

Replace opaque string context blobs with `T::Struct` inputs:

```ruby
class NavigationContext < T::Struct
  const :workflow_hint, T.nilable(String),
        description: "Current workflow phase guidance"
  const :action_log, T::Array[String], default: [],
        description: "Compact one-line-per-action history of research steps taken"
  const :iterations_remaining, Integer,
        description: "Budget remaining. Each tool call costs 1 iteration."
end
```

Benefits: type safety at compile time, per-field LLM descriptions, easy to test as value objects.

## Quality Gates

- Every signature has a `description` (concise goal statement)
- Structured outputs use `T::Struct`/`T::Enum` not opaque strings
- Tools cap input size and rescue LLM errors
- Schema tests pass without LLM calls
- VCR cassettes recorded for integration tests

## Outputs

- DSPy signatures, modules, tools, and toolsets
- Rails initializer and directory structure
- Test files with schema validation and VCR tests
- Optimized programs via MIPROv2 or GEPA

## Feeds Into

- `ce:work` (implementation execution)
- `ce:review` (code review of LLM components)

## Harness Notes

Current version: **0.34.3**

Key URLs:
- Homepage: https://oss.vicente.services/dspy.rb/
- GitHub: https://github.com/vicentereig/dspy.rb
- Docs: https://oss.vicente.services/dspy.rb/getting-started/
