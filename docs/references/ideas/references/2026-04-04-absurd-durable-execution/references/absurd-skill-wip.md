---
name: Absurd 0.3.0 Skill Draft
description: Technical reference and proposed SKILL.md for Absurd 0.3.0 -- SDK APIs, absurdctl, Habitat, patterns, with code examples
tags:
  - area/ea
  - kind/research
  - status/stable
date_updated: 2026-04-04
---

# Absurd Skill Draft Packet

Target release: `0.3.0`

This draft packet is based on the public docs site, the GitHub repository, the bundled upstream skill, and the `0.2.0...0.3.0` release diff.

## Source Audit

- Docs site: `https://earendil-works.github.io/absurd/`
- Repo: `https://github.com/earendil-works/absurd`
- Upstream bundled skill: `skills/absurd/SKILL.md`
- Latest release at time of writing: `0.3.0` published `2026-04-02`
- Release-specific additions verified in the compare view:
- `beginStep` / `completeStep` and Python equivalents for decomposed steps
- guarded cross-task waits so `awaitTaskResult` inside a task cannot target the same queue
- range-based `absurdctl migrate --dump-sql`
- bundled `absurdctl install-skill`
- cron pattern doc
- pi durable agent example

## Proposed `SKILL.md`

````md
---
name: absurd
description: Debug, operate, and build on Absurd 0.3.0 durable workflows. Use when a project uses Absurd, absurdctl, queues, tasks, runs, checkpoints, events, sleeps, retries, migrations, Habitat, or agent-facing workflow inspection.
license: Apache-2.0
release: 0.3.0
---

# Absurd

Use this skill when the project uses **Absurd**, the Postgres-native durable workflow engine, or when the user mentions **`absurdctl`**, queues, tasks, runs, retries, sleeping tasks, waiting for events, or Habitat.

## What Absurd is

Absurd is a durable execution system that pushes most of the workflow engine into Postgres.

- One SQL schema is the engine.
- Workers are pull-based.
- Tasks are durable workflows.
- Steps are persisted checkpoints.
- Events are cached wake-up signals.
- SDKs stay thin because retries, resumes, claims, waits, and checkpoint persistence live in SQL.

Absurd is a good fit when you want durable background work without running a separate orchestration cluster such as Temporal.

## Release scope for 0.3.0

This skill targets Absurd `0.3.0` and should assume these release-era capabilities exist:

- decomposed steps with `beginStep` / `completeStep` and `begin_step` / `complete_step`
- bundled skill installation through `absurdctl install-skill`
- range-based SQL generation through `absurdctl migrate --from ... --to ... --dump-sql`
- cross-queue child-task waits, with same-queue waits explicitly guarded against
- refreshed TypeScript and Python docs, cron pattern, and pi durable-agent pattern

## Tiny mental model

- A **queue** is a namespace of Absurd tables: `t_`, `r_`, `c_`, `e_`, `w_`.
- A **task** is the logical durable workflow.
- A **run** is one execution attempt of that task.
- A **step** is a checkpoint. Completed step results are persisted as JSON.
- A task can **sleep** or **await an event** and resume later.
- Events are cached. First emit wins.
- Code outside steps may run more than once across retries.

Important distinction:

- `task_id` = the whole workflow across attempts
- `run_id` = one specific attempt

## First: make sure `absurdctl` works

If `absurdctl` is not on `PATH` and you are inside an Absurd repo checkout, use:

```bash
export PATH="$PWD:$PATH"
```

## Connection precedence

Absurd tools and SDKs resolve database connections in this order:

```text
explicit argument or flag > ABSURD_DATABASE_URL > PGDATABASE > postgresql://localhost/absurd
```

For non-URI connections, `PGHOST`, `PGPORT`, `PGUSER`, and `PGPASSWORD` are also honored.

## Default operating workflow

Prefer **state inspection before source inspection**.

If the user explicitly asks to use **`absurdctl`** to inspect or fix a workflow, do that first instead of starting with source browsing.

When debugging a workflow:

```bash
absurdctl list-queues
absurdctl list-tasks --queue=default --limit=20
absurdctl list-tasks --queue=default --status=failed --limit=20
absurdctl list-tasks --queue=default --status=sleeping --limit=20
absurdctl dump-task --task-id=<task-id>
```

