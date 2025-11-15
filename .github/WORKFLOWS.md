# GitHub Actions Workflows

This document describes all GitHub Actions workflows configured for this repository and how they work together to ensure code quality, security, and smooth PR/merge processes.

## Overview

We have 4 main workflows that run automatically:

1. **Tests** (`tests.yml`) - Main testing and coverage workflow
2. **PR Labeler** (`pr-labeler.yml`) - Automatic PR labeling and stats
3. **Merge Checks** (`merge-checks.yml`) - Pre-merge validation
4. **Security** (`security.yml`) - Dependency and code security scanning

## Workflow Details

### 1. Tests (`tests.yml`)

**Triggers:**
- Push to `main`, `master`, `develop`, or `claude/*` branches
- Pull requests to `main`, `master`, or `develop`
- Merge queue events

**Jobs:**

#### Test Job
- **Platforms:** Ubuntu, Windows, macOS
- **Python Versions:** 3.8, 3.9, 3.10, 3.11, 3.12
- **Total Combinations:** 15 (3 OS × 5 Python versions)

**What it does:**
1. Sets up Python environment
2. Installs dependencies with caching
3. Runs pytest with coverage (95% minimum required)
4. Generates coverage reports (XML, HTML, terminal)
5. Creates coverage badge
6. Posts coverage report as PR comment
7. Uploads coverage to Codecov
8. Uploads coverage artifacts

**Key Features:**
- ✅ Parallel execution across all platform/version combinations
- ✅ Automatic PR comments with detailed coverage reports
- ✅ Fails if coverage drops below 95%
- ✅ Coverage badge generation
- ✅ HTML coverage reports as artifacts

#### Lint Job
- **Platform:** Ubuntu only
- **Python Version:** 3.11

**What it does:**
1. Checks code with flake8 (syntax errors and PEP 8 compliance)
2. Verifies formatting with black
3. Checks import sorting with isort
4. Posts code quality report as PR comment
5. Fails if any linting check fails

**Key Features:**
- ✅ Automatic PR comments with code quality results
- ✅ Helpful commands to fix issues locally
- ✅ Catches formatting issues before merge

#### Test Summary Job
- **Platform:** Ubuntu only
- Waits for both test and lint jobs to complete
- Provides overall pass/fail status
- Useful as a single required status check

**PR Comments:**
This workflow posts two types of comments on PRs:

1. **Coverage Report Comment:**
   ```
   📊 Test Coverage Report
   Overall Coverage: 99%
   [Detailed line-by-line coverage]
   ✅ Coverage meets the required threshold!
   ```

2. **Code Quality Report Comment:**
   ```
   🔍 Code Quality Report
   ✅ Flake8 (Linting): success
   ✅ Black (Formatting): success
   ✅ isort (Import Sorting): success
   ```

### 2. PR Labeler (`pr-labeler.yml`)

**Triggers:**
- Pull requests (opened, synchronized, reopened)

**What it does:**
1. Analyzes changed files in the PR
2. Automatically adds relevant labels based on file types:
   - `tests` - Test file changes
   - `documentation` - Markdown/docs changes
   - `ci/cd` - GitHub Actions changes
   - `enhancement` - Python code changes
   - `dependencies` - Requirements file changes
   - `configuration` - Config file changes

3. Adds size labels based on total changes:
   - `size/XS` - < 10 lines
   - `size/S` - 10-49 lines
   - `size/M` - 50-199 lines
   - `size/L` - 200-499 lines
   - `size/XL` - 500+ lines

4. Posts PR stats comment (on first open):
   ```
   📏 Pull Request Stats
   Files Changed: 3
   Lines Added: +150
   Lines Deleted: -20
   Total Changes: 170
   ```

**Benefits:**
- 🏷️ Automatic organization of PRs
- 📊 Quick visibility into PR scope
- 🔍 Easy filtering of PRs by type
- 📈 Size awareness for reviewers

