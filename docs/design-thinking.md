# Design Thinking: Open-Source Web App QA Portfolio

## Purpose

This project proves that the owner can build a recruiter-accessible UI automation framework from scratch, not just write isolated Selenium scripts.

The target users are:

- QA hiring managers checking automation structure and test judgment.
- Recruiters looking for visible evidence behind resume claims.
- The author, who needs a reusable portfolio repo that can grow into API, performance, and mobile tracks.

## Target application

The suite tests Sauce Labs' open-source **The Internet** application, a deliberately broad acceptance-test playground covering authentication, forms, dynamic waits, tables, JavaScript alerts, file upload, and browser windows.

## Tone

**Industrial QA war room.**

Not soft SaaS. Not purple gradient portfolio filler. The aesthetic direction is stark, operational, and command-center-like: dark graphite surfaces, amber hazard accents, grid overlays, terminal energy, and aggressive typography.

## Differentiation

The memorable idea: **a release control room for defects before production.**

The repository is not just test code. It includes:

- A real PyTest/Selenium framework.
- Page Object Model separation.
- Allure and pytest-html reporting.
- GitHub Actions CI.
- GitHub Pages-ready static report hub.
- Test strategy and defect-template documentation.

## Technical constraints

- Python + PyTest + Selenium WebDriver.
- Chrome and Firefox support.
- Headless CI execution.
- Explicit waits only; no fragile sleeps.
- Environment-based configuration.
- Allure-compatible artifacts.
- Static report hub deployable to GitHub Pages.
- Accessibility-aware color contrast and keyboard-readable content.

## Execution principle

The design is intentionally loud in the reporting layer and intentionally boring in the framework internals. Good QA automation should be dramatic to review but predictable to maintain.
