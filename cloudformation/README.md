# CloudFormation Templates

This directory contains AWS CloudFormation templates for infrastructure provisioning.

## When to Use CloudFormation vs Terraform

| Use CloudFormation When | Use Terraform When |
|------------------------|-------------------|
| AWS-only infrastructure | Multi-cloud or hybrid environments |
| Deep AWS service integration needed | Need provider ecosystem (GitHub, Datadog, etc.) |
| Using AWS-native tools (Service Catalog, StackSets) | Team already knows HCL |
| Compliance requires AWS-native IaC | Complex state management requirements |

## Files

- `example-stack.yaml` - Minimal example demonstrating CloudFormation structure

## Usage

### Deploy a Stack

```bash
# Deploy with default parameters
aws cloudformation deploy \
  --template-file cloudformation/example-stack.yaml \
  --stack-name my-app-dev \
  --parameter-overrides Environment=dev ProjectName=my-app

# Deploy with capabilities (required if creating IAM resources)
aws cloudformation deploy \
  --template-file cloudformation/example-stack.yaml \
  --stack-name my-app-dev \
  --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
  --parameter-overrides Environment=dev
```

### Validate Templates

```bash
# Validate syntax
aws cloudformation validate-template \
  --template-body file://cloudformation/example-stack.yaml

# Lint with cfn-lint (included in security scanner)
cfn-lint cloudformation/*.yaml
```

### Delete a Stack

```bash
aws cloudformation delete-stack --stack-name my-app-dev
```

## Extending the Template

Add resources by following AWS CloudFormation resource type syntax:

```yaml
Resources:
  MyLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub '${ProjectName}-${Environment}-handler'
      Runtime: python3.11
      Handler: index.handler
      # ... additional properties
```

See [AWS CloudFormation Resource Types](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html) for available resources.

## If You Don't Need CloudFormation

If your project uses Terraform exclusively:

1. Delete this `cloudformation/` directory
2. Remove CloudFormation references from the README
3. The security scanner will automatically skip CF scanning when no templates exist
