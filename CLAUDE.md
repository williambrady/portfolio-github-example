# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a GitHub template repository for portfolio projects following SDLC (Software Development Life Cycle) best practices. The repository is currently in its initial setup phase.

## Architecture

The codebase structure and architecture will be defined as the project develops. This section should be updated to reflect:

- Primary technology stack and frameworks
  - Terraform
  - CloudFormation
  - Python
  - Docker
- Project organization and module structure
  - / - Entry point for Docker
  - /terraform - Terraform configuration files
  - /cloudformation - CloudFormation templates
  - /scripts - Python application code
- Key architectural patterns and design decisions
  - Infrastructure as Code (IaC) with Terraform and/or CloudFormation
  - Python application code for data processing and analysis
  - Docker for containerization and portable execution
  - CI/CD pipelines for automated testing and deployment
  - Monitoring and logging for observability
- Data flow and component interactions
  - Data is processed and analyzed by the Python application
  - Results are stored in a persistent storage solution
    - Github Actions Logging
    - AWS Cloudwatch Log Group
    - AWS S3 Bucket
  - Monitoring and logging are implemented for observability

## Development Commands

### Docker Commands

```bash
# Build the Docker image
docker build -t portfolio-app .

# Run the container locally
docker run --rm portfolio-app

# Run with mounted volumes for development
docker run --rm -v $(pwd)/scripts:/app/scripts portfolio-app
```

### Python Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application locally
python scripts/main.py

# Run tests
pytest tests/

# Run a single test
pytest tests/test_name.py

# Linting
flake8 scripts/
pylint scripts/

# Formatting
black scripts/
isort scripts/
```

### Terraform Commands

```bash
# Initialize Terraform
cd terraform && terraform init

# Plan infrastructure changes
terraform plan

# Apply infrastructure changes
terraform apply

# Destroy infrastructure
terraform destroy

# Format Terraform files
terraform fmt -recursive

# Validate configuration
terraform validate
```

### CloudFormation Commands

```bash
# Validate template
aws cloudformation validate-template \
  --template-body file://cloudformation/example-stack.yaml

# Deploy stack
aws cloudformation deploy \
  --template-file cloudformation/example-stack.yaml \
  --stack-name my-app-dev \
  --parameter-overrides Environment=dev

# Delete stack
aws cloudformation delete-stack --stack-name my-app-dev

# Lint templates (via cfn-lint)
cfn-lint cloudformation/*.yaml
```

### Pre-commit Hooks

```bash
# Install hooks (run once after cloning)
pre-commit install

# Run all hooks manually
pre-commit run --all-files

# Run specific hook
pre-commit run black --all-files
pre-commit run terraform_fmt --all-files
pre-commit run cfn-lint --all-files

# Update hook versions
pre-commit autoupdate

# Skip hooks for a commit (use sparingly)
git commit --no-verify -m "message"
```

### Security Scanning

Security scanning is handled automatically via GitHub Actions using the [SDLC Code Scanner](https://github.com/williambrady/portfolio-code-scanner) action. The scan runs on:

- Every push to `main` or `develop` branches
- Every pull request to `main`
- Daily at 2 AM UTC (scheduled)
- Manual trigger via workflow_dispatch

For local scanning during development, you can use the SDLC Code Scanner Docker image directly:

```bash
# Pull the scanner image
docker pull ghcr.io/williambrady/portfolio-code-scanner:latest

# Run a local scan
docker run --rm \
  -v $(pwd):/repo:ro \
  -v $(pwd)/reports:/app/reports \
  ghcr.io/williambrady/portfolio-code-scanner:latest \
  scan-local --repo-path /repo --format json --format html
```

### CI/CD

- GitHub Actions workflows are located in `.github/workflows/`
- Workflows include:
  - `ci-cd.yml`: Build, test, and deploy pipeline
  - `terraform.yml`: Infrastructure validation and deployment
  - `sast.yml`: Security scanning (SAST/LINT)
- Infrastructure deployment is automated through Terraform
- Security scans run automatically on every push/PR and daily at 2 AM UTC

## Security Scanner

Security scanning uses the [SDLC Code Scanner](https://github.com/williambrady/portfolio-code-scanner) GitHub Action, which integrates 17+ security tools:

### Scanner Capabilities

**Terraform Scanning:**

- tfsec: Security-focused linting
- Checkov: Policy-as-code compliance
- Trivy: Vulnerability and misconfiguration detection
- TFLint: Terraform best practices
- Terraform validate: Syntax validation

**Python Scanning:**

- Bandit: Code security analysis (SQL injection, weak crypto, etc.)
- Safety: Dependency vulnerability detection

**Secrets Detection:**

- Gitleaks: Credentials and API key detection

**CloudFormation Scanning:**

- cfn-lint: Template validation
- cfn-nag: Security analysis
- Checkov: Policy compliance

**npm Scanning:**

- npm audit: Dependency vulnerabilities
- Snyk: Advanced vulnerability scanning (optional, requires token)

### Scanner Configuration

The scanner can be configured via inputs in `.github/workflows/sast.yml`:

- **scan-path**: Directory to scan (default: `.`)
- **output-formats**: Report formats (json, html, markdown, sarif)
- **fail-on-severity**: Fail threshold (CRITICAL, HIGH, MEDIUM, LOW, NONE)
- **config-path**: Path to custom config.yaml for advanced configuration

For custom rule exclusions or path exclusions, create a `config.yaml` file and reference it via the `config-path` input.

### Understanding Scan Results

- **CRITICAL/HIGH**: Must fix before merging
- **MEDIUM**: Should address soon
- **LOW/INFO**: Nice to have fixes

Scan results are:

- Uploaded as workflow artifacts
- Posted as PR comments (on pull requests)
- Integrated with GitHub Code Scanning via SARIF

See the [SDLC Code Scanner documentation](https://github.com/williambrady/portfolio-code-scanner) for comprehensive configuration options.

## Conventions

- **Pre-commit hooks must pass before pushing** - Run `pre-commit run --all-files` and fix any issues
- Python code follows PEP 8 style guidelines
- Use type hints in Python code
- Terraform code should be formatted with `terraform fmt`
- CloudFormation templates should pass `cfn-lint` validation
- All infrastructure changes must be made through IaC (Terraform or CloudFormation)
- Docker images should be built and tested in CI before deployment
- Security scans must pass (no CRITICAL/HIGH findings) before merging to main
- Document any security scan rule exclusions with justification
