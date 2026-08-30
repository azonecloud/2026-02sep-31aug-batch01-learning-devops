# Kubernetes Deployment Checklist

## Pre-Deployment Checklist

### Prerequisites
- [ ] Kubernetes cluster is running and accessible
- [ ] kubectl is installed and configured
- [ ] Docker is installed
- [ ] Maven 3.8+ is installed
- [ ] Git repository is clean (committed all changes)

### Configuration Review
- [ ] Review and update `k8s/02-configmap.yaml` for your environment
- [ ] Review and update `k8s/03-secret.yaml` with secure credentials
- [ ] Update `k8s/04-order-service-deployment.yaml` with correct Docker registry
- [ ] Verify Kafka broker address is correct
- [ ] Verify PostgreSQL configuration

### Build Phase
- [ ] Run `./deploy.sh build` to build application
- [ ] Run `./deploy.sh build-docker` to build Docker image
- [ ] Tag image: `docker tag order-service:latest ssadcloud/order-service:latest`
- [ ] Push to registry: `docker push ssadcloud/order-service:latest`
- [ ] Verify image is accessible in registry

## Deployment Phase

### Create Namespace and Secrets
- [ ] Run: `kubectl apply -f k8s/01-namespace.yaml`
- [ ] Run: `kubectl apply -f k8s/02-configmap.yaml`
- [ ] Run: `kubectl apply -f k8s/03-secret.yaml`
- [ ] Verify: `kubectl get configmap -n order-service`
- [ ] Verify: `kubectl get secret -n order-service`

### Deploy Application
- [ ] Run: `kubectl apply -f k8s/04-order-service-deployment.yaml`
- [ ] Wait for order-service to be ready (60-120 seconds)
- [ ] Verify: `kubectl get pods -n order-service -l app=order-service`
- [ ] Check logs: `kubectl logs -n order-service -l app=order-service`

### Enable Auto-Scaling
- [ ] Run: `kubectl apply -f k8s/05-hpa.yaml`
- [ ] Verify: `kubectl get hpa -n order-service`
- [ ] Monitor HPA: `kubectl get hpa -n order-service -w`

## Post-Deployment Verification

### Health Checks
- [ ] All pods are running: `kubectl get pods -n order-service`
- [ ] Database pod is ready: `kubectl wait --for=condition=ready pod -l app=postgres -n order-service`
- [ ] Application pods are ready: `kubectl wait --for=condition=ready pod -l app=order-service -n order-service`

### Connectivity Tests
- [ ] Run: `./deploy.sh port-forward` (in another terminal)
- [ ] Test: `curl http://localhost:8080/actuator/health`
- [ ] Expected: HTTP 200 with health status

### API Tests
- [ ] Create order: 
  ```bash
  curl -X POST http://localhost:8080/orders \
    -H "Content-Type: application/json" \
    -d '{"customerId": "01", "amount": 100.00}'
  ```
- [ ] Expected: HTTP 202 with order response
- [ ] Get order status: `curl http://localhost:8080/orders/{orderId}/status`
- [ ] Expected: HTTP 200 with status

### Metrics and Monitoring
- [ ] Check metrics: `curl http://localhost:8080/actuator/metrics`
- [ ] Check specific metric: `curl http://localhost:8080/actuator/metrics/jvm.memory.used`
- [ ] View logs: `./deploy.sh logs`

## Scaling Tests

### Test Horizontal Pod Autoscaler
- [ ] Current state: `kubectl get hpa -n order-service`
- [ ] Check current replicas: `kubectl get pods -n order-service -l app=order-service`
- [ ] Generate load (optional): `ab -n 1000 -c 10 http://localhost:8080/actuator/health`
- [ ] Monitor scaling: `kubectl get hpa -n order-service -w`
- [ ] Verify max replicas: Should not exceed 5
- [ ] Verify min replicas: Should not go below 2

## Production Readiness Checklist

### Storage and Persistence
- [ ] [ ] Implement PersistentVolumeClaim for PostgreSQL
- [ ] [ ] Configure backup strategy for database
- [ ] [ ] Test backup and restore procedures

### Security
- [ ] [ ] Use external secrets management (sealed-secrets/external-secrets)
- [ ] [ ] Implement RBAC (Role-Based Access Control)
- [ ] [ ] Configure network policies
- [ ] [ ] Scan Docker image for vulnerabilities
- [ ] [ ] Enable Pod Security Policies

### Monitoring and Logging
- [ ] [ ] Configure Prometheus scraping
- [ ] [ ] Set up Grafana dashboards
- [ ] [ ] Configure ELK stack or similar for logs
- [ ] [ ] Set up alerting rules
- [ ] [ ] Test alert notifications

### High Availability
- [ ] [ ] Configure Pod Disruption Budgets
- [ ] [ ] Set up backup cluster or multi-region deployment
- [ ] [ ] Test failover procedures
- [ ] [ ] Configure cross-region database replication

### Performance and Optimization
- [ ] [ ] Review and optimize resource requests/limits
- [ ] [ ] Performance test with production-like load
- [ ] [ ] Review and optimize Kafka configuration
- [ ] [ ] Implement caching if needed
- [ ] [ ] Review database indexes

## Rollback Procedure

If deployment fails or issues arise:

1. Check logs: `kubectl logs -n order-service deployment/order-service`
2. Describe pods: `kubectl describe pod -n order-service -l app=order-service`
3. Rollback deployment: `kubectl rollout undo deployment/order-service -n order-service`
4. Check rollout history: `kubectl rollout history deployment/order-service -n order-service`
5. Restore previous version: `kubectl rollout undo deployment/order-service -n order-service --to-revision=1`

## Cleanup (if needed)

```bash
# Delete all resources
./deploy.sh clean

# Or manually
kubectl delete namespace order-service
```

## Sign-Off

- [ ] Deployment completed successfully
- [ ] All health checks passed
- [ ] API tests passed
- [ ] Performance acceptable
- [ ] Ready for production traffic

Deployed by: _______________  
Date: _______________  
Version: _______________  
Notes: ________________________________________________________________

