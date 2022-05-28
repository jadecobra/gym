import diagrams
import diagrams.k8s.clusterconfig
import diagrams.k8s.compute
import diagrams.k8s.network
import diagrams.k8s.storage

def create_pods(count):
    return [
        diagrams.k8s.compute.Pod(name=f"pod{i}")
        for i in range(count)
    ]

def diagram_exposed_pods(count=3):
    with diagrams.Diagram(f'kubernetes_exposed_pods', show=False):
        diagrams.k8s.network.Ingress('domain.com') >> diagrams.k8s.network.Service('service') >> [
            diagrams.k8s.compute.Pod(f'pod{i}') for i in range(count)
        ] << diagrams.k8s.compute.ReplicaSet('replica_set') << diagrams.k8s.compute.Deployment('deployment') << diagrams.k8s.clusterconfig.HPA('hpa')

def diagram_stateful_architecture():
    with diagrams.Diagram('kubernetes_stateful_architecture', show=False):
        with diagrams.Cluster('Applications'):
            service = diagrams.k8s.network.Service('service')
            states = diagrams.k8s.compute.StatefulSet('stateful_set')

            applications = []
            for number in range(3):
                pod = diagrams.k8s.compute.Pod(f'pod{number}')
                pvc = diagrams.k8s.storage.PVC(f'pvc{number}')
                pod - states - pvc
                applications.append(service >> pod >> pvc)


        (
            applications
            << diagrams.k8s.storage.PV('pv')
            << diagrams.k8s.storage.StorageClass('storage_class')
        )

diagram_exposed_pods()
diagram_stateful_architecture()