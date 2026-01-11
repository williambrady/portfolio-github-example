# Terraform Infrastructure

This directory contains Terraform configurations for provisioning AWS infrastructure for the portfolio application.

## Resources Provisioned

- **CloudWatch Log Group**: For application logging
- **S3 Bucket**: For data storage and log archival with lifecycle policies
- **IAM Role**: For application permissions with policies for CloudWatch and S3 access

## Prerequisites

- Terraform 1.0 or higher
- AWS CLI configured with appropriate credentials
- AWS account with permissions to create resources

## Usage

### Initialize Terraform

```bash
terraform init
```

### Review Planned Changes

```bash
terraform plan
```

### Apply Configuration

```bash
terraform apply
```

### Destroy Infrastructure

```bash
terraform destroy
```

## Configuration

### Variables

Key variables can be customized in `variables.tf` or passed via command line:

- `aws_region`: AWS region (default: us-east-1)
- `project_name`: Project name (default: portfolio-app)
- `environment`: Environment (dev/staging/prod, default: dev)
- `log_retention_days`: CloudWatch log retention (default: 30)

### Example: Override Variables

```bash
terraform apply -var="environment=prod" -var="project_name=my-app"
```

Or create a `terraform.tfvars` file:

```hcl
environment         = "prod"
project_name        = "my-app"
log_retention_days  = 90
```

## State Management

For production use, configure remote state storage:

1. Create an S3 bucket for state storage
2. Create a DynamoDB table for state locking
3. Uncomment and configure the backend block in `main.tf`

Example backend configuration:

```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state-bucket"
    key            = "portfolio/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}
```

## Outputs

After applying, Terraform will output:

- CloudWatch Log Group name and ARN
- S3 Bucket name and ARN
- IAM Role name and ARN

Use these outputs in your application configuration.

## Security Best Practices

- Store `terraform.tfvars` in `.gitignore` (already configured)
- Use AWS IAM roles instead of access keys when possible
- Enable S3 bucket encryption (already enabled)
- Enable S3 versioning (already enabled)
- Block public access to S3 buckets (already configured)
- Use Terraform remote state with encryption
- Review IAM policies for least privilege access

## Cost Considerations

The resources provisioned incur minimal costs:

- CloudWatch Logs: Charged per GB ingested and stored
- S3: Charged per GB stored, with lifecycle policies to reduce costs
- IAM: No charge

Estimate costs using the AWS Pricing Calculator before deploying to production.
