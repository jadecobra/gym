import diagrams
import diagrams.onprem.analytics
import diagrams.onprem.compute
import diagrams.onprem.database
import diagrams.onprem.inmemory
import diagrams.onprem.aggregator
import diagrams.onprem.monitoring
import diagrams.onprem.network
import diagrams.onprem.queue


def draw_on_premises_web_service():
    with diagrams.Diagram(
        'on_premises_example', show=False
    ):
        ingress = diagrams.onprem.network.Nginx('nginx_ingress')
        metrics = diagrams.onprem.monitoring.Prometheus('prometheus_metrics')
        metrics << diagrams.onprem.monitoring.Grafana('grafana_monitoring')

        with diagrams.Cluster('service_cluster'):
            compute_servers = [
                diagrams.onprem.compute.Server(f'server_{number}')
                for number in range(3)
            ]

        with diagrams.Cluster('cached_sessions'):
            primary = diagrams.onprem.inmemory.Redis('primary')
            primary - diagrams.onprem.inmemory.Redis('replica') << metrics
            compute_servers >> primary

        with diagrams.Cluster('database'):
            primary = diagrams.onprem.database.PostgreSQL('users')
            primary - diagrams.onprem.database.PostgreSQL('replica') << metrics
            compute_servers >> primary

        aggregator = diagrams.onprem.aggregator.Fluentd('logging')
        aggregator >> diagrams.onprem.queue.Kafka('stream') >> diagrams.onprem.analytics.Spark('analytics')

        ingress >> compute_servers >> aggregator

def draw_on_premises_web_service():
    with diagrams.Diagram(
        'on_premises_example_colored', show=False
    ):
        ingress = diagrams.onprem.network.Nginx('nginx_ingress')
        metrics = diagrams.onprem.monitoring.Prometheus('prometheus_metrics')
        metrics << diagrams.Edge(color='firebrick', style='dashed') << diagrams.onprem.monitoring.Grafana('grafana_monitoring')

        with diagrams.Cluster('service_cluster'):
            compute_servers = [
                diagrams.onprem.compute.Server(f'server_{number}')
                for number in range(3)
            ]

        with diagrams.Cluster('cached_sessions'):
            primary = diagrams.onprem.inmemory.Redis('primary')
            (
                primary
                - diagrams.Edge(color='brown', style='dashed')
                - diagrams.onprem.inmemory.Redis('replica')
                << diagrams.Edge(label='collect')
                << metrics
            )
            (
                compute_servers >>
                diagrams.Edge(color='brown') >>
                primary)

        with diagrams.Cluster('database'):
            primary = diagrams.onprem.database.PostgreSQL('users')
            primary - diagrams.onprem.database.PostgreSQL('replica') << metrics
            compute_servers >> primary

        aggregator = diagrams.onprem.aggregator.Fluentd('logging')
        aggregator >> diagrams.onprem.queue.Kafka('stream') >> diagrams.onprem.analytics.Spark('analytics')

        ingress >> compute_servers >> aggregator

draw_on_premises_web_service()
draw_on_premises_web_service_with_colors()