### 3. Merge Checks (`merge-checks.yml`)

**Triggers:**
- Pull requests (opened, synchronized, reopened, ready_for_review)
- Only runs on non-draft PRs

**What it does:**
1. Checks if PR is up to date with base branch
2. Detects merge conflicts
3. Posts merge readiness status as PR comment
4. Fails the check if conflicts exist

**PR Comment Example:**
```
🔀 Merge Status: ✅ Ready to merge!

Checklist:
✅ Up to date with base branch
✅ No merge conflicts
```

**Benefits:**
- 🚨 Early conflict detection
- ⚡ Prevents stale PR merges
- 🔄 Encourages keeping PRs updated
- ✅ Clear merge readiness indicator

### 4. Security (`security.yml`)

**Triggers:**
- Push to `main`, `master`, or `develop`
- Pull requests to `main`, `master`, or `develop`
- Weekly schedule (Mondays at 00:00 UTC)

**Jobs:**

#### Dependency Check
**What it does:**
1. Scans dependencies with Safety (checks for known CVEs)
2. Scans dependencies with pip-audit (PyPI advisories)
3. Posts security report as PR comment
4. Uploads security reports as artifacts

**PR Comment Example:**
```
🔒 Security Scan Results

✅ Safety Check: success
✅ Pip Audit: success

✅ No known security vulnerabilities found in dependencies.
```

#### Code Security Analysis
**What it does:**
1. Runs Bandit security scanner on Python code
2. Checks for common security issues (SQL injection, XSS, etc.)
3. Posts code security report as PR comment
4. Uploads Bandit report as artifact

**PR Comment Example:**
```
🛡️ Code Security Analysis

✅ Bandit Security Scan: success

✅ No security issues detected in code.
```

**Benefits:**
- 🔒 Automatic vulnerability detection
- 📅 Weekly scans on main branch
- 🚨 Early warning for security issues
- 📊 Security reports for audit trail

## How Workflows Work Together

### On Pull Request Creation:

1. **PR Labeler** runs first
   - Adds labels and posts stats comment

2. **Tests** workflow starts
   - Runs on all platforms/versions in parallel
   - Runs linting checks
   - Posts coverage and code quality comments

3. **Merge Checks** runs
   - Checks for conflicts
   - Posts merge readiness status

4. **Security** workflow runs
   - Scans dependencies
   - Scans code
   - Posts security reports

### On Push to Main Branch:

1. **Tests** workflow runs
   - Validates all tests still pass
   - Updates coverage

2. **Security** workflow runs
   - Scans for vulnerabilities
   - Archives reports

### Weekly Schedule:

1. **Security** workflow runs every Monday
   - Catches newly disclosed vulnerabilities
   - Ensures dependencies stay secure

## Required Status Checks

For branch protection, require these checks to pass:

**Minimum (Recommended):**
- `test (ubuntu-latest, 3.11)` - At least one full test run
- `lint` - Code quality must pass
- `test-summary` - Overall status check

**Full Protection:**
- All `test` jobs (15 total)
- `lint`
- `test-summary`
- `merge-readiness`

See [BRANCH_PROTECTION.md](BRANCH_PROTECTION.md) for detailed setup instructions.

## Artifacts Generated

Each workflow run generates artifacts that can be downloaded:

### Tests Workflow
- `coverage-badge` - SVG badge showing coverage percentage
- `coverage-report` - Full HTML coverage report

### Security Workflow
- `security-reports` - JSON reports from Safety and pip-audit
- `bandit-report` - JSON report from Bandit scan

**To download artifacts:**
1. Go to Actions tab
2. Click on a workflow run
3. Scroll to "Artifacts" section
4. Click to download

## PR Comment Management

All workflows use **smart comment management**:
- Comments are created once on PR open
- Subsequent runs **update** the existing comment
- No spam from multiple workflow runs
- Comments are clearly identified by emoji headers