Notes:

- `list-tasks` defaults to 50 rows if `--limit` is omitted.
- Useful statuses are `pending`, `running`, `sleeping`, `completed`, `failed`, and `cancelled`.
- `dump-task` is the best first deep-inspection command once you know the task or run identifier.
- `dump-task` exposes task params, headers, retry settings, attempts, checkpoints, waits, and terminal failure or result data.

Only search application code after you know the task name, queue, state, and checkpoint history.

## How to reason about common states

### Failed task

1. Run `absurdctl dump-task --task-id=<task-id>`.
2. Read the failure payload and the last successful checkpoints.
3. Inspect the newest `run_id` if attempt-level detail matters.
4. Search application code only after that.
5. Decide whether to retry only after understanding the failure.

### Sleeping task

1. Run `absurdctl dump-task --task-id=<task-id>`.
2. Determine whether it is sleeping until a timestamp or waiting for an event name.
3. If the user wants it resumed and it is event-gated, emit that event.

### Running task

1. Run `absurdctl dump-task --task-id=<task-id>`.
2. Read existing checkpoints to see how far it got.
3. Only inspect worker logs or runtime code when the state suggests a stuck worker.

### About workers

Do not assume you need to start or modify a worker.

- If a task moves from `pending` to `sleeping`, `running`, or `completed`, a worker is already active.
- If tasks remain `pending`, investigate whether a worker for that queue is actually running.
- Only inspect Python or TypeScript runtime details when task state suggests a worker problem or the user explicitly asks for code changes.

## Feature catalog with examples

### 1. Schema install and upgrades

Fresh install:

```bash
export PGDATABASE="postgresql://user:pass@localhost:5432/mydb"
absurdctl init
absurdctl schema-version
absurdctl create-queue default
```

Pin to a release:

```bash
absurdctl init --ref 0.3.0
absurdctl schema-version
```

Upgrade in place:

```bash
absurdctl migrate
absurdctl migrate --to 0.3.0
absurdctl migrate --dry-run
```

Generate SQL for your own migration system:

```bash
absurdctl migrate --from 0.2.0 --to 0.3.0 --dump-sql \
  > db/migrations/202604020001_absurd_0.2.0_to_0.3.0.sql
```

### 2. Queue management

CLI:

```bash
absurdctl create-queue emails
absurdctl list-queues
absurdctl drop-queue emails --yes
```

TypeScript:

```typescript
import { Absurd } from "absurd-sdk";

const app = new Absurd({ queueName: "default" });

await app.createQueue("emails");
console.log(await app.listQueues());
await app.dropQueue("emails");
await app.close();
```

Python:

```python
from absurd_sdk import Absurd

app = Absurd(queue_name="default")
app.create_queue("emails")
print(app.list_queues())
app.drop_queue("emails")
app.close()
```

### 3. Creating a client

TypeScript:

```typescript
import * as pg from "pg";
import { Absurd } from "absurd-sdk";

const fromUrl = new Absurd({
  db: "postgresql://user:pass@localhost:5432/mydb",
  queueName: "default",
});

const pool = new pg.Pool({ connectionString: process.env.PGDATABASE });
const fromPool = new Absurd({ db: pool, queueName: "default" });

const minimal = new Absurd();

await fromUrl.close();
await fromPool.close();
await minimal.close();
```

Python sync and async:

```python
from absurd_sdk import Absurd, AsyncAbsurd
from psycopg import Connection

app = Absurd("postgresql://user:pass@localhost:5432/mydb", queue_name="default")

conn = Connection.connect("postgresql://user:pass@localhost:5432/mydb", autocommit=True)
app_from_conn = Absurd(conn, queue_name="default")

async_app = AsyncAbsurd("postgresql://user:pass@localhost:5432/mydb", queue_name="default")

app.close()
app_from_conn.close()
```

### 4. Registering tasks and checkpointed steps

TypeScript:

```typescript
import { Absurd } from "absurd-sdk";

const app = new Absurd({ queueName: "default" });

app.registerTask(
  {
    name: "send-email",
    defaultMaxAttempts: 5,
    defaultCancellation: { maxDuration: 3600, maxDelay: 600 },
  },
  async (params, ctx) => {
    const rendered = await ctx.step("render", async () => {
      return `<h1>${params.template}</h1>`;
    });

    const delivered = await ctx.step("send", async () => {
      return { accepted: [params.to], html: rendered };
    });

    return delivered;
  },
);

await app.startWorker();
```

