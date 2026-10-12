import js from '@eslint/js';
import globals from 'globals';

export default [
  { ignores: ['node_modules/', 'output/', '.vscode-test/'] },
  js.configs.recommended,
  {
    files: ['**/*.js'],
    languageOptions: { ecmaVersion: 2022, sourceType: 'commonjs', globals: { ...globals.node } },
    rules: { 'no-unused-vars': ['error', { argsIgnorePattern: '^_' }] },
  },
];
