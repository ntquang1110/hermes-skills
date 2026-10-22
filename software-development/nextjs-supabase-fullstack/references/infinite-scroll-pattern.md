# Infinite Scroll Pattern (IntersectionObserver)

## Use case

When a feed shows many items (100+) and rendering all at once causes performance issues or the user wants incremental loading.

## Pattern: Batch render + IntersectionObserver sentinel

Works with any list of items. The server passes ALL items (fetched via Supabase or API), the client batches them.

### State variables

```typescript
const BATCH_SIZE = 20; // Items per batch
const [visibleCount, setVisibleCount] = useState(BATCH_SIZE);
const sentinelRef = useRef<HTMLDivElement>(null);
```

### Filtered list + visible slice

```typescript
const visibleCards = filtered.slice(0, visibleCount);
const hasMore = visibleCount < filtered.length;
```

### Reset on filter change

```typescript
useEffect(() => {
  setVisibleCount(BATCH_SIZE);
}, [topicFilter, readFilter]); // Dependencies = all filter state vars
```

### IntersectionObserver sentinel

```typescript
const filteredRef = useRef(filtered.length);
filteredRef.current = filtered.length;

useEffect(() => {
  const el = sentinelRef.current;
  if (!el) return;
  const observer = new IntersectionObserver(
    (entries) => {
      if (entries[0].isIntersecting) {
        setVisibleCount((prev) => Math.min(prev + BATCH_SIZE, filteredRef.current));
      }
    },
    { rootMargin: "200px" } // Load 200px before reaching the sentinel
  );
  observer.observe(el);
  return () => observer.disconnect();
}, [filtered.length]);
```

### JSX sentinel

```tsx
{/* Sentinel — triggers next batch load */}
{hasMore && (
  <div ref={sentinelRef} className="text-center py-6 text-[var(--color-text-tertiary)]">
    <div className="inline-block w-5 h-5 border-2 border-[var(--color-accent)] border-t-transparent rounded-full animate-spin" />
    <p className="text-xs mt-2">Đang tải thêm...</p>
  </div>
)}

{/* End marker */}
{!hasMore && filtered.length > BATCH_SIZE && (
  <div className="text-center py-6 text-[var(--color-text-tertiary)] text-xs">
    ─ Đã hiển thị tất cả {filtered.length} bài ─
  </div>
)}
```

## Important details

1. **Dependency on `filtered.length`** — the effect re-runs when total filtered count changes (new filter applied). This avoids stale closures.
2. **`rootMargin: "200px"`** — triggers the load before the user reaches the bottom, so the next batch is ready when they scroll there.
3. **`setVisibleCount` uses a callback** (`prev => ...`) — this prevents stale closure issues with `filtered.length`.
4. **Reset `visibleCount` on filter change** — otherwise the user switches filters and still sees only old data beyond the previous count.
5. **`filtered` must be defined BEFORE the effect** — in JavaScript, `const filtered = ...` is NOT hoisted. If the effect references `filtered.length` in its dependency array, `filtered` must be declared above the effect (use `useMemo` to compute filtered data before the observer effect).

## PITFALL: `filtered` used before declaration

```typescript
// ❌ BROKEN — ReferenceError: Cannot access 'filtered' before initialization
useEffect(() => { /* depends on filtered.length */ }, [filtered.length]);
const filtered = ...;
// filtered is referenced in the dependency array above ITS declaration

// ✅ CORRECT — useMemo moves filtered computation before the effect
const filtered = useMemo(() => ..., [deps]);
useEffect(() => { /* depends on filtered.length */ }, [filtered.length]);
```

## PITFALL: Stale closure inside IntersectionObserver callback

When `filtered` is a derived value (`useMemo` or computed during render), the `IntersectionObserver` callback captures it from the closure at the time the effect ran. If `filtered.length` is in the dependency array, the effect re-runs when the count changes, so the closure should be correct. BUT — with async-loaded data (like read status from a fetch), the order of updates can cause a race where the callback sees a stale value.

**Most reliable fix — use `useRef` to break the closure:**

```typescript
// Store the live value in a ref (updated every render)
const filteredRef = useRef(filtered.length);
filteredRef.current = filtered.length;

useEffect(() => {
  const el = sentinelRef.current;
  if (!el) return;
  const observer = new IntersectionObserver(
    (entries) => {
      if (entries[0].isIntersecting) {
        // Read from ref — always current, no stale closure
        setVisibleCount((prev) => Math.min(prev + BATCH_SIZE, filteredRef.current));
      }
    },
    { rootMargin: "200px" }
  );
  observer.observe(el);
  return () => observer.disconnect();
}, [filtered.length]);
```

The ref is updated every render (before the effect runs), so the callback always reads the latest `filtered.length` regardless of when the effect was set up.

## PITFALL: Sentinel not rendered when data is still loading

If the sentinel is inside a `{hasMore && (...)}` conditional, and `hasMore` depends on `filtered.length`, there's a window where the sentinel is NOT rendered:

1. Page loads, read status is still loading
2. `readIds` is empty → ALL cards pass the "unread" filter → `filtered` = full list
3. `hasMore = (visibleCount < filtered.length)` = TRUE → sentinel IS rendered
4. Observer attaches to sentinel, works correctly

This case works. But if `filtered` computation throws or returns 0 initially (e.g., cards haven't loaded from server yet), `hasMore` could be false and the sentinel never renders. **Solution:** Always render the sentinel when there are ANY cards, regardless of filter state:

```tsx
{/* Always render sentinel when there are cards — even during loading */}
{dbCards.length > 0 && (
  <div ref={sentinelRef} className={hasMore ? "" : "hidden"} />
)}
```