Python:

```python
from absurd_sdk import Absurd

app = Absurd(queue_name="default")


@app.register_task(
    name="send-email",
    default_max_attempts=5,
    default_cancellation={"maxDuration": 3600, "maxDelay": 600},
)
def send_email(params, ctx):
    rendered = ctx.step("render", lambda: f"<h1>{params['template']}</h1>")
    delivered = ctx.step("send", lambda: {"accepted": [params["to"]], "html": rendered})
    return delivered


app.start_worker()
```

### 5. Decomposed steps in 0.3.0

Use decomposed steps when the checkpoint lifecycle needs to be split across two calls.

TypeScript:

```typescript
type AgentState = { messages: string[] };

const handle = await ctx.beginStep<AgentState>("agent-turn");

if (handle.done) {
  return handle.state;
}

const nextState = { messages: ["hello"] };
await ctx.completeStep(handle, nextState);
```

Python:

```python
handle = ctx.begin_step("agent-turn")

if handle.done:
    state = handle.state
else:
    state = ctx.complete_step(handle, {"messages": ["hello"]})
```

### 6. Python decorator-style steps

Python also supports `run_step`.

```python
@ctx.run_step("process-payment")
def payment():
    return {"charge_id": f"charge-{params['amount']}"}

print(payment)
```

### 7. Sleep primitives

TypeScript:

```typescript
await ctx.sleepFor("cooldown", 3600);
await ctx.sleepUntil("deadline", new Date("2026-12-31T00:00:00Z"));
```

Python:

```python
from datetime import datetime, timezone

ctx.sleep_for("cooldown", 3600)
ctx.sleep_until("deadline", datetime(2026, 12, 31, tzinfo=timezone.utc))
```

### 8. Awaiting events and emitting events

TypeScript:

```typescript
const shipment = await ctx.awaitEvent(`shipment.packed:${params.orderId}`, {
  stepName: "wait-for-shipment",
  timeout: 86400,
});

await ctx.emitEvent(`order.completed:${params.orderId}`, {
  orderId: params.orderId,
});

await app.emitEvent(`shipment.packed:${params.orderId}`, {
  trackingNumber: "TRACK-123",
});

await app.emitEvent("shipment.packed", { trackingNumber: "TRACK-123" }, "orders");
```

Python:

```python
shipment = ctx.await_event(
    f"shipment.packed:{params['order_id']}",
    step_name="wait-for-shipment",
    timeout=86400,
)

ctx.emit_event(f"order.completed:{params['order_id']}", {"order_id": params["order_id"]})

app.emit_event(f"shipment.packed:{params['order_id']}", {"tracking_number": "TRACK-123"})
app.emit_event("shipment.packed", {"tracking_number": "TRACK-123"}, queue_name="orders")
```

Notes:

- first emit wins for a given event name
- event payloads are immutable once recorded
- timeout expiration raises `TimeoutError`

### 9. Spawning tasks with retries, headers, cancellation, and idempotency

TypeScript:

```typescript
const spawned = await app.spawn(
  "send-email",
  { to: "user@example.com", template: "welcome" },
  {
    queue: "emails",
    maxAttempts: 10,
    retryStrategy: {
      kind: "exponential",
      baseSeconds: 2,
      factor: 2,
      maxSeconds: 300,
    },
    headers: { traceId: "trace-123", requestId: "req-456" },
    cancellation: { maxDuration: 7200, maxDelay: 600 },
    idempotencyKey: "welcome:user-42",
  },
);

console.log(spawned.taskID, spawned.runID, spawned.attempt, spawned.created);
```

Python:

```python
spawned = app.spawn(
    "send-email",
    {"to": "user@example.com", "template": "welcome"},
    queue="emails",
    max_attempts=10,
    retry_strategy={
        "kind": "exponential",
        "base_seconds": 2,
        "factor": 2,
        "max_seconds": 300,
    },
    headers={"trace_id": "trace-123", "request_id": "req-456"},
    cancellation={"maxDuration": 7200, "maxDelay": 600},
    idempotency_key="welcome:user-42",
)

print(spawned["task_id"], spawned["run_id"], spawned["attempt"])
```

