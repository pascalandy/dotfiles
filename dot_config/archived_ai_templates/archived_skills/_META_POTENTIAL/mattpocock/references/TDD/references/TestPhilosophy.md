# Test Philosophy

## Good Tests

Integration-style tests that exercise real code paths through public APIs.

Characteristics:
- Tests behavior users/callers care about
- Uses public API only
- Survives internal refactors
- Describes WHAT the system does, not HOW
- One logical assertion per test
- Test name describes the behavior, not the implementation

### Example: Good Test

```typescript
test("checkout applies discount and returns updated total", async () => {
  const cart = await createCart();
  await addItem(cart.id, { productId: "widget-1", quantity: 2 });

  const result = await checkout(cart.id, { discountCode: "SAVE10" });

  expect(result.total).toBe(18.00); // 2 × $10 - 10%
  expect(result.status).toBe("completed");
});
```

This test:
- Uses the public interface (`createCart`, `addItem`, `checkout`)
- Verifies behavior ("applies discount and returns updated total")
- Would survive any internal refactor of the checkout logic

## Bad Tests

Implementation-detail tests coupled to internal structure.

Red flags:
- Mocking internal collaborators (your own classes/modules)
- Testing private methods
- Asserting on call counts or invocation order
- Test name describes HOW, not WHAT
- Test breaks when refactoring without behavior change
- Verifying by bypassing the interface instead of through it

### Example: Bad Test (Mock Assertions)

```typescript
test("checkout calls discount service", async () => {
  const mockDiscountService = jest.fn().mockReturnValue(0.10);
  const mockCartRepo = jest.fn().mockReturnValue({ items: [{ price: 10, qty: 2 }] });

  await checkout("cart-1", { discountCode: "SAVE10" }, mockDiscountService, mockCartRepo);

  expect(mockDiscountService).toHaveBeenCalledWith("SAVE10");
  expect(mockCartRepo).toHaveBeenCalledTimes(1);
});
```

This test breaks if you refactor how discounts are applied, even if the behavior is unchanged.

### Example: Bad Test (Bypassing the Interface)

```typescript
test("createUser saves to database", async () => {
  await createUser({ name: "Alice", email: "alice@example.com" });

  // BAD: Bypasses the interface to verify
  const row = await db.query("SELECT * FROM users WHERE email = 'alice@example.com'");
  expect(row).toBeDefined();
});
```

### Example: Good Version (Through the Interface)

```typescript
test("createUser makes user retrievable by email", async () => {
  await createUser({ name: "Alice", email: "alice@example.com" });

  // GOOD: Verifies through the public interface
  const user = await getUser("alice@example.com");
  expect(user.name).toBe("Alice");
});
```

## The Distinction

A test should answer: "Does the system do what users expect?" Not: "Does the system do it the way I think it should internally?"

If you refactor the internals and no behavior changes, zero tests should break. If tests break, they were testing implementation, not behavior.
