import { readFileSync } from 'node:fs';

const html = readFileSync(new URL('../index.html', import.meta.url), 'utf8');
const checks = [
  'Atlas Agent Lab',
  'Prompt Injection',
  'Evaluation harness',
  'runPipeline',
  'RAG',
  'tool router'
];

const missing = checks.filter(x => !html.toLowerCase().includes(x.toLowerCase()));
if (missing.length) {
  console.error('Smoke test failed. Missing: ' + missing.join(', '));
  process.exit(1);
}
if (html.length < 15000) {
  console.error('Smoke test failed. index.html is unexpectedly small.');
  process.exit(1);
}
console.log('Smoke test passed. Inspected ' + html.length.toLocaleString() + ' HTML bytes.');