Use idempotency keys for deduplication at spawn time. Use stable task identity or business identity for external idempotency inside steps.

TypeScript external idempotency:

```typescript
const payment = await ctx.step("process-payment", async () => {
  const idempotencyKey = `${ctx.taskID}:payment`;
  return await stripe.charges.create({
    amount: params.amount,
    idempotencyKey,
  });
});
```

Python external idempotency:

```python
def process_payment():
    idempotency_key = f"{ctx.task_id}:payment"
    return stripe.charges.create(amount=params["amount"], idempotency_key=idempotency_key)


payment = ctx.step("process-payment", process_payment)
```

### 10. Fetching and awaiting task results

TypeScript:

```typescript
const snapshot = await app.fetchTaskResult(taskID);
const finalResult = await app.awaitTaskResult(taskID, { timeout: 30 });

console.log(snapshot?.state, finalResult.state);
```

Python:

```python
snapshot = app.fetch_task_result(task_id)
final_result = app.await_task_result(task_id, timeout=30)

print(snapshot.state if snapshot else None, final_result.state)
```

### 11. Waiting for another task from inside a task

This is durable, but it must target a **different queue** than the current task.

TypeScript:

```typescript
const child = await app.spawn("child-task", {}, { queue: "child-workers" });

const childResult = await ctx.awaitTaskResult(child.taskID, {
  queue: "child-workers",
  timeout: 60,
});

if (childResult.state === "completed") {
  return childResult.result;
}
```

Python:

```python
child = app.spawn("child-task", {}, queue="child-workers")

child_result = ctx.await_task_result(
    child["task_id"],
    queue_name="child-workers",
    timeout=60,
)

if child_result.state == "completed":
    return child_result.result
```

Release note for `0.3.0`: same-queue waits are explicitly rejected to avoid deadlocks under low concurrency.

### 12. Heartbeats

Use heartbeats when a step will run for a while without writing checkpoints.

TypeScript:

```typescript
await ctx.heartbeat(300);
```

Python:

```python
ctx.heartbeat(300)
```

### 13. Cancellation and retry operations

TypeScript:

```typescript
await app.cancelTask(taskID);
await app.cancelTask(taskID, "emails");

const retried = await app.retryTask(taskID, {
  maxAttempts: 5,
  spawnNewTask: false,
});

console.log(retried);
```

Python:

```python
app.cancel_task(task_id)
app.cancel_task(task_id, queue_name="emails")

retried = app.retry_task(task_id, max_attempts=5, spawn_new=False)
print(retried)
```

Tasks observe cancellation at the next `step`, `heartbeat`, or event-wait boundary.

### 14. Starting workers and processing batches

TypeScript long-lived worker:

```typescript
const worker = await app.startWorker({
  concurrency: 4,
  claimTimeout: 120,
  batchSize: 4,
  pollInterval: 0.25,
  workerId: "web-1",
  fatalOnLeaseTimeout: true,
  onError: (err) => console.error(err),
});

await worker.close();
```

TypeScript single batch:

```typescript
await app.workBatch("cron-1", 120, 10);
```

Python blocking worker:

```python
app.start_worker(
    worker_id="web-1",
    claim_timeout=120,
    concurrency=1,
    poll_interval=0.25,
)
```

Python single batch:

```python
app.work_batch(worker_id="cron-1", claim_timeout=120, batch_size=10)
```

### 15. Binding work to a specific connection

TypeScript:

```typescript
import * as pg from "pg";
import { Absurd } from "absurd-sdk";

const pool = new pg.Pool({ connectionString: process.env.PGDATABASE });
const app = new Absurd({ db: pool, queueName: "default" });

const client = await pool.connect();
try {
  const bound = app.bindToConnection(client);
  await bound.spawn("my-task", { key: "value" });
} finally {
  client.release();
}
```

### 16. Hooks for tracing and context propagation

TypeScript:

```typescript
const app = new Absurd({
  hooks: {
    beforeSpawn: (taskName, params, options) => {
      return {
        ...options,
        headers: {
          ...options.headers,
          traceId: "trace-123",
        },
      };
    },
    wrapTaskExecution: async (ctx, execute) => {
      console.log("task", ctx.taskID, "trace", ctx.headers.traceId);
      return await execute();
    },
  },
});
```

