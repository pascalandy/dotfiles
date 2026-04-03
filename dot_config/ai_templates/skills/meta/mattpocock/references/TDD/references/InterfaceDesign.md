# Interface Design for Testability

Good interfaces make testing natural. Bad interfaces require workarounds (mocks, stubs, test-only methods) to test at all.

## Principles

### 1. Accept Dependencies, Don't Create Them

```typescript
// Testable: caller controls the dependency
function processOrder(order: Order, paymentGateway: PaymentGateway): OrderResult {
  const charge = paymentGateway.charge(order.total);
  return { orderId: order.id, charged: charge.amount };
}

// Hard to test: creates its own dependency internally
function processOrder(order: Order): OrderResult {
  const gateway = new StripeGateway(); // Can't substitute in tests
  const charge = gateway.charge(order.total);
  return { orderId: order.id, charged: charge.amount };
}
```

### 2. Return Results, Don't Produce Side Effects

```typescript
// Testable: caller can inspect the return value
function calculateDiscount(cart: Cart): Discount {
  return { amount: cart.total * 0.1, reason: "loyalty" };
}

// Hard to test: mutates the argument, nothing to assert on directly
function applyDiscount(cart: Cart): void {
  cart.total -= cart.total * 0.1; // Side effect on input
}
```

### 3. Small Surface Area

- Fewer methods = fewer tests needed
- Fewer parameters = simpler test setup
- Each method does one thing = each test verifies one behavior

## Testing Implication

When an interface follows these principles, tests:
- Need minimal setup (no complex mock wiring)
- Have clear assertions (return values, not side effects)
- Are independent of implementation details
- Read like specifications of behavior
