# Andrew Kane Gem Writer

> Write Ruby gems following Andrew Kane's battle-tested patterns from 100+ gems with 374M+ downloads (Searchkick, PgHero, Chartkick, Strong Migrations, Lockbox, Ahoy, Blazer, Groupdate, Neighbor, Blind Index).

## When to Use

When creating new Ruby gems, refactoring existing gems, designing gem APIs, or when clean, minimal, production-ready Ruby library code is needed.

## Inputs

- Gem name and purpose
- Target audience (plain Ruby, Rails integration, or both)
- Whether the gem needs a web interface (Engine) or just model integration (Railtie)
- Database support requirements (single, multi-DB, specific adapters)

## Methodology

### Core Philosophy

**Simplicity over cleverness.** Zero or minimal dependencies. Explicit code over metaprogramming. Rails integration without Rails coupling. Every pattern serves production use cases.

---

### Entry Point Structure

Every gem follows this exact pattern in `lib/gemname.rb`:

```ruby
# 1. Dependencies (stdlib preferred)
require "forwardable"

# 2. Internal modules
require_relative "gemname/model"
require_relative "gemname/version"

# 3. Conditional Rails (CRITICAL - never require Rails directly)
require_relative "gemname/railtie" if defined?(Rails)

# 4. Module with config and errors
module GemName
  class Error < StandardError; end
  class InvalidConfigError < Error; end

  class << self
    attr_accessor :timeout, :logger
    attr_writer :client
  end

  self.timeout = 10  # Defaults set immediately
end
```

---

### Module Organization

**Simple gem layout:**
```
lib/
├── gemname.rb          # Entry point, config, errors
└── gemname/
    ├── helper.rb       # Core functionality
    ├── engine.rb       # Rails engine (if needed)
    └── version.rb      # VERSION constant only
```

**Complex gem layout (PgHero pattern):**
```
lib/
├── pghero.rb
└── pghero/
    ├── database.rb     # Main class
    ├── engine.rb       # Rails engine
    └── methods/        # Functional decomposition
        ├── basic.rb
        ├── connections.rb
        ├── indexes.rb
        ├── queries.rb
        └── replication.rb
```

**Method decomposition pattern** — Break large classes into includable modules by feature:

```ruby
# lib/pghero/database.rb
module PgHero
  class Database
    include Methods::Basic
    include Methods::Connections
    include Methods::Indexes
    include Methods::Queries
  end
end

# lib/pghero/methods/indexes.rb
module PgHero
  module Methods
    module Indexes
      def index_hit_rate
        # implementation
      end

      def unused_indexes
        # implementation
      end
    end
  end
end
```

**Version file — keep it minimal:**
```ruby
# lib/gemname/version.rb
module GemName
  VERSION = "2.0.0"
end
```

**Require order in entry point:**
```ruby
# 1. Standard library
require "forwardable"
require "json"

# 2. External dependencies (minimal)
require "active_support"

# 3. Internal files via require_relative
require_relative "searchkick/index"
require_relative "searchkick/model"
require_relative "searchkick/version"

# 4. Conditional Rails loading (LAST)
require_relative "searchkick/railtie" if defined?(Rails)
```

**Autoload vs require:** Kane uses explicit `require_relative`, not `autoload`.

**Comments style:** Minimal section headers only:
```ruby
# dependencies
require "active_support"

# adapters
require_relative "adapters/postgresql_adapter"
```

---

### Class Macro DSL Pattern

The signature Kane pattern — single method call configures everything:

```ruby
# Usage
class Product < ApplicationRecord
  searchkick word_start: [:name]
end

# Implementation
module GemName
  module Model
    def gemname(**options)
      unknown = options.keys - KNOWN_KEYWORDS
      raise ArgumentError, "unknown keywords: #{unknown.join(", ")}" if unknown.any?

      mod = Module.new
      mod.module_eval do
        define_method :some_method do
          # implementation
        end unless method_defined?(:some_method)
      end
      include mod

      class_eval do
        cattr_reader :gemname_options, instance_reader: false
        class_variable_set :@@gemname_options, options.dup
      end
    end
  end
end
```

---

### Rails Integration

**The golden rule: Always use `ActiveSupport.on_load` — never require Rails gems directly.**

