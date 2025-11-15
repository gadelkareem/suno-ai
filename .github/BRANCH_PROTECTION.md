# Branch Protection Rules

This document describes the recommended branch protection rules for this repository to ensure code quality and prevent accidental issues.

## Recommended Settings for `main` Branch

### Branch Protection Rules

Navigate to: **Settings → Branches → Add branch protection rule**

#### 1. Branch Name Pattern
```
main
```

#### 2. Protect Matching Branches

**✅ Require a pull request before merging**
- Required approvals: **1**
- ✅ Dismiss stale pull request approvals when new commits are pushed
- ✅ Require review from Code Owners (if CODEOWNERS file exists)

**✅ Require status checks to pass before merging**
- ✅ Require branches to be up to date before merging
- Required status checks:
  - `test (ubuntu-latest, 3.8)`
  - `test (ubuntu-latest, 3.9)`
  - `test (ubuntu-latest, 3.10)`
  - `test (ubuntu-latest, 3.11)`
  - `test (ubuntu-latest, 3.12)`
  - `test (windows-latest, 3.11)` (at minimum)
  - `test (macos-latest, 3.11)` (at minimum)
  - `lint`
  - `test-summary`
  - `merge-readiness`

**✅ Require conversation resolution before merging**
- All PR comments must be resolved

**✅ Require signed commits** (optional but recommended)

**✅ Require linear history** (optional, prevents merge commits)

**✅ Include administrators**
- Apply these rules to administrators too

**✅ Restrict who can push to matching branches** (optional)
- Add specific teams/users who can push

**❌ Allow force pushes** - Keep disabled
**❌ Allow deletions** - Keep disabled

## Additional Protection for `develop` Branch

If you use a `develop` branch, apply similar rules but you might want to:
- Reduce required approvals to 0 for faster iteration
- Still require all status checks to pass
- Allow more flexibility for experimental features

## Setting Up Required Status Checks

After enabling the GitHub Actions workflows, the following checks will be available:

### Test Checks
- `test (ubuntu-latest, 3.8)` through `test (ubuntu-latest, 3.12)`
- `test (windows-latest, 3.8)` through `test (windows-latest, 3.12)`
- `test (macos-latest, 3.8)` through `test (macos-latest, 3.12)`

You can require all of them or a subset. Recommended minimum:
- All Ubuntu tests (fastest, most common)
- At least one Windows test (Python 3.11)
- At least one macOS test (Python 3.11)

### Code Quality Checks
- `lint` - Ensures code quality (flake8, black, isort)
- `test-summary` - Overall test result summary

### Merge Readiness Checks
- `merge-readiness` - Checks for conflicts and branch updates

## How to Apply These Settings

1. Go to your repository on GitHub
2. Click **Settings** (requires admin access)
3. Click **Branches** in the left sidebar
4. Click **Add branch protection rule**
5. Enter `main` as the branch name pattern
6. Check all the boxes listed above
7. Select the required status checks
8. Click **Create** or **Save changes**

## Merge Strategies

Choose one of the following merge strategies (Settings → General → Pull Requests):

### Recommended: Squash and Merge
- ✅ **Allow squash merging**
  - Clean, linear history
  - All PR commits squashed into one
  - Easier to revert features

### Alternative: Rebase and Merge
- ✅ **Allow rebase merging**
  - Linear history
  - Preserves individual commits
  - Good for detailed history

### Not Recommended: Merge Commits
- ❌ **Allow merge commits**
  - Creates merge bubbles
  - Harder to read history
  - Only use if you need to preserve exact commit structure

## Auto-Delete Head Branches

- ✅ **Automatically delete head branches**
  - Keeps repository clean
  - Removes merged PR branches automatically

## Example `.github/CODEOWNERS` File

Create this file to automatically request reviews from specific people:

```
# Default owners for everything
* @your-github-username

# Specific owners for different parts
/tests/ @your-github-username
/.github/ @your-github-username
/automated_downloader.py @your-github-username
*.md @your-github-username
```

## Testing Branch Protection

After setting up branch protection:

1. Create a test branch
2. Make a small change
3. Open a PR
4. Try to merge without approval → Should fail
5. Try to merge with failing tests → Should fail
6. Get approval and pass tests → Should succeed

## Updating These Rules

As your project grows, you may want to:
- Add more required status checks
- Require more reviewers (increase to 2+)
- Add CODEOWNERS file
- Enable required signed commits
- Add custom status checks

## References

- [GitHub Docs - Branch Protection Rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub Docs - Required Status Checks](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches#require-status-checks-before-merging)
- [GitHub Docs - CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
