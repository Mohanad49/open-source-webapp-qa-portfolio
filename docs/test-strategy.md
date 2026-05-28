# Test Strategy

## Scope

Target: `https://the-internet.herokuapp.com`

The framework validates representative browser behaviors that appear in production web applications:

- Authentication and session access control.
- Navigation integrity.
- Checkbox, dropdown, and numeric input behavior.
- Dynamic loading and AJAX-style controls.
- Table content and sorting.
- JavaScript alert and prompt handling.
- File upload.
- Multi-window handling.
- Status-code messaging.

## Out of scope

- Visual snapshot testing.
- Security scanning.
- BrowserStack/Sauce Labs cloud grid execution.
- Backend/database validation.
- Performance testing.

Those are intentionally excluded so this repository stays focused on clean UI automation.

## Risk-based priorities

| Priority | Area | Reason |
|---|---|---|
| P0 | Login/logout | Core user access path. |
| P0 | Dynamic loading | Common source of flaky automation when waits are weak. |
| P1 | Forms | Regression-prone interaction layer. |
| P1 | Tables | Validates data display and sorting behavior. |
| P2 | Windows/alerts/uploads | Browser-level interactions that show automation maturity. |

## Test design approach

- Use Page Object Model for reusable behavior.
- Prefer semantic assertions over screenshots.
- Use parameterization to expand coverage without duplicating code.
- Capture screenshots and HTML source on failure.
- Keep test data explicit and searchable.

## Exit criteria

A release branch is considered portfolio-ready when:

- Smoke suite passes locally.
- Full regression suite passes in GitHub Actions.
- HTML and Allure reports are generated.
- GitHub Pages report hub is deployed.
