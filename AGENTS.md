# Contributor Guide

## Before you start developing
- Ensure all tests pass before you begin development by running `make test`
- Ensure all linting etc is correct before you begin development by running `make lint`

## Development guidelines
- Use black style formatting.
- Ensure every function has complete documentation using numpy style docstrings.
- Strictly use type hinting.
- Use perfect spelling and grammar for all documentation etc. Use Australian english.

## Testing Instructions
- Find the CI plan in the .github/workflows folder.
- Run `make test` to run every test.
- From the package root you can just call `make test`. The commit should pass all tests before you merge.
- Fix any test or type errors until the whole suite is green.
- After moving files or changing imports, run `make lint` to be sure all linting rules still pass.
- Add or update tests for the code you change, even if nobody asked.

## PR instructions
- Use [Conventional Commits](https://www.conventionalcommits.org/) for commit mesasges.
  - Using any aof the following types fix:, feat:, chore:, ci:, docs:, style:, refactor:, perf:, test:
  - Do not use a body or footer unless indicating a BREAKING CHANGE