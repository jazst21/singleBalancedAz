# Single Pod Kubernetes AZ Balancer

Single Pod Kubernetes AZ Balancer is a tool designed to automatically balance single-replica pod deployments across multiple Availability Zones (AZs) in a Kubernetes cluster. It comes in two flavors: a Mutating Admission Webhook and a Kubernetes Operator.

## Features

- Automatically distributes new single-replica deployments across available AZs
- Only affects deployments with exactly one replica
- Supports both webhook and operator implementations
- Easy to deploy and configure
- Helps maintain high availability and fault tolerance for single-pod deployments

## Webhook Implementation

The webhook implementation (`webhook.py`) is a Mutating Admission Webhook that intercepts pod creation requests for single-replica deployments and modifies them to ensure even distribution across AZs.

### How it works

1. When a new pod is created, the webhook intercepts the request.
2. It checks if the pod belongs to a deployment with exactly one replica.
3. If it's a single-replica deployment, it checks the current distribution of pods across AZs.
4. It selects the AZ with the lowest number of pods.
5. It modifies the pod specification to include a node selector for the chosen AZ.
6. The modified pod specification is then sent back to the Kubernetes API server.

## Operator Implementation

The operator implementation (in the `operator/` directory) is a Kubernetes Operator that watches for custom `AZBalancer` resources and balances specified single-replica deployments across AZs.

### How it works

1. The operator watches for `AZBalancer` custom resources.
2. When a new `AZBalancer` resource is created or updated, the operator:
   a. Checks if the specified deployment has exactly one replica.
   b. If it's a single-replica deployment, it checks the current distribution of pods across AZs.
   c. Selects the AZ with the lowest number of pods.
   d. Updates the specified deployment to use a node selector for the chosen AZ.
3. The operator continuously monitors and adjusts the deployment to maintain balance.

## Installation

### Webhook

1. Apply the necessary RBAC rules and create the TLS secret.
2. Deploy the webhook using the provided Kubernetes manifests.
3. Configure the `MutatingWebhookConfiguration` to intercept pod creation requests.

### Operator

1. Apply the Custom Resource Definition (CRD) and RBAC rules.
2. Build and push the operator Docker image.
3. Deploy the operator using the provided deployment YAML.
4. Create `AZBalancer` custom resources to balance specific single-replica deployments.

## Usage

### Webhook

Once deployed, the webhook will automatically intercept and modify pod creation requests for single-replica deployments. No additional action is required.

### Operator

Create an `AZBalancer` custom resource for each single-replica deployment you want to balance:


## Comparison: Mutating Admission Webhook vs Kubernetes Operator

| Feature | Mutating Admission Webhook | Kubernetes Operator |
|---------|----------------------------|---------------------|
| Scenario 1: New pod (replica=1) | Works well, as it intercepts the pod creation and modifies the placement in real-time. | Works, but adds overhead as it may require rescheduling the pod after creation. |
| Scenario 2: Scaled-down pod | May not work as scale-down events don't trigger the webhook (no new pod is created). | Works well, as it continuously monitors the state and can reschedule after scaling down. |
| Pod Scheduling Modification | Happens at the time of pod creation (one-time mutation). | Can continuously manage placement and reschedule if needed. |
| Complexity | Simpler to implement for specific, one-time changes. | More complex, but offers more long-term flexibility and lifecycle management. |

## Installation

### Webhook

1. Apply the necessary RBAC rules and create the TLS secret.
2. Deploy the webhook using the provided Kubernetes manifests.
3. Configure the `MutatingWebhookConfiguration` to intercept pod creation requests.

### Operator

1. Apply the Custom Resource Definition (CRD) and RBAC rules.
2. Build and push the operator Docker image.
3. Deploy the operator using the provided deployment YAML.
4. Create `AZBalancer` custom resources to balance specific single-replica deployments.

## Usage

### Webhook

Once deployed, the webhook will automatically intercept and modify pod creation requests for single-replica deployments. No additional action is required.

### Operator

Create an `AZBalancer` custom resource for each single-replica deployment you want to balance:

