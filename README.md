# Project instructions: https://1drv.ms/x/s!AjmFbdbExp7UhZx-dwOrL14mD8sOgw?e=rCoZKk
# How to provision AWS infrastructure
terraform init
terraform apply -auto-approve

# After provision has been completed.
# How to connect kubectl to EKS Cluster
cd webapp-terraform
aws eks --region $(terraform output -raw region) update-kubeconfig --name $(terraform output -raw cluster_name)

# webapp-python
    # 1. edit .env
AWS_ACCESS_KEY_ID= < your AWS access key id >
AWS_SECRET_ACCESS_KEY= < your AWS secret key >
AWS_REGION=ap- < your AWS region >

    # 2. build your image
 - cd ~/webapp-helm-terraform/webapp-python
 - docker build -t < dockerhub_user/webapp > .
 - docker push < dockerhub_user/webapp > 

# webapp-helm
    # 1. Create "webapp" namespace
-> kubectl create namespace webapp
    # 2. modifiy value.yaml
-> repository: to your repo on docker hub
-> tag: your tag image
    # 2. Install helm chart
- cd ~/webapp-helm-terraform
- helm install webapp ./webapp-helm
