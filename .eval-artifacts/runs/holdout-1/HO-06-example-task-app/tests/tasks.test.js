const test = require("node:test");
const assert = require("node:assert");
const T = require("../tasks.js");

const sample = () => [
  { id: 1, title: "a", done: true },
  { id: 2, title: "b", done: false },
  { id: 3, title: "c", done: true },
  { id: 4, title: "d", done: false },
];

test("clearCompleted removes only done tasks", () => {
  assert.ok(T.clearCompleted(sample()).every((t) => !t.done));
});

test("clearCompleted keeps undone tasks in order", () => {
  assert.deepStrictEqual(T.clearCompleted(sample()).map((t) => t.id), [2, 4]);
});

test("empty list stays empty", () => {
  assert.deepStrictEqual(T.clearCompleted([]), []);
});

test("list with no done tasks is unchanged", () => {
  const l = [{ id: 1, title: "a", done: false }];
  assert.deepStrictEqual(T.clearCompleted(l), l);
});

test("all-done list becomes empty", () => {
  assert.deepStrictEqual(
    T.clearCompleted([{ id: 1, title: "a", done: true }]),
    []
  );
});

test("clearCompleted does not mutate input", () => {
  const l = sample();
  const copy = JSON.parse(JSON.stringify(l));
  T.clearCompleted(l);
  assert.deepStrictEqual(l, copy);
});

test("handleClearCompleted removes nothing when confirm returns false", () => {
  const l = sample();
  assert.strictEqual(T.handleClearCompleted(l, () => false), l);
});

test("handleClearCompleted removes done tasks when confirm returns true", () => {
  assert.deepStrictEqual(
    T.handleClearCompleted(sample(), () => true).map((t) => t.id),
    [2, 4]
  );
});

test("handleClearCompleted does not prompt with zero completed", () => {
  let called = false;
  const l = [{ id: 1, title: "a", done: false }];
  const r = T.handleClearCompleted(l, () => { called = true; return true; });
  assert.strictEqual(called, false);
  assert.strictEqual(r, l);
});
