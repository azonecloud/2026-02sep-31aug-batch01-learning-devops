=================================================================================================
# STEPS TO BE FOLLOWED-Deploy SpringBoot Application along with POSTGRESDB
=================================================================================================
  # KUBECTL INSTALLATION
   $ curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
   $ sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# DOCKER BUILD 
 	git clone https://git-codecommit.us-east-2.amazonaws.com/v1/repos/dkr-ion-springboot-app-eks
	cd dkr-ion-springboot-app-eks
	mvn clean package
	mvn package -DskipTests=true
	mvn clean package -DskipTests=true -Dstart-class=com.example.postgresdemo.PostgresDemoApplication
	aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 932589472370.dkr.ecr.us-east-2.amazonaws.com
	docker build -t myapp .
	docker tag myapp:latest 932589472370.dkr.ecr.us-east-2.amazonaws.com/myapp:latest
	docker psuh 932589472370.dkr.ecr.us-east-2.amazonaws.com/myapp:latest

=================================================================================================
# Running Deployment files
=================================================================================================
# Encode USERNAME and PASSWORD of Postgres using following commands:
    $ echo -n "postgresadmin" | base64 && echo -n "admin123" | base64

# Create the Secret using kubectl apply:
	$ kubectl apply -f postgres-secrets.yaml

# Create Storage Class and describe it
	$ kubectl apply -f postgres-storage-class-aws.yaml
	$ kubectl get storageclass
	$ kubectl describe storageclass ebs-storage-class #AWS

# Create PersistentVolume(PV) and PersistentVolumeClaim(PVC) for Postgres using yaml file:
	$ kubectl apply -f postgres-storage-aws.yaml
	$ kubectl get pv
	$ kubectl describe pv postgres-pv-volume
	$ kubectl get pvc
	$ kubectl describe pvc postgres-pv-claim

# Deploying Postgres with kubectl apply:
	$ kubectl apply -f postgres-deployment.yaml
	$ kubectl get deploy
	$ kubectl get pods
	$ kubectl describe pod <<pod-name>>
	$ kubectl exec --stdin --tty <pod-reference> -- /bin/bash

	$ kubectl apply -f postgres-service.yaml
	$ kubectl get svc
	$ kubectl get svc postgres
	$ kubectl describe svc postgres

# Create a config map with the hostname of Postgres
$ kubectl create configmap hostname-config --from-literal=postgres_host=$(kubectl get svc postgres -o jsonpath="{.spec.clusterIP}")

# Deploy Spring Application:
	$ kubectl apply -f springboot-deployment.yaml
	$ kubectl get pods
	$ kubectl describe pod <<pod-name>>
	$ kubectl apply -f springboot-service.yaml
	$ kubectl get svc
	$ kubectl describe svc 

# To Get Services ,Secrets:
	$ kubectl get secrets
	$ kubectl get configmaps
	$ kubectl get pv
	$ kubectl get pvc
	$ kubectl get deploy
	$ kubectl get pods
	$ kubectl get svc

# For Database Connections
	$ kubectl get pods -l app=postgres
	$ kubectl logs my-pod
	$ kubectl exec --stdin --tty <pod-reference> -- /bin/bash
	$ psql -h localhost -U postgres    # Use when role assicoated with PostgresSQL Denies the request
																	 # [psql: FATAL:  role "root" does not exist]
# To Delete Pods , Volumes, Secrets, configmaps:
    kubectl delete secrets postgres-secrets
	kubectl delete storageclass ebs-storage-class
	kubectl delete pvc postgres-pv-claim
	kubectl delete pv postgres-pv-volume
	kubectl delete configmaps hostname-config
	kubectl delete deploy spring-boot-postgres-sample postgres
	kubectl delete svc spring-boot-postgres-sample postgres






