Python:

```python
def inject_trace(task_name, params, options):
    options["headers"] = {**(options.get("headers") or {}), "trace_id": "trace-123"}
    return options


def with_tracing(ctx, execute):
    print("task", ctx.task_id, "trace", ctx.headers.get("trace_id"))
    return execute()


app = Absurd(hooks={"before_spawn": inject_trace, "wrap_task_execution": with_tracing})
```

### 17. Python context helpers and sync-async switching

Context variable access:

```python
from absurd_sdk import get_current_context


def helper():
    ctx = get_current_context()
    if ctx is not None:
        ctx.heartbeat(60)
```

Switching between sync and async clients:

```python
async_app = app.make_async()
sync_app = await async_app.make_sync()
```

### 18. absurdctl task and event operations

Spawn tasks:

```bash
absurdctl spawn-task my-task -q default -P foo=bar -P count:=42
absurdctl spawn-task my-task -q default -P user.name=Alice -P user.age:=30
absurdctl spawn-task my-task -q default --params '{"foo":"bar","count":42}'
```

List and inspect tasks:

```bash
absurdctl list-tasks --queue=default --limit=20
absurdctl list-tasks --queue=default --status=failed --limit=20
absurdctl list-tasks --queue=default --task-name=my-task --limit=5
absurdctl dump-task --task-id=<task-id>
absurdctl dump-task --run-id=<run-id>
```

Cancel and retry:

```bash
absurdctl cancel-task <task-id>
absurdctl cancel-task -q default <task-id>

absurdctl retry-task <task-id>
absurdctl retry-task <task-id> --max-attempts 10
absurdctl retry-task -q default <task-id> --spawn-new
```

Guidance:

- plain `retry-task` retries the existing task
- `--spawn-new` creates a brand-new task with the original inputs
- prefer understanding the failure before retrying

Emit events:

```bash
absurdctl emit-event order.completed -q default -P orderId=123
absurdctl emit-event shipment.packed:42 -q default --payload '{"trackingNumber":"XYZ"}'
```

Cleanup:

```bash
absurdctl cleanup default 7
absurdctl cleanup emails 30
```

Install the bundled skill:

```bash
absurdctl install-skill
absurdctl install-skill .pi/skills
absurdctl install-skill ~/.pi/agent/skills --force
```

### 19. Habitat dashboard

Run Habitat:

```bash
habitat run -db-name mydb
habitat run -db-url "postgresql://user:pass@localhost:5432/mydb"
```

Use environment variables:

```bash
export HABITAT_DB_URL="postgresql://user:pass@localhost:5432/mydb"
export HABITAT_LISTEN=":8080"
habitat run
```

Serve under a reverse-proxy prefix:

```bash
habitat run -db-name mydb -base-path /habitat
```

nginx example:

```nginx
location /habitat/ {
    proxy_pass http://localhost:7890/;
    proxy_set_header X-Forwarded-Prefix /habitat;
    proxy_set_header Host $host;
}
```

Habitat shows:

- queues
- tasks
- runs
- checkpoints
- events

Use it for state inspection, retry analysis, and debugging failed or sleeping tasks.

### 20. Cleanup and retention patterns

Direct SQL cleanup:

```sql
select absurd.cleanup_tasks('default', 7 * 86400, 1000);
select absurd.cleanup_events('default', 7 * 86400, 1000);
```

Batch cleanup loop:

```bash
#!/usr/bin/env bash
set -euo pipefail

QUEUE="default"
TTL_SECONDS=$((30 * 86400))
LIMIT=1000

while true; do
  deleted_tasks=$(psql "$PGDATABASE" -Atqc \
    "select absurd.cleanup_tasks('${QUEUE}', ${TTL_SECONDS}, ${LIMIT})")
  deleted_events=$(psql "$PGDATABASE" -Atqc \
    "select absurd.cleanup_events('${QUEUE}', ${TTL_SECONDS}, ${LIMIT})")

  echo "deleted tasks=${deleted_tasks} events=${deleted_events}"

  if [ "$deleted_tasks" = "0" ] && [ "$deleted_events" = "0" ]; then
    break
  fi
done
```

