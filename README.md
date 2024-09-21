# Single Pod Kubernetes AZ Balancer

Single Pod Kubernetes AZ Balancer is a tool designed to automatically balance pod deployments which has only 1 replica across multiple Availability Zones (AZs) in a Kubernetes cluster. It comes in two flavors: a Mutating Admission Webhook and a Kubernetes Operator.

## Features

- Automatically distributes new scheduled single-pod deployment across available AZs
- Supports both webhook and operator implementations
- Easy to deploy and configure
- Helps maintain high availability and fault tolerance

## Webhook Implementation

The webhook implementation (`webhook.py`) is a Mutating Admission Webhook that intercepts pod creation requests and modifies them to ensure even distribution across AZs.

### How it works

1. When a new pod is created, the webhook intercepts the request.
2. It checks the current distribution of pods across AZs.
3. It selects the AZ with the lowest number of pods.
4. It modifies the pod specification to include a node selector for the chosen AZ.
5. The modified pod specification is then sent back to the Kubernetes API server.

## Operator Implementation

The operator implementation (in the `operator/` directory) is a Kubernetes Operator that watches for custom `AZBalancer` resources and balances specified deployments across AZs.

### How it works

1. The operator watches for `AZBalancer` custom resources.
2. When a new `AZBalancer` resource is created or updated, the operator:
   a. Checks the current distribution of pods across AZs.
   b. Selects the AZ with the lowest number of pods.
   c. Updates the specified deployment to use a node selector for the chosen AZ.
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
4. Create `AZBalancer` custom resources to balance specific deployments.

## Usage

### Webhook

Once deployed, the webhook will automatically intercept and modify pod creation requests. No additional action is required.

### Operator

Create an `AZBalancer` custom resource for each deployment you want to balance:

