// greet.test.js — wave 1 acceptance test (task w1-s1-greet).
// Run: node --test   (built-in runner; verdict V-003)
const test = require("node:test");
const assert = require("node:assert/strict");
const { greet } = require("./greet.js");

test("greets a name with the fixed format", () => {
  assert.equal(greet("Mesh"), "Hello, Mesh!");
});

test("rejects empty and non-string input", () => {
  assert.throws(() => greet(""), TypeError);
  assert.throws(() => greet(undefined), TypeError);
});
