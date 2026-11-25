
const fs = require('fs');
const fullCode = fs.readFileSync('scratch/classroom.js', 'utf8');

// Find the engine functions
const startIdx = fullCode.indexOf('var vr={orange:');
const endIdx = fullCode.indexOf('function dh()');
const engineCode = fullCode.substring(startIdx, endIdx);

// Wrap and evaluate in a node sandbox
const vm = require('vm');
const sandbox = {
  console: console,
  document: {
    fonts: { addEventListener: () => {} },
    createElement: () => ({ getContext: () => ({ font: '', measureText: (t) => ({ width: t.length * 6 }) }) })
  },
  window: {},
  getComputedStyle: () => ({ getPropertyValue: () => 'monospace' })
};
vm.createContext(sandbox);

try {
  // Execute engine
  vm.runInContext(engineCode, sandbox);
  console.log("Engine loaded successfully!");
} catch (e) {
  console.error("Error evaluating engine:", e);
}