Tracked cleanup as an Absurd task:

```typescript
import * as pg from "pg";
import { Absurd } from "absurd-sdk";

const pool = new pg.Pool({ connectionString: process.env.PGDATABASE });
const app = new Absurd({ db: pool, queueName: "ops" });

app.registerTask({ name: "cleanup-retention" }, async (params, ctx) => {
  const ttlSeconds = params.ttlDays * 86400;
  const limit = params.limit ?? 1000;

  const deletedTasks = await ctx.step("cleanup-tasks", async () => {
    const result = await pool.query(
      "select absurd.cleanup_tasks($1, $2, $3) as deleted",
      [params.targetQueue, ttlSeconds, limit],
    );
    return result.rows[0].deleted as number;
  });

  const deletedEvents = await ctx.step("cleanup-events", async () => {
    const result = await pool.query(
      "select absurd.cleanup_events($1, $2, $3) as deleted",
      [params.targetQueue, ttlSeconds, limit],
    );
    return result.rows[0].deleted as number;
  });

  return { deletedTasks, deletedEvents };
});
```

### 21. Cron deduplication pattern

TypeScript:

```typescript
import { createHash } from "node:crypto";
import { CronExpressionParser } from "cron-parser";
import { Absurd } from "absurd-sdk";

const app = new Absurd({ queueName: "default" });

function dedupKey(taskName: string, expr: string, nextAt: Date): string {
  const slot = nextAt.toISOString().slice(0, 16);
  const raw = `${taskName}|${expr}|${slot}`;
  return `cron:${createHash("sha256").update(raw).digest("hex").slice(0, 24)}`;
}

const nextAt = CronExpressionParser.parse("*/5 * * * *", {
  currentDate: new Date(),
  tz: "UTC",
}).next().toDate();

await app.spawn(
  "send-report",
  { scheduledFor: nextAt.toISOString() },
  { idempotencyKey: dedupKey("send-report", "*/5 * * * *", nextAt) },
);
```

Python:

```python
from datetime import datetime, timezone
from hashlib import sha256

from croniter import croniter
from absurd_sdk import Absurd

app = Absurd(queue_name="default")


def dedup_key(task_name: str, expr: str, next_at: datetime) -> str:
    slot = next_at.astimezone(timezone.utc).isoformat(timespec="minutes")
    raw = f"{task_name}|{expr}|{slot}"
    return "cron:" + sha256(raw.encode()).hexdigest()[:24]


now = datetime.now(timezone.utc).replace(second=0, microsecond=0)
next_at = croniter("*/5 * * * *", now).get_next(datetime)
app.spawn(
    "send-report",
    {"scheduled_for": next_at.isoformat()},
    idempotency_key=dedup_key("send-report", "*/5 * * * *", next_at),
)
```

### 22. Living with code changes

Version the step name when the checkpoint meaning changed:

```typescript
const payment = await ctx.step("process-payment:v2", async () => {
  return {
    chargeId: `charge-${params.amount}`,
    provider: "stripe",
    receiptEmail: params.email ?? null,
  };
});
```

Normalize legacy checkpoint shapes when the change is additive:

```python
def normalize_payment(value):
    if isinstance(value, str):
        return {
            "charge_id": value,
            "provider": "stripe",
            "receipt_email": None,
        }

    return {
        "charge_id": value["charge_id"],
        "provider": value.get("provider", "stripe"),
        "receipt_email": value.get("receipt_email"),
    }
```

Rules of thumb:

- rename the step when semantics changed
- normalize old data once at the boundary when semantics did not change
- split side effects into smaller named steps so versioning stays local
- prefer new task names for major workflow rewrites

### 23. Durable agent turns with pi

Use decomposed steps to append `message_end` events to a durable message log and resume safely.

