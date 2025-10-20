# Security Best Practices Implementation
<!-- File: ~/code/ltphongssvn/5-day-ai-agents-intensive-google/SECURITY.md -->

## API Key Management

### Environment Variables Setup

This project requires API keys for AI services. **Never commit API keys to version control.**

**Required API Keys:**
- `OPENAI_API_KEY` - OpenAI API access
- `ANTHROPIC_API_KEY` - Claude API access
- `GOOGLE_API_KEY` - Google AI (Gemini) access

### Setup Instructions

1. **Copy the example file:**
   ```bash
   cp .env.example .env
   ```

2. **Add your API keys to `.env`:**
   ```bash
   OPENAI_API_KEY=sk-proj-...
   ANTHROPIC_API_KEY=sk-ant-...
   GOOGLE_API_KEY=AIza...
   ```

3. **Verify `.gitignore` protection:**
   ```bash
   grep "^\.env$" .gitignore
   ```

### Loading Environment Variables

The project uses `python-dotenv` to load API keys:

```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
```

## Secret Scanning (Recommended)

### Pre-commit Hook Setup

Install secret detection to prevent accidental commits:

```bash
pip install pre-commit detect-secrets
```

**Create `.pre-commit-config.yaml`:**
```yaml
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.5.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
        exclude: ^\.venv/|.*\.pyc$
```

**Activate protection:**
```bash
detect-secrets scan > .secrets.baseline
pre-commit install
```

**Manual scan:**
```bash
pre-commit run --all-files
```

## Dependency Security

### Regular Updates

Update dependencies to patch vulnerabilities:

```bash
pip install --upgrade openai anthropic google-generativeai
```

### Development Dependencies

Use optional dev dependencies for testing:

```bash
pip install -e ".[dev]"
```

## Code Security Best Practices

### 1. Never Hardcode Secrets
❌ **Wrong:**
```python
client = OpenAI(api_key="sk-proj-abc123...")
```

✅ **Correct:**
```python
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

### 2. Validate Environment Variables
```python
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not set")
```

### 3. API Key Rotation

If a key is exposed:
1. Revoke immediately via provider console
2. Generate new key
3. Update `.env` file
4. Restart all services

## File Exclusions

**Protected by `.gitignore`:**
- `.env` - API keys
- `.venv/` - Virtual environment
- `__pycache__/` - Python cache
- `*.pyc` - Compiled Python

## Team Guidelines

- **Never share `.env` files** via Slack, email, or commit
- **Use `.env.example`** for onboarding documentation
- **Run `pre-commit install`** after cloning repository
- **Rotate keys** if accidental exposure occurs
- **Use separate keys** for development and production

## Incident Response

If API keys are compromised:

1. **Immediate:** Revoke exposed keys via provider dashboards
    - OpenAI: https://platform.openai.com/api-keys
    - Anthropic: https://console.anthropic.com/settings/keys
    - Google: https://aistudio.google.com/app/apikey

2. **Generate:** Create new API keys

3. **Update:** Replace in `.env` file

4. **Notify:** Alert team members

5. **Review:** Check usage logs for unauthorized access

## Verification Checklist

- [ ] `.env` file exists and contains all required keys
- [ ] `.env` is in `.gitignore`
- [ ] No hardcoded API keys in code
- [ ] `python-dotenv` installed and used
- [ ] Pre-commit hooks installed (optional but recommended)
- [ ] Team members have separate API keys

## Support

For security concerns, contact the project maintainer privately via:
- GitHub: Open a security advisory (not a public issue)
- Email: [Project maintainer email]

**Last Updated:** October 19, 2025