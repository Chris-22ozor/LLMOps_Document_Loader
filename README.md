# CHANGES made in custom exception (using the sys module is a legacy approach)
# requirements.txt
# versions.py

###### docker build -t document-portal-system . (for running the image)
##### docker run -d -p 8093:8080 --name my-doc-portal document-portal-system (for running the container)
#
# for deployment, we will need 3 files ( aws.yaml write out the entire configuration, task definition template.#yml- configuration for the deployment)
## aws.yml - it is tiggering the github action server
## task-definition - instruction for ECS
## template.yml - it is used for creating or automating the INFRA set up
## INFRA set up includes below: 
## ECR Repo, VPC( with 2 public subnets, internet gateway, ECS cluster, Task definition-FARGATE,
## ECS service- no load balancer, IAM role, security group)