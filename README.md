# portfolio-github-example

An example of an actively developed project demonstrating modern software development practices including Infrastructure as Code (IaC), containerization, CI/CD pipelines, and automated security scanning.

## Purpose

This repository serves as a practical demonstration of:

- **Python Application Development** - Example scripts with testing and code quality tooling
- **Infrastructure as Code** - Both Terraform and CloudFormation examples for AWS resources
- **Containerization** - Docker configuration for portable deployments
- **CI/CD Pipelines** - GitHub Actions workflows for testing, building, and deploying
- **Security Scanning** - Automated SAST using [SDLC Code Scanner](https://github.com/williambrady/portfolio-code-scanner)
- **Pre-commit Hooks** - Automated code quality checks before commits

## Repository Structure

```text
.
├── scripts/              # Python application code
├── terraform/            # Terraform IaC configurations
├── cloudformation/       # CloudFormation templates
├── tests/                # Python test suite
├── .github/workflows/    # CI/CD pipeline definitions
├── Dockerfile            # Container build configuration
└── .pre-commit-config.yaml
```

## Security Scan Findings

This repository intentionally contains example Infrastructure as Code that triggers security scanner findings. These findings demonstrate the types of issues the SDLC Code Scanner detects in real-world codebases.

### Expected Findings

The security scan will report findings in the following categories:

| Category | Count | Severity | Explanation |
|----------|-------|----------|-------------|
| Terraform | ~19 | HIGH/MEDIUM | Example IaC using AES256 encryption instead of KMS, missing access logging, etc. |
| CloudFormation | ~5 | MEDIUM | Similar patterns in CFN templates |
| Python/Pylint | ~12 | LOW/INFO | Code style and convention findings in example scripts |

### Why These Findings Exist

These are **intentional for demonstration purposes**:

1. **Simplified Examples** - Production IaC would include KMS encryption, access logging, and VPC configurations that add complexity inappropriate for examples
2. **Scanner Demonstration** - Shows what the SDLC Code Scanner detects and how findings appear in GitHub Code Scanning
3. **Learning Opportunity** - Each finding includes remediation guidance that developers can learn from

### Viewing Findings

Once the initial content PR is merged, you can view findings in:
- **GitHub Code Scanning** - Security tab > Code scanning alerts
- **PR Comments** - Automated scan summary on pull requests
- **Workflow Artifacts** - Detailed JSON/HTML reports

## Related Projects

| Project | Description |
|---------|-------------|
| [portfolio-code-scanner](https://github.com/williambrady/portfolio-code-scanner) | The SDLC Code Scanner that performs security analysis |
| [portfolio-github-management](https://github.com/williambrady/portfolio-github-management) | Terraform management of this and other repositories |

## License

This project is licensed under the PolyForm Noncommercial License 1.0.0. For licensing inquiries, contact licensing@crofton.cloud.
