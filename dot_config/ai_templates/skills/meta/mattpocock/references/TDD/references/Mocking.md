# When to Mock

Mock at **system boundaries** only. Everything else should use real implementations.

## Mock These (System Boundaries)

- External APIs (payment processors, email services, third-party integrations)
- Databases (sometimes -- prefer a test database or local substitute like PGLite/SQLite)
- Time and randomness (when deterministic behavior is needed for assertions)
- File system (sometimes -- prefer a temp directory)

## Do Not Mock These (Your Own Code)

- Your own classes or modules
- Internal collaborators
- Anything you control and can run in a test environment

## Designing for Mockability

### 1. Dependency Injection

Pass external dependencies in -- do not create them internally. This makes substitution at boundaries natural.

```typescript
// Easy to mock: dependency is injected
async function processPayment(
  amount: number,
  gateway: PaymentGateway
): Promise<PaymentResult> {
  return gateway.charge(amount);
}

// Hard to mock: dependency is created internally
async function processPayment(amount: number): Promise<PaymentResult> {
  const gateway = new StripeGateway(); // Can't substitute
  return gateway.charge(amount);
}
```

### 2. Prefer SDK-Style Interfaces Over Generic Fetchers

```typescript
// Good: each method is specific and independently mockable
const paymentAPI = {
  charge(amount: number, currency: string): Promise<Charge> { ... },
  refund(chargeId: string): Promise<Refund> { ... },
  getBalance(): Promise<Balance> { ... },
};

// Less good: generic fetch, harder to mock meaningfully
async function callPaymentAPI(endpoint: string, options: RequestInit): Promise<Response> {
  return fetch(`https://api.stripe.com/${endpoint}`, options);
}
```

Benefits of the SDK-style approach:
- Each mock returns one specific shape -- no conditional logic in test setup
- Easier to see which endpoints a test exercises
- Type safety per endpoint