```typescript
import { Absurd, type StepHandle, type TaskContext } from "absurd-sdk";
import {
  runAgentLoopContinue,
  type AgentContext,
  type AgentEvent,
  type AgentLoopConfig,
  type AgentMessage,
} from "@mariozechner/pi-agent-core";

type MessageLogEntry = { message: AgentMessage };

async function loadMessageLog(ctx: TaskContext): Promise<{
  messages: AgentMessage[];
  nextHandle: StepHandle<MessageLogEntry>;
}> {
  const messages: AgentMessage[] = [];
  while (true) {
    const handle = await ctx.beginStep<MessageLogEntry>("message");
    if (!handle.done) return { messages, nextHandle: handle };
    messages.push(handle.state!.message);
  }
}

const persistEvent = async (
  event: AgentEvent,
  context: AgentContext,
  nextHandle: StepHandle<MessageLogEntry>,
  ctx: TaskContext,
) => {
  if (event.type !== "message_end") return nextHandle;
  await ctx.completeStep(nextHandle, { message: event.message });
  context.messages.push(event.message);
  return await ctx.beginStep<MessageLogEntry>("message");
};
```

### 24. Agent installation and debugging workflow

Install the upstream skill into a common location:

```bash
absurdctl install-skill
absurdctl install-skill .agents/skills --force
```

Recommended agent workflow:

```bash
absurdctl list-queues
absurdctl list-tasks --queue=default --limit=20
absurdctl dump-task --task-id=<task-id>
```

Then decide whether to:

- retry failed work
- emit an event to wake a sleeping task
- spawn a reproducer task
- inspect application code for the registered task handler

### 25. Safe operating rules

Treat these commands as state-changing and potentially production-sensitive:

- `absurdctl init`
- `absurdctl migrate`
- `absurdctl create-queue`
- `absurdctl drop-queue`
- `absurdctl cleanup`
- `absurdctl cancel-task`
- `absurdctl retry-task`
- `absurdctl emit-event`
- `absurdctl spawn-task`

If the target database or queue is ambiguous, ask before executing them.

### 26. Fast copy-paste playbooks

Latest failures in `default`:

```bash
absurdctl list-queues
absurdctl list-tasks --queue=default --status=failed --limit=20
absurdctl dump-task --task-id=<task-id>
```

Wake a sleeping task:

```bash
absurdctl list-tasks --queue=default --status=sleeping --limit=20
absurdctl dump-task --task-id=<task-id>
absurdctl emit-event <event-name> -q default -P key=value
```

Reproduce then inspect:

```bash
absurdctl spawn-task my-task -q default -P foo=bar
absurdctl list-tasks --queue=default --task-name=my-task --limit=5
absurdctl dump-task --task-id=<task-id>
```

Fast path when the user says to spawn a task and debug it:

```bash
absurdctl spawn-task my-task -q default -P foo=bar
absurdctl list-tasks --queue=default --task-name=my-task --limit=5
absurdctl dump-task --task-id=<task-id>
# then either:
absurdctl emit-event <event-name> -q default -P key=value
# or:
absurdctl retry-task <task-id>
```

## Extra reference

- Use `absurdctl <command> --help` for full options.
- `dump-task --task-id` is usually the best starting point once you know the task.
- Checkpointed step results are durable JSON state; code outside steps may execute multiple times across retries.

## When to search code

Only after you know the task name or event name.

TypeScript / JavaScript:

```bash
rg -n "registerTask\(|name:\s*['\"]<task-name>['\"]" .
```

Python:

```bash
rg -n "register_task\(|@.*register_task|['\"]<task-name>['\"]" .
```

If the task is event-driven, also search for the event name.
````

## Detailed Plan

1. Freeze scope to Absurd `0.3.0` and list every authoritative source that can change behavior claims.
2. Build a feature inventory from four surfaces: core concepts, SDK APIs, `absurdctl`, and Habitat/patterns.
3. Separate durable-execution primitives from operator workflows so the skill teaches both building and debugging.
4. Map each feature to at least one concrete example, preferring upstream examples and docs wording where possible.
5. Call out release-specific additions that matter to agent workflows: decomposed steps, bundled skill install, migration SQL generation, and guarded cross-queue waits.
6. Draft the skill in a state-first style: inspect queues and task state before reading source.
7. Add concise TypeScript and Python examples for shared SDK features, then add language-specific examples for Python-only and TypeScript-only APIs.
8. Add command examples for every `absurdctl` capability that an agent is likely to need in setup, inspection, recovery, and cleanup.
9. Add Habitat, cleanup, cron, code-evolution, and pi-agent patterns so the draft covers the operational and long-lived workflow edges.
10. Review the draft against the feature inventory and remove any claims that were not verified in docs, release diff, or upstream skill content.
11. Leave the output as a draft packet so the proposed `SKILL.md` can be copied cleanly while preserving the planning and review artifacts.

