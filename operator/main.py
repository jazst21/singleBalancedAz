import kopf
from az_balancer_operator.controller import handle_azbalancer_create, handle_azbalancer_update
from az_balancer_operator.crd import AZBalancer

@kopf.on.create('example.com', 'v1', 'azbalancers')
def create_fn(spec, **kwargs):
    return handle_azbalancer_create(spec)

@kopf.on.update('example.com', 'v1', 'azbalancers')
def update_fn(spec, **kwargs):
    return handle_azbalancer_update(spec)

if __name__ == "__main__":
    kopf.run()