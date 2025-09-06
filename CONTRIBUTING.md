# Contributing to FastAPI Vue Starter

Thank you for your interest in contributing to the FastAPI Vue Starter project! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Feature Requests](#feature-requests)

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

- Be respectful and inclusive
- Exercise consideration and empathy
- Focus on what is best for the community
- Use welcoming and inclusive language

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/fastapi-vue-starter.git`
3. Add upstream remote: `git remote add upstream https://github.com/original/fastapi-vue-starter.git`
4. Create a new branch: `git checkout -b feature/your-feature-name`

## Development Setup

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies

# Set up pre-commit hooks
pre-commit install
```

### Frontend Setup

```bash
cd frontend
npm install
npm run prepare  # Sets up husky hooks
```

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm run test

# End-to-end tests
npm run test:e2e
```

## Coding Standards

### Python (Backend)

- Follow PEP 8 style guide
- Use Black for code formatting
- Use isort for import sorting
- Maximum line length: 88 characters
- Use type hints for all functions
- Write docstrings for public functions and classes

```python
def create_user(db: Session, user_data: UserCreate) -> User:
    """Create a new user in the database.
    
    Args:
        db: Database session
        user_data: User creation data
        
    Returns:
        Created user instance
        
    Raises:
        ValueError: If email already exists
    """
    # Implementation...
```

### TypeScript/Vue (Frontend)

- Use TypeScript for all new code
- Follow Vue 3 Composition API patterns
- Use ESLint and Prettier for code formatting
- Prefer `const` over `let`, avoid `var`
- Use meaningful variable names
- Write JSDoc comments for complex functions

```typescript
/**
 * Authenticate user with email and password
 */
const login = async (credentials: LoginCredentials): Promise<AuthResponse> => {
  try {
    const response = await authAPI.login(credentials)
    // Handle response...
  } catch (error) {
    // Handle error...
  }
}
```

### CSS/Styling

- Use Tailwind CSS utility classes
- Create reusable component classes when needed
- Follow mobile-first responsive design
- Use semantic HTML elements
- Ensure accessibility (ARIA labels, keyboard navigation)

## Commit Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that don't affect code meaning (white-space, formatting)
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `perf`: Performance improvements
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to build process or auxiliary tools

### Examples

```bash
feat(auth): add magic link authentication
fix(api): handle null user in profile endpoint
docs: update deployment guide
style(frontend): format login component
test(auth): add unit tests for user service
```

## Pull Request Process

1. **Update your branch**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Ensure tests pass**
   ```bash
   # Backend
   cd backend && pytest
   
   # Frontend
   cd frontend && npm run test
   
   # Linting
   npm run lint
   ```

3. **Update documentation**
   - Update README.md if needed
   - Add/update docstrings and comments
   - Update API documentation if endpoints changed

4. **Create pull request**
   - Use a clear, descriptive title
   - Reference related issues (`Fixes #123`)
   - Describe what changes were made and why
   - Include screenshots for UI changes
   - Mark as draft if not ready for review

5. **Pull Request Template**
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update
   
   ## Testing
   - [ ] Unit tests pass
   - [ ] Integration tests pass
   - [ ] Manual testing completed
   
   ## Checklist
   - [ ] Code follows project style guidelines
   - [ ] Self-review completed
   - [ ] Comments added for hard-to-understand areas
   - [ ] Documentation updated
   - [ ] No new warnings introduced
   ```

## Issue Reporting

### Bug Reports

When filing bug reports, please include:

1. **Environment information**
   - OS and version
   - Python version (backend)
   - Node.js version (frontend)
   - Browser and version (frontend issues)

2. **Steps to reproduce**
   - Detailed steps to reproduce the issue
   - Expected behavior
   - Actual behavior
   - Screenshots or error messages

3. **Code samples**
   - Minimal code example that reproduces the issue
   - Configuration files if relevant

### Bug Report Template

```markdown
**Environment:**
- OS: [e.g., Ubuntu 20.04, Windows 10, macOS 12]
- Python: [e.g., 3.11.0]
- Node.js: [e.g., 18.12.0]
- Browser: [e.g., Chrome 108, Firefox 107]

**Bug Description:**
A clear and concise description of the bug.

**Steps to Reproduce:**
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

**Expected Behavior:**
A clear description of what you expected to happen.

**Actual Behavior:**
A clear description of what actually happened.

**Screenshots:**
If applicable, add screenshots to help explain your problem.

**Additional Context:**
Add any other context about the problem here.
```

## Feature Requests

Feature requests are welcome! Please provide:

1. **Use case description**
   - What problem does this solve?
   - Who would benefit from this feature?
   - How would you use this feature?

2. **Proposed solution**
   - Describe your preferred solution
   - Consider alternative approaches
   - Think about potential drawbacks

3. **Implementation considerations**
   - Would this be a breaking change?
   - What parts of the system would be affected?
   - Are there any dependencies needed?

## Development Workflow

1. **Before starting work**
   - Check if an issue exists for your feature/bug
   - Comment on the issue to let others know you're working on it
   - Get approval from maintainers for large features

2. **During development**
   - Make small, focused commits
   - Write tests for new functionality
   - Update documentation as you go
   - Run tests frequently

3. **Before submitting**
   - Rebase your branch on latest main
   - Squash related commits if appropriate
   - Ensure all tests pass
   - Verify no linting errors exist

## Code Review Process

1. **Automatic checks**
   - CI/CD pipeline must pass
   - Code coverage should not decrease significantly
   - No linting errors or warnings

2. **Manual review**
   - At least one maintainer review required
   - Address all feedback before merging
   - Re-request review after making changes

3. **Merge process**
   - Maintainers will merge approved PRs
   - Use "Squash and merge" for feature branches
   - Use "Merge commit" for version releases

## Getting Help

- **Documentation**: Check README.md and docs/
- **Issues**: Search existing issues before creating new ones
- **Discussions**: Use GitHub Discussions for questions
- **Discord**: Join our community Discord server (link in README)

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- GitHub contributors page
- Release notes for significant contributions

Thank you for contributing to FastAPI Vue Starter! 🚀