import diagrams
import diagrams.gcp.analytics
import diagrams.gcp.compute
import diagrams.gcp.database
import diagrams.gcp.iot
import diagrams.gcp.storage

with diagrams.Diagram(
    'gcp_message_collecting',
    show=False,
    direction='LR',
):
    pub_sub = diagrams.gcp.analytics.PubSub('pubsub')

    with diagrams.Cluster('Source of Data'):
        [
            diagrams.gcp.iot.IotCore(f'core_{number}')
            for number in range(3)
        ] >> pub_sub

    with diagrams.Cluster('Targets'):
        with diagrams.Cluster('Data Flow'):
            flow = diagrams.gcp.analytics.Dataflow('data flow')

        with diagrams.Cluster('Data Lake'):
            flow >> [diagrams.gcp.analytics.BigQuery('big_query'), diagrams.gcp.storage.GCS('storage')]

        with diagrams.Cluster('Event Driven'):
            with diagrams.Cluster('Processing'):
                flow >> diagrams.gcp.compute.AppEngine('engine') >> diagrams.gcp.database.BigTable('big_table')

            with diagrams.Cluster('Serverless'):
                flow >> diagrams.gcp.compute.Functions('functions') >> diagrams.gcp.compute.AppEngine('app_engine')

    pub_sub >> flow