# Using Standard Module Structure recommended from HashiCorp
https://developer.hashicorp.com/terraform/language/modules/develop/structure

# Learn Terraform - Provision an EKS Cluster
This repo is a companion repo to the [Provision an EKS Cluster tutorial](https://developer.hashicorp.com/terraform/tutorials/kubernetes/eks), containing
Terraform configuration files to provision an EKS cluster on AWS.
# How to provision AWS infrastructure
terraform init
terraform apply -auto-approve
# After provision has been completed.
# How to connect kubectl to EKS Cluster
cd webapp-terraform
aws eks --region $(terraform output -raw region) update-kubeconfig --name $(terraform output -raw cluster_name)