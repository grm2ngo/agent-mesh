// greet.js — trivial artifact of wave 1 (task w1-s1-greet).
// Greeting format claim: AGENT_VERDICTS.md V-001 (VERIFIED).

/** Greet a person by name. @param {string} name @returns {string} */
function greet(name) {
  if (typeof name !== "string" || name.length === 0) {
    throw new TypeError("greet(name): name must be a non-empty string");
  }
  return `Hello, ${name}!`;
}

module.exports = { greet };
