import diagrams
import diagrams.aws.compute
import diagrams.aws.database
import diagrams.aws.network
import diagrams.aws.integration
import diagrams.aws.storage

def create_compute_instances(compute, name='compute',count=4):
    return [
        diagrams.aws.compute.__getattribute__(compute)(f'{name}_{number}') for number in range(count)
    ]

def diagram_grouped_workers():
    with diagrams.Diagram(
        'aws_grouped_workers',
        show=False,
        direction='TB'
    ):
        (
            diagrams.aws.network.ELB('load_balancer') >>
            create_compute_instances('EC2') >>
            diagrams.aws.database.RDS('database_layer')
        )


def diagram_clustered_web_services():
    with diagrams.Diagram(
        'aws_clustered_web_services',
        show=False,
        direction='LR',
    ):
        with diagrams.Cluster('web_services'):
            compute_layer = create_compute_instances('ECS')
        with diagrams.Cluster('database'):
            database_layer = diagrams.aws.database.RDS('user_database')
            database_layer - [diagrams.aws.database.RDS('user_database_replica')]

        (
            diagrams.aws.network.Route53('dns') >>
            diagrams.aws.network.ELB('load_balancer') >>
            compute_layer >>
            database_layer
        )

        compute_layer >> diagrams.aws.database.Elasticache('memcached')

def diagram_event_processing():
    with diagrams.Diagram(
        'aws_event_processing',
        show=False,
        direction='LR',
    ):
        source = create_compute_instances('EKS', count=1)[0]

        with diagrams.Cluster('Event Flows'):
            with diagrams.Cluster('Event Workers'):
                compute_layer = create_compute_instances('ECS')

            queue = diagrams.aws.integration.SQS('event_queue')

            with diagrams.Cluster('Processing'):
                handlers = create_compute_instances('Lambda')

        source >> compute_layer >> queue >> handlers >>  diagrams.aws.storage.S3('event_store')
        handlers >> diagrams.aws.database.Redshift('analytics')

diagram_grouped_workers()
diagram_clustered_web_services()
diagram_event_processing()