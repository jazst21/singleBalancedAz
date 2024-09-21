class AZBalancer:
    def __init__(self, spec):
        self.deployment_name = spec.get('deploymentName')
        self.namespace = spec.get('namespace', 'default')