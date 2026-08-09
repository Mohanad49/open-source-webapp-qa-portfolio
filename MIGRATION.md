# Selenium → Playwright: what the numbers actually said

This repository is the Selenium suite. Its successor is
[orangehrm-playwright](https://github.com/Mohanad49/orangehrm-playwright). Both run
nightly, both report into [TestPulse](https://testpulse-eight.vercel.app), and this
document is the comparison between them.

I wrote it expecting to conclude "Playwright is faster and less flaky, migrate." That is
the conclusion everyone writes. My own data does not support it as stated, and working
out why was more useful than the conclusion would have been.

---

## Read this before the numbers

**These are not two implementations of the same suite.** This one drives
[The Internet](https://the-internet.herokuapp.com) — a public Heroku instance, 70
collected checks from 36 test functions, most of them small. The Playwright suite drives
[OrangeHRM](https://www.orangehrm.com/) — a containerised instance built and seeded from
scratch in CI, 18 tests, most of them multi-step business workflows like *create an
employee* or *apply for leave and verify the balance*.

So this is not a controlled experiment. Two things changed at once: the framework **and**
the environment. Most of the table below is therefore evidence about my two suites rather
than about Selenium versus Playwright in general, and I have marked which is which.

I could have made it look controlled by porting these 70 checks to Playwright and
reporting a clean before/after. I did not, because that would be a benchmark of
`the-internet.herokuapp.com`'s response times on two different evenings, dressed up as a
framework comparison.

## The measured numbers

All figures below are read from TestPulse's rolling window, not from a stopwatch on a
good day — 44 runs for this suite, 50 for the Playwright one, as of 2026-08-09.

| | Selenium / pytest (this repo) | Playwright / TS |
|---|---:|---:|
| Tests | 70 collected (36 functions) | 18 |
| Pass rate over the window | 97.86% | 98.55% |
| **Tests classified flaky** | **17 of 70 — 24.3%** | **1 of 18 — 5.6%** |
| Mean run wall-clock | 175.7 s | 101.4 s |
| Most recent run | 93.0 s | 56.5 s |
| Run-duration trend | −0.9 s per run | −5.5 s per run |
| Mean per-test duration | 2,510 ms | 7,128 ms |
| Test + page-object lines | 765 | 875 |
| Config lines | 104 (`conftest.py`) | 69 (`playwright.config.ts`) |

### Three of those rows do not mean what they look like

**Per-test duration says Selenium is nearly 3× faster.** It is not. A test here asserts
that a link points at a path; a test there creates an employee through a multi-step form
and verifies the record in a table. Comparing their durations compares the workloads, not
the frameworks. Anyone quoting "2,510 ms vs 7,128 ms" as a framework benchmark is quoting
a fact about my test design.

**Lines of code says Playwright cost me more.** 875 lines for 18 tests against 765 for
70. Same reason. The one honest read is per-page-object: Selenium's five page objects
carry 411 lines, Playwright's five carry 531, and the extra is mostly explicit typing —
which is a cost paid at write time and refunded at rename time.

**Total wall-clock says Playwright is 43% faster.** Also confounded: it runs against
localhost, this one crosses the public internet to a free Heroku dyno. The honest version
of that row is the *trend* — −5.5 s per run against −0.9 s — because both are measured
against themselves. The Playwright suite is getting faster roughly six times as quickly,
and that is a fact about work I did on it, not about the tool.

## The row that does mean something, and it is not the tool

**24.3% flaky against 5.6%** is the largest gap here, and my first instinct was to credit
Playwright's auto-waiting. Then I looked at *which* tests were flaky:

```
0.02  pass=95.5%  test_valid_user_can_log_in
0.02  pass=90.9%  test_key_example_link_points_to_expected_path[Dropdown-/dropdown]
0.02  pass=90.9%  test_home_page_exposes_large_acceptance_test_catalog
0.02  pass=90.9%  test_key_example_link_points_to_expected_path[A/B Testing-/abtest]
0.02  pass=90.9%  test_key_example_link_points_to_expected_path[Checkboxes-/checkboxes]
```

Three of the top five assert that a link on a static page points where it says it does.
There is no race condition in that. No amount of auto-waiting fixes it, because nothing
is waiting for anything — the page simply did not arrive that night. These are a free
Heroku dyno cold-starting, and they would flake identically in Playwright, Cypress, or
curl.

The Playwright suite's single flaky test is `Edit employee personal details → save →
verify update`, at 98% — a genuine, occasional, save-then-read race. One real flake in a
suite, correctly identified.

**So the honest finding is: the framework change is not what moved flakiness. Controlling
the environment is.** The Playwright suite got a Dockerised, seeded instance; this one
still points at a shared public demo. That decision is worth more than the framework
decision, and it is the transferable lesson — you can buy most of that improvement
without rewriting a single test.

There is a second-order effect I will not pretend to have isolated: because the Playwright
suite runs against an instance nobody else touches, I could afford `retries: 1` with a
reporter that records *each attempt separately*, so a retry is captured as flake evidence
instead of hidden. That is a Playwright capability this repo cannot match — pytest has no
equivalent per-attempt record — and it is the one place where the tool genuinely changed
what I can observe.

## What Selenium still does better

Kept deliberately, not as a consolation section.

- **Reach.** Real Safari, real Edge, IE mode, mobile browsers via Appium's WebDriver
  lineage, and a grid you can point at a device farm. Playwright drives browser *engines*;
  when a bug is in Apple's Safari rather than in WebKit, Selenium is the tool that sees it.
- **It is a W3C standard.** WebDriver is a specification with multiple implementations.
  Playwright is one vendor's protocol, and a suite written against it is a bet on that
  vendor.
- **Language breadth with first-class parity.** Java, C#, Ruby, Python, JS — a Selenium
  suite can live in whatever language the team already reviews.
- **It is what enterprises actually run.** A large share of QA job specs still say
  Selenium, and a portfolio with no Selenium artifact fails a keyword screen before a
  human reads it. That is a real reason to keep this repository, and I would rather state
  it than pretend it is purely technical.

What I do not miss: `WebDriverWait` on every interaction, driver-binary version drift, and
having no first-class trace to open when CI fails and my machine does not.

## What I would do next, in order

1. **Point this suite at a container**, the way the Playwright one is. If the 17 flaky
   tests are the network rather than the code, that single change should collapse most of
   them — and because both suites report into TestPulse, the before-and-after is already
   being recorded. This is the experiment the document above is missing, and it is cheap.
2. **Then** re-read the flake numbers. Whatever survives a controlled environment is the
   part that is actually about the framework, and that comparison would be worth
   publishing.
3. Move the Playwright suite's auth from `beforeEach` to a `storageState` fixture, so
   sixteen of its eighteen tests stop logging in through the UI to reach their
   precondition.

## Why this repository is not archived

It is the control. Retiring it would delete the only baseline I have, and the number that
matters most in this document — 17 flaky tests concentrated in checks that cannot race —
only exists because both suites kept running side by side, into the same tool, long enough
for a rolling window to mean something.

That mirrors the migration I did at work, where the Selenium suite kept running until the
Playwright one had earned the right to replace it. The version of this comparison I would
have written on day one, from intuition, would have credited the framework for all of it.
