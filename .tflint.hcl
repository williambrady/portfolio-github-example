# TFLint configuration
# https://github.com/terraform-linters/tflint

config {
  # Call module type: "all" checks both local and remote modules
  call_module_type = "local"
}

# AWS plugin for AWS-specific rules
plugin "aws" {
  enabled = true
  version = "0.30.0"
  source  = "github.com/terraform-linters/tflint-ruleset-aws"
}

# Terraform plugin for general Terraform rules
plugin "terraform" {
  enabled = true
  preset  = "recommended"
}

# =============================================================================
# Rule configurations
# =============================================================================

# Naming conventions
rule "terraform_naming_convention" {
  enabled = true
}

# Require descriptions for variables and outputs
rule "terraform_documented_variables" {
  enabled = true
}

rule "terraform_documented_outputs" {
  enabled = true
}

# Standard module structure
rule "terraform_standard_module_structure" {
  enabled = true
}

# Workspace naming
rule "terraform_workspace_remote" {
  enabled = true
}