## Viewing Workflow Results

### In Pull Requests
1. **Checks Tab** - See all workflow runs and their status
2. **Conversation Tab** - See automated comments with results
3. **Files Changed Tab** - See coverage information inline (if Codecov is configured)

### In Actions Tab
1. Click **Actions** in repository menu
2. See all workflow runs
3. Filter by workflow, branch, or status
4. Click any run to see detailed logs

## Troubleshooting Workflows

### Tests Failing
```bash
# Run tests locally first
pytest --cov=automated_downloader --cov-report=html

# Check coverage
open htmlcov/index.html

# Fix linting
black automated_downloader.py
isort automated_downloader.py
flake8 automated_downloader.py
```

### Coverage Below 95%
- Add tests for uncovered code
- Check `htmlcov/index.html` to see which lines need coverage
- Use `pytest --cov-report=term-missing` to see missing lines

### Linting Failures
```bash
# Auto-fix formatting
black automated_downloader.py
isort automated_downloader.py

# Check what's wrong
flake8 automated_downloader.py --show-source
```

### Merge Conflicts
```bash
# Update your branch
git fetch origin main
git merge origin/main

# Resolve conflicts
# Then push
```

### Security Issues
```bash
# Check locally
pip install safety pip-audit bandit
safety check
pip-audit
bandit -r automated_downloader.py

# Update vulnerable packages
pip install --upgrade <package-name>
```

## Customizing Workflows

### Changing Coverage Threshold
Edit `.github/workflows/tests.yml`:
```yaml
pytest --cov-fail-under=90  # Change from 95 to 90
```

Also update:
- `pytest.ini` - `fail_under` setting
- `.coveragerc` - `fail_under` setting
- `README.md` - Documentation

### Adding More Platforms/Versions
Edit `.github/workflows/tests.yml`:
```yaml
matrix:
  os: [ubuntu-latest, windows-latest, macos-latest, macos-13]  # Add more
  python-version: ['3.8', '3.9', '3.10', '3.11', '3.12', '3.13']  # Add more
```

### Changing Security Scan Schedule
Edit `.github/workflows/security.yml`:
```yaml
schedule:
  - cron: '0 0 * * 1'  # Monday at 00:00 UTC
  # Change to daily: '0 0 * * *'
  # Change to monthly: '0 0 1 * *'
```

## Cost Considerations

GitHub Actions is free for public repositories with unlimited minutes.

For private repositories:
- **Free tier:** 2,000 minutes/month
- **Our usage per PR:** ~20-30 minutes (15 test jobs + linting + other workflows)
- **Estimated PRs per month:** ~60-100 PRs before hitting limit

**To reduce costs:**
1. Reduce test matrix (e.g., only test Python 3.11 on Windows/macOS)
2. Use `fail-fast: true` to stop on first failure
3. Cache dependencies aggressively
4. Only run full matrix on main branch, subset on PRs

## Best Practices

1. **Always run tests locally before pushing**
   ```bash
   pytest && flake8 automated_downloader.py && black --check automated_downloader.py
   ```

2. **Keep PRs small and focused**
   - Smaller PRs = faster CI runs
   - Easier to review
   - Less likely to have conflicts

3. **Update your branch regularly**
   - Prevents merge conflicts
   - Ensures compatibility with latest main

4. **Read the automated comments**
   - They provide valuable feedback
   - Show exactly what needs fixing

5. **Don't force-push after reviews**
   - Makes it hard to track changes
   - Breaks review comments

## Support

If you encounter issues with the workflows:

1. Check the [Actions](../../actions) tab for detailed logs
2. Review this documentation
3. Check [GitHub Actions documentation](https://docs.github.com/en/actions)
4. Open an issue if you think there's a bug in the workflow

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Branch Protection Rules](./BRANCH_PROTECTION.md)
- [Pull Request Template](./pull_request_template.md)
- [pytest Documentation](https://docs.pytest.org/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
