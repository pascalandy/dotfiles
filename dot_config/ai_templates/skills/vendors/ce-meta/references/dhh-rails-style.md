# DHH Rails Style

> Apply 37signals/DHH Rails conventions to Ruby and Rails code — REST purity, fat models, thin controllers, Hotwire, and "clarity over cleverness."

## When to Use

- Writing Ruby or Rails code of any kind (models, controllers, views, jobs, mailers, tests)
- Refactoring existing Rails code toward 37signals patterns
- Reviewing code for DHH style compliance
- Choosing between gem dependencies or vanilla Rails solutions
- Questions about 37signals philosophy, Basecamp, HEY, or Campfire architecture

## Inputs

- Description of what to build or code to review
- Optionally: which domain (controllers, models, frontend, architecture, testing, gems)

## Methodology

### Step 1: Identify Domain

Route the request to the relevant pattern area(s):

| Topic | Reference area |
|-------|----------------|
| Controllers, REST mapping, Turbo responses, API | Controllers |
| Models, concerns, state records, callbacks, scopes | Models |
| Views, Turbo, Stimulus, CSS | Frontend |
| Routing, auth, jobs, Current attributes, caching | Architecture |
| Minitest, fixtures, integration tests | Testing |
| Gems, dependencies | Gems |
| Full code review | All areas |

### Step 2: Apply Core Philosophy

**"The best code is the code you don't write."**

**Vanilla Rails is plenty:**
- Rich domain models over service objects
- CRUD controllers over custom actions
- Concerns for horizontal code sharing
- Records as state instead of boolean columns
- Database-backed everything (no Redis)
- Build solutions before reaching for gems

**Deliberately avoid:**
- devise → custom ~150-line auth instead
- pundit/cancancan → simple role checks on models
- sidekiq → Solid Queue (database-backed)
- redis → database for everything
- view_component → partials work fine
- GraphQL → REST with Turbo is sufficient
- factory_bot → fixtures are simpler
- rspec → Minitest ships with Rails
- Tailwind → native CSS with layers

**Development philosophy:**
- Ship → Validate → Refine: prototype-quality to production to learn
- Fix root causes, not symptoms
- Write-time operations over read-time computations
- Database constraints over ActiveRecord validations

---

### Controllers

#### Everything Maps to CRUD

Custom actions become new resources. Create noun resources instead of verbs on existing resources:

```ruby
# Instead of:
POST /cards/:id/close
DELETE /cards/:id/close
POST /cards/:id/archive

# Do this:
POST /cards/:id/closure      # create closure
DELETE /cards/:id/closure    # destroy closure
POST /cards/:id/archival     # create archival
```

Real examples from 37signals:
```ruby
resources :cards do
  resource :closure       # closing/reopening
  resource :goldness      # marking important
  resource :not_now       # postponing
  resources :assignments  # managing assignees
end
```

#### Controller Concerns

Common patterns: `CardScoped`, `BoardScoped`, `CurrentRequest`, `CurrentTimezone`, `FilterScoped`, `TurboFlash`, `ViewTransitions`, `BlockSearchEngineIndexing`, `RequestForgeryProtection`.

```ruby
module CardScoped
  extend ActiveSupport::Concern

  included do
    before_action :set_card
  end

  private
    def set_card
      @card = Card.find(params[:card_id])
      @board = @card.board
    end

    def render_card_replacement
      render turbo_stream: turbo_stream.replace(@card)
    end
end
```

#### Authorization

Controllers check permissions via `before_action`; models define what permissions mean:

```ruby
module Authorization
  extend ActiveSupport::Concern
  private
    def ensure_can_administer
      head :forbidden unless Current.user.admin?
    end
end

class Board < ApplicationRecord
  def editable_by?(user)
    user.admin? || user == creator
  end
end
```

#### Security