## Atomic Checklist

**Task 1**
- [ ] Confirm the release target and source set.
Acceptance criteria:
- Latest stable release is identified as `0.3.0`.
- The docs site, repo, upstream skill, and release diff are all in scope.
- Any claim in the draft can be traced back to one of those sources.

**Task 2**
- [ ] Inventory the core durable-execution model.
Acceptance criteria:
- The draft explains queues, tasks, runs, steps, events, sleeps, retries, and workers.
- The draft distinguishes `task_id` from `run_id`.
- The draft warns that code outside steps can run more than once.

**Task 3**
- [ ] Inventory release-specific additions in `0.3.0`.
Acceptance criteria:
- Decomposed steps are called out.
- `absurdctl install-skill` is called out.
- range-based `migrate --dump-sql` is called out.
- guarded cross-queue child waits are called out.

**Task 4**
- [ ] Cover setup and migration workflows.
Acceptance criteria:
- Fresh install examples exist.
- pinned-release install examples exist.
- upgrade and dry-run examples exist.
- migration SQL generation examples exist.

**Task 5**
- [ ] Cover queue lifecycle operations.
Acceptance criteria:
- queue creation, listing, and deletion are shown.
- at least one CLI example exists.
- at least one SDK example exists.

**Task 6**
- [ ] Cover task registration and checkpoint semantics.
Acceptance criteria:
- shared task-registration examples exist for TypeScript and Python.
- checkpointed `step` usage is shown.
- cancellation defaults and retry defaults are demonstrated.

**Task 7**
- [ ] Cover every task-context primitive.
Acceptance criteria:
- `step` is shown.
- `beginStep` / `completeStep` and `begin_step` / `complete_step` are shown.
- sleep APIs are shown.
- event-wait APIs are shown.
- `awaitTaskResult` inside a task is shown.
- `heartbeat` is shown.
- in-task `emitEvent` / `emit_event` is shown.

**Task 8**
- [ ] Cover spawn-time controls and result inspection.
Acceptance criteria:
- examples include retries, headers, queue override, cancellation, and idempotency.
- `fetchTaskResult` / `fetch_task_result` are shown.
- `awaitTaskResult` / `await_task_result` are shown.
- result snapshots and terminal states are described.

**Task 9**
- [ ] Cover worker operation and recovery APIs.
Acceptance criteria:
- `startWorker` / `start_worker` are shown.
- batch processing is shown.
- cancel and retry APIs are shown.
- same-queue child waits are explicitly described as invalid.

**Task 10**
- [ ] Cover language-specific extras.
Acceptance criteria:
- Python `run_step` is shown.
- Python `get_current_context` is shown.
- Python sync-async switching is shown.
- TypeScript connection binding is shown.
- hooks are shown for both ecosystems.

**Task 11**
- [ ] Cover the full `absurdctl` operator surface.
Acceptance criteria:
- schema commands are shown.
- queue commands are shown.
- spawn, list, dump, cancel, retry, emit, cleanup, and install-skill are shown.
- examples cover typed params and JSON payload forms.

**Task 12**
- [ ] Cover Habitat and operational patterns.
Acceptance criteria:
- Habitat launch and configuration examples exist.
- reverse-proxy example exists.
- cleanup SQL and cron-style retention examples exist.
- the draft explains what Habitat shows.

**Task 13**
- [ ] Cover long-lived workflow patterns.
Acceptance criteria:
- cron deduplication is shown.
- code-evolution guidance is shown.
- pi durable-agent turns are shown.
- the draft states when to rename a step versus normalize checkpoint data.

**Task 14**
- [ ] Review for safety, ordering, and agent usability.
Acceptance criteria:
- the draft tells agents to inspect state before code.
- state-changing commands are marked as sensitive.
- copy-paste playbooks exist for common debugging flows.
- unsupported claims and speculative behavior are removed.

**Task 15**
- [ ] Final coverage pass.
Acceptance criteria:
- every documented feature category has at least one example.
- all examples are internally consistent with `0.3.0` naming.
- the proposed `SKILL.md` can be extracted cleanly from this draft packet.