```ruby
# WRONG - causes premature loading
require "active_record"
ActiveRecord::Base.include(MyGem::Model)

# CORRECT - lazy loading
ActiveSupport.on_load(:active_record) do
  extend GemName::Model
end

# Use prepend for behavior modification
ActiveSupport.on_load(:active_record) do
  ActiveRecord::Migration.prepend(GemName::Migration)
end
```

**Common `on_load` hooks:**
```ruby
# Models
ActiveSupport.on_load(:active_record) do
  extend GemName::Model        # Add class methods (searchkick, has_encrypted)
  include GemName::Callbacks   # Add instance methods
end

# Controllers
ActiveSupport.on_load(:action_controller) do
  include Ahoy::Controller
end

# Jobs
ActiveSupport.on_load(:active_job) do
  include GemName::JobExtensions
end

# Mailers
ActiveSupport.on_load(:action_mailer) do
  include GemName::MailerExtensions
end
```

**Railtie Pattern (non-mountable gems):**
```ruby
# lib/gemname/railtie.rb
module GemName
  class Railtie < Rails::Railtie
    initializer "gemname.configure" do
      ActiveSupport.on_load(:active_record) do
        extend GemName::Model
      end
    end

    # Optional: Add to controller runtime logging
    initializer "gemname.log_runtime" do
      require_relative "controller_runtime"
      ActiveSupport.on_load(:action_controller) do
        include GemName::ControllerRuntime
      end
    end

    # Optional: Rake tasks
    rake_tasks do
      load "tasks/gemname.rake"
    end
  end
end
```

**Engine Pattern (mountable gems with web interfaces — PgHero, Blazer, Ahoy):**
```ruby
# lib/pghero/engine.rb
module PgHero
  class Engine < ::Rails::Engine
    isolate_namespace PgHero

    initializer "pghero.assets", group: :all do |app|
      if app.config.respond_to?(:assets) && defined?(Sprockets)
        app.config.assets.precompile << "pghero/application.js"
        app.config.assets.precompile << "pghero/application.css"
      end
    end

    initializer "pghero.config" do
      PgHero.config = Rails.application.config_for(:pghero) rescue {}
    end
  end
end
```

**YAML Configuration with ERB:**
```ruby
def self.settings
  @settings ||= begin
    path = Rails.root.join("config", "blazer.yml")
    if path.exist?
      YAML.safe_load(ERB.new(File.read(path)).result, aliases: true)
    else
      {}
    end
  end
end
```

**Conditional feature detection:**
```ruby
# Check for specific Rails versions
if ActiveRecord.version >= Gem::Version.new("7.0")
  # Rails 7+ specific code
end

# Check for optional dependencies
def self.client
  @client ||= if defined?(OpenSearch::Client)
    OpenSearch::Client.new
  elsif defined?(Elasticsearch::Client)
    Elasticsearch::Client.new
  else
    raise Error, "Install elasticsearch or opensearch-ruby"
  end
end
```

**Generator Pattern:**
```ruby
# lib/generators/gemname/install_generator.rb
module GemName
  module Generators
    class InstallGenerator < Rails::Generators::Base
      source_root File.expand_path("templates", __dir__)

      def copy_initializer
        template "initializer.rb", "config/initializers/gemname.rb"
      end

      def copy_migration
        migration_template "migration.rb", "db/migrate/create_gemname_tables.rb"
      end
    end
  end
end
```

---

### Configuration Pattern

Use `class << self` with `attr_accessor`, not Configuration objects:

```ruby
module GemName
  class << self
    attr_accessor :timeout, :logger
    attr_writer :master_key
  end

  def self.master_key
    @master_key ||= ENV["GEMNAME_MASTER_KEY"]
  end

  self.timeout = 10
  self.logger = nil
end
```

---

### Error Handling

Simple hierarchy with informative messages:

```ruby
module GemName
  class Error < StandardError; end
  class ConfigError < Error; end
  class ValidationError < Error; end
end

# Validate early with ArgumentError
def initialize(key:)
  raise ArgumentError, "Key must be 32 bytes" unless key&.bytesize == 32
end
```

---

### Database Adapters

