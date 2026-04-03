# CHANGES made in custom exception (using the sys module is a legacy approach)
# requirements.txt
# versions.py

###### docker build -t document-portal-system . (for running the image)
##### docker run -d -p 8093:8080 --name my-doc-portal document-portal-system (for running the container)
#
# for deployment, we will need 3 files ( aws.yaml write out the entire configuration, task definition template.#yml- configuration for the deployment)