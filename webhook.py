from flask import Flask, request, jsonify
from kubernetes import client, config
import base64
import json
import os

app = Flask(__name__)

# Load Kubernetes configuration
config.load_incluster_config()
v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()

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

def is_single_replica_deployment(pod_name, namespace):
    try:
        deployment_name = "-".join(pod_name.split("-")[:-2])
        deployment = apps_v1.read_namespaced_deployment(deployment_name, namespace)
        return deployment.spec.replicas == 1
    except client.exceptions.ApiException:
        return False

@app.route('/mutate', methods=['POST'])
def mutate():
    request_info = request.json['request']
    
    # Check if the request is for a Pod
    if request_info['kind']['kind'] != 'Pod':
        return jsonify({"response": {"allowed": True}})

    pod_spec = request_info['object']['spec']
    pod_name = request_info['object']['metadata']['name']
    namespace = request_info['object']['metadata']['namespace']

    # Check if it's a new pod for a single-replica deployment
    if not is_single_replica_deployment(pod_name, namespace):
        return jsonify({"response": {"allowed": True}})

    az_distribution = get_pod_az_distribution()
    balanced_az = select_balanced_az(az_distribution)

    if balanced_az:
        if 'nodeSelector' in pod_spec:
            patch = [
                {
                    "op": "add",
                    "path": "/spec/nodeSelector/topology.kubernetes.io~1zone",
                    "value": balanced_az
                }
            ]
        else:
            patch = [
                {
                    "op": "add",
                    "path": "/spec/nodeSelector",
                    "value": {"topology.kubernetes.io/zone": balanced_az}
                }
            ]

        return jsonify({
            "response": {
                "allowed": True,
                "patchType": "JSONPatch",
                "patch": base64.b64encode(json.dumps(patch).encode()).decode()
            }
        })
    else:
        return jsonify({"response": {"allowed": True}})

if __name__ == '__main__':
    cert_path = os.environ.get('CERT_PATH', '/path/to/cert.pem')
    key_path = os.environ.get('KEY_PATH', '/path/to/key.pem')
    app.run(ssl_context=(cert_path, key_path), host='0.0.0.0', port=8443)