Sec-Fetch-Site CSRF protection:
```ruby
def verify_request_origin
  return if request.get? || request.head?
  return if %w[same-origin same-site].include?(request.headers["Sec-Fetch-Site"]&.downcase)
  verify_authenticity_token
end
```

Rate limiting (Rails 8+):
```ruby
class MagicLinksController < ApplicationController
  rate_limit to: 10, within: 15.minutes, only: :create
end
```

#### Turbo Stream Responses

```ruby
class Cards::ClosuresController < ApplicationController
  include CardScoped
  def create
    @card.close
    render_card_replacement
  end
  def destroy
    @card.reopen
    render_card_replacement
  end
end
```

For complex updates: `render turbo_stream: turbo_stream.morph(@card)`

#### API Design

Same controllers, different format:
```ruby
def create
  @card = Card.create!(card_params)
  respond_to do |format|
    format.html { redirect_to @card }
    format.json { head :created, location: @card }
  end
end
```
Status codes: Create → 201 + Location; Update/Delete → 204 No Content. Bearer token auth.

#### HTTP Caching

```ruby
def show
  @card = Card.find(params[:id])
  fresh_when etag: [@card, Current.user.timezone]
end
```
Include timezone in ETag — times render server-side in user's timezone.
Global ETag: `etag { "v1" }` in ApplicationController. Use `touch: true` for cache invalidation.

---

### Models

#### Concerns for Horizontal Behavior

A Card model typically includes 14+ concerns. Name them as adjectives: `Closeable`, `Publishable`, `Watchable`.

```ruby
class Card < ApplicationRecord
  include Assignable
  include Broadcastable
  include Closeable
  include Golden
  include Watchable
  # ... etc.
end
```

Each concern is self-contained (associations + scopes + methods). Size: 50–150 lines. Create only for genuine reuse, not organization.

#### State as Records, Not Booleans

```ruby
# Instead of: closed: boolean, is_golden: boolean

class Card::Closure < ApplicationRecord
  belongs_to :card
  belongs_to :creator, class_name: "User"
end

module Closeable
  extend ActiveSupport::Concern
  included do
    has_one :closure, dependent: :destroy
  end
  def closed? = closure.present?
  def close(creator: Current.user) = create_closure!(creator: creator)
  def reopen = closure&.destroy
end

# Querying:
Card.joins(:closure)         # closed cards
Card.where.missing(:closure) # open cards
```

Benefits: automatic timestamps, tracks who changed state, easy filtering.

#### Callbacks — Used Sparingly

Only 38 callback occurrences across 30 files in Fizzy.

Use for: `after_commit` for async work, `before_save` for derived data, `after_create_commit` for side effects.
Avoid: complex callback chains, business logic in callbacks, synchronous external calls.

#### Scope Naming

```ruby
scope :chronologically,          -> { order(created_at: :asc) }
scope :reverse_chronologically,  -> { order(created_at: :desc) }
scope :alphabetically,           -> { order(title: :asc) }
scope :latest,                   -> { reverse_chronologically.limit(10) }
scope :preloaded,                -> { includes(:creator, :assignees, :tags) }
scope :indexed_by,               ->(column) { order(column => :asc) }
scope :sorted_by,                ->(column, direction = :asc) { order(column => direction) }
```

#### Method Naming

Verbs (change state): `card.close`, `card.reopen`, `card.gild`, `board.publish`
Predicates (query state): `card.closed?`, `card.golden?`, `board.published?`
Avoid generic setters: use `card.close`, not `card.set_closed(true)`.

#### POROs — Plain Old Ruby Objects

Namespaced under parent models. Used for presentation logic and system commenters — NOT for service objects. Business logic stays in models.

```ruby
class Event::Description
  def initialize(event) = @event = event
  def to_s = # presentation logic
end
```

#### Validation Philosophy

Minimal validations on models. Use contextual validations on form/operation objects. Prefer database constraints over model validations for data integrity.

#### Let It Crash

Use bang methods that raise exceptions:
```ruby
@card = Card.create!(card_params)
@card.update!(title: new_title)
```
Let errors propagate. Rails handles `ActiveRecord::RecordInvalid` with 422.

#### Default Values

```ruby
belongs_to :creator, class_name: "User", default: -> { Current.user }
```

#### Rails 7.1+ Patterns

`normalizes`, `delegated_type`, `store_accessor` for clean model code.

#### Touch Chains & Transactions

```ruby
class Comment < ApplicationRecord
  belongs_to :card, touch: true
end

def close(creator: Current.user)
  transaction do
    create_closure!(creator: creator)
    record_event(:closed)
    notify_watchers_later
  end
end
```

---

### Frontend

#### Turbo Patterns

- `turbo_stream.replace(@card)` for partial updates
- `turbo_stream.morph(@card)` for complex updates
- `turbo_refreshes_with method: :morph, scroll: :preserve` globally in layout
- Fragment caching: `<%= render partial: "card", collection: @cards, cached: true %>`
- No ViewComponents — standard partials work fine

#### Turbo Morphing Best Practices

Listen for morph events to restore client state; use `data-turbo-permanent` for elements to skip morphing.

| Problem | Solution |
|---------|----------|
| Timers not updating | Clear/restart in morph event listener |
| Forms resetting | Wrap form sections in turbo frames |
| Pagination breaking | Use turbo frames with `refresh: :morph` |
| Flickering on replace | Switch to morph instead of replace |
| localStorage loss | Listen to `turbo:morph-element`, restore state |

#### Turbo Frames

Lazy loading with spinner, inline editing with edit/view toggle, `turbo_frame: "_parent"` to target parent, `turbo_stream_from` for real-time subscriptions.

#### Stimulus Controllers

52 controllers in Fizzy — 62% reusable, 38% domain-specific. Single responsibility, configuration via values/classes, events for communication, private methods with `#`, most under 50 lines.

Common examples:
- `copy-to-clipboard` (25 lines): uses Values API + setTimeout feedback
- `auto-click` (7 lines): calls `this.element.click()` on connect
- `toggle-class` (31 lines): Boolean value, `classList.toggle`
- `auto-submit` (28 lines): debounced `requestSubmit()` with `delayValue`
- `dialog` (45 lines): native HTML dialog with `showModal()`/`close()`
- `local-time` (40 lines): relative time display from datetime value

Best practices:
- Use Values API, not `getAttribute`
- Cleanup in `disconnect()` (clearTimeout, removeEventListener)
- `:self` action filter to prevent bubbling
- Dispatch events for loose coupling: `this.dispatch("selected", { detail: { id } })`

#### CSS Architecture

Vanilla CSS, no preprocessors:

```css
@layer reset, base, components, modules, utilities;
```

OKLCH color system:
```css
:root {
  --color-primary: oklch(60% 0.15 250);
  --color-success: oklch(65% 0.2 145);
}
```

Dark mode via CSS variables and `@media (prefers-color-scheme: dark)`. Native CSS nesting. ~60 minimal utilities. Modern features: `@starting-style`, `color-mix()`, `:has()`, logical properties, container queries.

#### User-Specific Content in Caches

Move personalization to client-side JavaScript. Use Stimulus to reveal owner-only elements post-cache-hit. Extract dynamic content to separate turbo frames.

#### Broadcasting

```ruby
after_create_commit :broadcast_created
private
  def broadcast_created
    broadcast_append_to [Current.account, board], :cards
  end
```
Always scope by tenant using `[Current.account, resource]`.

---

### Architecture

#### Routing

Everything maps to CRUD. Verb-to-noun conversion:
| Action | Resource |
|--------|----------|
| close a card | `card.closure` |
| watch a board | `board.watching` |
| mark as golden | `card.goldness` |
| archive a card | `card.archival` |

