from kubernetes import client, config
from .crd import AZBalancer

config.load_incluster_config()
v1 = client.CoreV1Api()

def get_pod_az_distribution():
    az_distribution = {}
    pods = v1.list_pod_for_all_namespaces().items
    for pod in pods:
        az = pod.spec.node_selector.get('topology.kubernetes.io/zone')
        if az:
            az_distribution[az] = az_distribution.get(az, 0) + 1
    return az_distribution

def select_balanced_az(az_distribution):
    if not az_distribution:
        return None
    min_az = min(az_distribution, key=az_distribution.get)
    return min_az

def handle_azbalancer_create(spec):
    az_balancer = AZBalancer(spec)
    az_distribution = get_pod_az_distribution()
    balanced_az = select_balanced_az(az_distribution)

    if balanced_az:
        patch = {
            "spec": {
                "template": {
                    "spec": {
                        "nodeSelector": {
                            "topology.kubernetes.io/zone": balanced_az
                        }
                    }
                }
            }
        }
        api = client.AppsV1Api()
        api.patch_namespaced_deployment(
            name=az_balancer.deployment_name,
            namespace=az_balancer.namespace,
            body=patch
        )
    return {"status": "created", "balanced_az": balanced_az}

def handle_azbalancer_update(spec):
    # Similar to create, but you might want to add additional logic for updates
    return handle_azbalancer_create(spec)