**Abstract base class pattern:**
```ruby
# lib/strong_migrations/adapters/abstract_adapter.rb
module StrongMigrations
  module Adapters
    class AbstractAdapter
      def initialize(checker)
        @checker = checker
      end

      def min_version
        nil
      end

      def set_statement_timeout(timeout)
        # no-op by default
      end

      def check_lock_timeout
        # no-op by default
      end

      private

      def connection
        @checker.send(:connection)
      end

      def quote(value)
        connection.quote(value)
      end
    end
  end
end
```

**Adapter detection pattern — use regex matching on adapter name:**
```ruby
def adapter
  @adapter ||= case connection.adapter_name
    when /postg/i
      Adapters::PostgreSQLAdapter.new(self)
    when /mysql|trilogy/i
      if connection.try(:mariadb?)
        Adapters::MariaDBAdapter.new(self)
      else
        Adapters::MySQLAdapter.new(self)
      end
    when /sqlite/i
      Adapters::SQLiteAdapter.new(self)
    else
      Adapters::AbstractAdapter.new(self)
    end
end
```

**Multi-database support (PgHero pattern):**
```ruby
module PgHero
  class << self
    attr_accessor :databases
  end
  self.databases = {}

  class Database
    attr_reader :id, :config

    def initialize(id, config)
      @id = id
      @config = config
    end

    def connection_model
      @connection_model ||= begin
        Class.new(ActiveRecord::Base) do
          self.abstract_class = true
        end.tap do |model|
          model.establish_connection(config)
        end
      end
    end

    def connection
      connection_model.connection
    end
  end
end
```

**SQL dialect handling:**
```ruby
def quote_column(column)
  case adapter_name
  when /postg/i
    %("#{column}")
  when /mysql/i
    "`#{column}`"
  else
    column
  end
end
```

---

### Testing (Minitest Only)

Kane exclusively uses Minitest — never RSpec.

```ruby
# test/test_helper.rb
require "bundler/setup"
Bundler.require(:default)
require "minitest/autorun"
require "minitest/pride"

# Load the gem
require "gemname"

# Test database setup (if needed)
ActiveRecord::Base.establish_connection(
  ENV["DATABASE_URL"] || { adapter: "postgresql", database: "gemname_test" }
)

# Base test class
class Minitest::Test
  def setup
    # Reset state before each test
  end
end
```

**Test file structure:**
```ruby
# test/model_test.rb
require_relative "test_helper"

class ModelTest < Minitest::Test
  def setup
    User.delete_all
  end

  def test_basic_functionality
    user = User.create!(email: "test@example.org")
    assert_equal "test@example.org", user.email
  end

  def test_with_invalid_input
    error = assert_raises(ArgumentError) do
      User.create!(email: nil)
    end
    assert_match /email/, error.message
  end
end
```

**Assertion patterns:**
```ruby
# Basic assertions
assert result
assert_equal expected, actual
assert_nil value
assert_empty array

# Exception testing
assert_raises(ArgumentError) { bad_code }

error = assert_raises(GemName::Error) { risky_operation }
assert_match /expected message/, error.message

# Refutations
refute condition
refute_equal unexpected, actual
refute_nil value
```

**Skipping database-specific tests:**
```ruby
def test_postgresql_specific
  skip "PostgreSQL only" unless postgresql?
  # test code
end

def postgresql?
  ActiveRecord::Base.connection.adapter_name =~ /postg/i
end
```

**Multi-version testing** — Test against multiple Rails/Ruby versions using gemfiles:

```
test/
├── test_helper.rb
└── gemfiles/
    ├── activerecord70.gemfile
    ├── activerecord71.gemfile
    └── activerecord72.gemfile
```

```ruby
# test/gemfiles/activerecord70.gemfile
source "https://rubygems.org"
gemspec path: "../../"
gem "activerecord", "~> 7.0.0"
gem "sqlite3"
```

Run with specific gemfile:
```bash
BUNDLE_GEMFILE=test/gemfiles/activerecord70.gemfile bundle install
BUNDLE_GEMFILE=test/gemfiles/activerecord70.gemfile bundle exec rake test
```

**Rakefile:**
```ruby
require "bundler/gem_tasks"
require "rake/testtask"

Rake::TestTask.new(:test) do |t|
  t.libs << "test"
  t.pattern = "test/**/*_test.rb"
end

task default: :test
```

**GitHub Actions CI:**
```yaml
name: build
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        include:
          - ruby: "3.2"
            gemfile: activerecord70
          - ruby: "3.3"
            gemfile: activerecord71
          - ruby: "3.3"
            gemfile: activerecord72
    env:
      BUNDLE_GEMFILE: test/gemfiles/${{ matrix.gemfile }}.gemfile
    steps:
      - uses: actions/checkout@v4
      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: ${{ matrix.ruby }}
          bundler-cache: true
      - run: bundle exec rake test
```

**Database-specific CI (with PostgreSQL service):**
```yaml
services:
  postgres:
    image: postgres:15
    env:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - 5432:5432
    options: >-
      --health-cmd pg_isready
      --health-interval 10s
      --health-timeout 5s
      --health-retries 5
env:
  DATABASE_URL: postgres://postgres:postgres@localhost/gemname_test
```

**Test database setup:**
```ruby
ActiveRecord::Base.establish_connection(
  ENV["DATABASE_URL"] || { adapter: "postgresql", database: "gemname_test" }
)

ActiveRecord::Schema.define do
  create_table :users, force: true do |t|
    t.string :email
    t.text :encrypted_data
    t.timestamps
  end
end

class User < ActiveRecord::Base
  gemname_feature :email
end
```

---

### Gemspec Pattern

Zero runtime dependencies when possible:

```ruby
Gem::Specification.new do |spec|
  spec.name = "gemname"
  spec.version = GemName::VERSION
  spec.required_ruby_version = ">= 3.1"
  spec.files = Dir["*.{md,txt}", "{lib}/**/*"]
  spec.require_path = "lib"
  # NO add_dependency lines - dev deps go in Gemfile
end
```

---

### Design Philosophy Summary (From Studying 100+ Gems)

1. **Zero dependencies when possible** — Each dep is a maintenance burden
2. **ActiveSupport.on_load always** — Never require Rails gems directly
3. **Class macro DSLs** — Single method configures everything
4. **Explicit over magic** — No method_missing, define methods directly
5. **Minitest only** — Simple, sufficient, no RSpec
6. **Multi-version testing** — Support broad Rails/Ruby versions
7. **Helpful errors** — Template-based messages with fix suggestions
8. **Abstract adapters** — Clean multi-database support
9. **Engine isolation** — `isolate_namespace` for mountable gems
10. **Minimal documentation** — Code is self-documenting, README is examples

---

### Anti-Patterns to Avoid

- `method_missing` (use `define_method` instead)
- Configuration objects (use class accessors)
- `@@class_variables` (use `class << self`)
- Requiring Rails gems directly
- Many runtime dependencies
- Committing `Gemfile.lock` in gems
- RSpec (use Minitest)
- Heavy DSLs (prefer explicit Ruby)
- `autoload` (use explicit `require_relative`)

---

### Reference Repos (Key Source Files to Study)

**Entry point patterns:**
- `github.com/ankane/searchkick` — `lib/searchkick.rb`
- `github.com/ankane/pghero` — `lib/pghero.rb`
- `github.com/ankane/strong_migrations` — `lib/strong_migrations.rb`
- `github.com/ankane/lockbox` — `lib/lockbox.rb`

**Class macro implementations:**
- `github.com/ankane/searchkick` — `lib/searchkick/model.rb`
- `github.com/ankane/lockbox` — `lib/lockbox/model.rb`

**Rails integration (Railtie/Engine):**
- `github.com/ankane/pghero` — `lib/pghero/engine.rb`
- `github.com/ankane/searchkick` — `lib/searchkick/railtie.rb`

**Database adapters:**
- `github.com/ankane/strong_migrations` — `lib/strong_migrations/adapters/`

**Essential reading:** `ankane.org/gem-patterns`

## Quality Gates

- Zero or minimal runtime dependencies
- All Rails integration via `ActiveSupport.on_load`
- Minitest test suite covering basic functionality and error cases
- Multi-version CI matrix (Ruby 3.2+, multiple ActiveRecord versions)
- `Gemfile.lock` not committed

## Outputs

- `lib/gemname.rb` entry point following the exact pattern
- `lib/gemname/` directory with organized modules
- `test/` suite with Minitest
- `gemname.gemspec` with zero runtime deps
- `Rakefile` with test task
- `.github/workflows/build.yml` CI matrix

## Feeds Into

- gem release workflows
- Rails app integration
- ce:plan for feature additions to existing gems