Shallow nesting: `resources :cards, shallow: true`. Singular resources for one-per-parent. Use `resolve` for URL generation.

#### Multi-Tenancy (Path-Based)

Middleware extracts tenant from URL prefix. Cookies scoped per tenant path. Background jobs serialize tenant via `Current.set`. Recurring jobs iterate all tenants. Controllers always scope through tenant: `Current.user.accessible_cards.find(params[:id])`.

#### Authentication

Custom passwordless magic link auth (~150 lines total). Session + MagicLink models. Bearer token for APIs.

Why not Devise: ~150 lines vs massive dependency, no password storage liability, full control.

#### Background Jobs

Jobs are shallow wrappers calling model methods:
```ruby
class NotifyWatchersJob < ApplicationJob
  def perform(card) = card.notify_watchers
end
```

Naming: `_later` suffix for async, `_now` for immediate. Solid Queue (database-backed, no Redis). `enqueue_after_transaction_commit = true`. Use `retry_on` for transient errors, `discard_on` for permanent. `ActiveJob::Continuable` for large batch processing.

#### Database Patterns

- UUIDs as primary keys (UUIDv7 time-sortable)
- State as records (not booleans)
- Hard deletes + event logs for auditing
- Counter caches for performance
- Account scoping on every table via `default_scope`

#### Current Attributes

```ruby
class Current < ActiveSupport::CurrentAttributes
  attribute :session, :user, :account, :request_id
  delegate :user, to: :session, allow_nil: true
  def account=(account)
    super
    Time.zone = account&.time_zone || "UTC"
  end
end
```

#### Caching

HTTP caching with ETags, fragment caching, Russian doll caching. Cache invalidation via `touch: true`. Solid Cache (database-backed, no Redis).

#### Event Tracking

Events are the single source of truth. `Eventable` concern with polymorphic `has_many :events`. Webhooks driven by events.

#### Email Patterns

Multi-tenant URL helpers via `default_url_options`, timezone-aware delivery, batch delivery via `perform_all_later`, one-click unsubscribe (RFC 8058).

#### Security Patterns

XSS: escape first, then mark safe. SSRF: resolve DNS once, pin IP, block private networks. CSP via initializer. ActionText sanitization.

#### Active Storage

Variant preprocessing with `preprocessed: true`. Direct upload expiry extended. Mirror service for migrations.

---

### Testing

#### Core Philosophy

"Minitest with fixtures — simple, fast, deterministic."

Why Minitest over RSpec: ships with Rails, simpler (plain Ruby assertions), faster boot, no DSL magic.

Why fixtures over factories: loaded once, no runtime creation overhead, explicit relationships, deterministic IDs.

#### Fixture Structure

```yaml
# test/fixtures/cards.yml
one:
  title: First Card
  board: main
  creator: alice

# ERB for time-sensitive data
recent_card:
  title: Recent Card
  created_at: <%= 1.hour.ago %>
```

#### Unit Tests

```ruby
class CardTest < ActiveSupport::TestCase
  setup do
    @card = cards(:one)
    @user = users(:david)
  end

  test "closing a card creates a closure" do
    assert_difference -> { Card::Closure.count } do
      @card.close(creator: @user)
    end
    assert @card.closed?
    assert_equal @user, @card.closure.creator
  end
end
```

#### Integration Tests

```ruby
class CardsControllerTest < ActionDispatch::IntegrationTest
  setup { sign_in users(:david) }

  test "closing a card" do
    post card_closure_path(cards(:one))
    assert_response :success
    assert cards(:one).reload.closed?
  end

  test "unauthorized user cannot close card" do
    sign_in users(:guest)
    post card_closure_path(cards(:one))
    assert_response :forbidden
  end
end
```

#### System Tests

Capybara-driven browser tests for full UX flows including drag-and-drop.

#### Advanced Patterns

- `travel_to` for time-dependent tests
- VCR for external API testing (record + replay)
- `assert_enqueued_with` for background job assertions
- `assert_emails` for mailer assertions
- `assert_turbo_stream_broadcasts` for ActionCable assertions

#### Five Testing Principles

1. **Test observable behavior**, not implementation
2. **Don't mock everything** — test the real thing
3. **Tests ship with features** — same commit, not TDD-first but together
4. **Security fixes always include regression tests**
5. **Integration tests validate complete workflows**

#### File Organization

```
test/
├── controllers/    # Integration tests
├── fixtures/       # YAML fixtures
├── helpers/
├── integration/    # API integration
├── jobs/
├── mailers/
├── models/         # Unit tests
├── system/         # Browser tests
└── test_helper.rb
```

Test helper: `fixtures :all`, `parallelize(workers: :number_of_processors)`, `driven_by :selenium, using: :headless_chrome`.

---

### Gems

#### What 37signals Uses

Core: turbo-rails, stimulus-rails, importmap-rails, propshaft
Solid suite: solid_queue, solid_cache, solid_cable
Auth: bcrypt
Own gems: geared_pagination, lexxy, mittens
Utilities: rqrcode, redcarpet + rouge, web-push
Ops: kamal, thruster, mission_control-jobs, autotuner

#### Decision Framework Before Adding a Gem

1. **Can vanilla Rails do this?** ActiveRecord, ActionMailer, ActiveJob cover most needs.
2. **Is the complexity worth it?** 150 lines of custom code vs. 10,000-line gem.
3. **Does it add infrastructure?** Redis? Consider database-backed alternatives.
4. **Is it from someone you trust?** Well-maintained, focused gems are fine; kitchen-sink gems are overkill.

> "Build solutions before reaching for gems."

---

### Quick Reference

**Naming:**
- Verbs: `card.close`, `card.gild`, `board.publish`
- Predicates: `card.closed?`, `card.golden?`
- Concerns: `Closeable`, `Publishable`, `Watchable`
- Controllers: `Cards::ClosuresController`
- Scopes: `chronologically`, `preloaded`, `active`

**Ruby syntax preferences:**
```ruby
# Symbol arrays with spaces inside brackets
before_action :set_message, only: %i[ show edit update destroy ]

# Private method indentation
  private
    def set_message
      @message = Message.find(params[:id])
    end

# Expression-less case
case
when params[:before].present?
  messages.page_before(params[:before])
else
  messages.last_page
end

# Bang methods for fail-fast
@message = Message.create!(params)
```

**Success criteria checklist:**
- [ ] Controllers map to CRUD verbs on resources
- [ ] Models use concerns for horizontal behavior
- [ ] State tracked via records, not booleans
- [ ] No unnecessary service objects or abstractions
- [ ] Database-backed solutions over external services
- [ ] Tests use Minitest with fixtures
- [ ] Turbo/Stimulus for interactivity (no heavy JS)
- [ ] Native CSS (layers, OKLCH, nesting)
- [ ] Authorization logic on User model
- [ ] Jobs are shallow wrappers calling model methods

## Quality Gates

- All new controllers map actions to CRUD on named resources
- No new boolean state columns without consideration of record-based alternative
- No new gem without passing the 4-question decision framework
- Tests committed in same PR as feature code

## Outputs

- Ruby/Rails code following 37signals conventions
- Refactored code with violation explanations
- Code review feedback organized by category

## Feeds Into

- `ce:review` (code review)
- `ce:work` (implementation)
- `andrew-kane-gem-writer` (if writing a gem)

## Harness Notes

The routing table (Step 1) references `references/` files in the original skill. In this distilled form, all reference content is included inline above. No external file reads required.

*Based on [The Unofficial 37signals/DHH Rails Style Guide](https://github.com/marckohlbrugge/unofficial-37signals-coding-style-guide) — LLM-generated, may contain inaccuracies, not affiliated with 37signals.*
