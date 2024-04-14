from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "test"), encrypted=False)


def remove_nodes(tx):
    # result = tx.run("MATCH (n{key: 'bigquery://spinnaker-dev-315722'}) "
    #                 "WITH  [(x)<-[:SCHEMA]-(n) | x] as children "
    #                 "UNWIND children AS child "
    #                 "WITH child "
    #                 "WHERE NOT ( child.key IN [\"bigquery://spinnaker-dev-315722.dw_prod\", \"bigquery://spinnaker-dev-315722.dw_develop\"]) "
    #                 "MATCH (d {key: child.key}) "
    #                 "DETACH DELETE d")

    result = tx.run("MATCH (n{key: 'bigquery://datateam-248616'}) "
           "WITH  [(x)<-[:SCHEMA]-(n) | x] as children "
           "UNWIND children AS child "
           "WITH child "
           "WHERE NOT ( child.key IN [\"bigquery://datateam-248616.heap_hippo_builder_one_production\", "
                    "\"bigquery://datateam-248616.heap_lender_portal_production\", "
                    "\"bigquery://datateam-248616.heap_main_production\", "
                    "\"bigquery://datateam-248616.heap_customer_portal_production\", "
                    "\"bigquery://datateam-248616.heap_hbo_customer_flow_production\", "
                    "\"bigquery://datateam-248616.marketing_google_ads\", "
                    "\"bigquery://datateam-248616.marketing_microsoft_ads\", "
                    "\"bigquery://datateam-248616.heap_producer_portal_production\", "
                    "\"bigquery://datateam-248616.postgres_hhc_public\", "
                    "\"bigquery://datateam-248616.postgres_hbo_public\", "
                    "\"bigquery://datateam-248616.postgres_property_service_public\", "
                    "\"bigquery://datateam-248616.postgres_pod_prod_public\", "
                    "\"bigquery://datateam-248616.postgres_hbo_prod_public\", "
                    "\"bigquery://datateam-248616.postgres_gator_prod_public\", "
                    "\"bigquery://datateam-248616.postgres_billing_service_prod_public\", "
                    "\"bigquery://datateam-248616.salesforce_prod\", "
                    "\"bigquery://datateam-248616.sendgrid\", "
                    "\"bigquery://datateam-248616.postgres_smart_home_service_public\", "
                    "\"bigquery://datateam-248616.stripe_spinnaker\", "
                    "\"bigquery://datateam-248616.spinhouse_data\", "
                    "\"bigquery://datateam-248616.customer_io\", "
                    "\"bigquery://datateam-248616.datascience_production\", "
                    "\"bigquery://datateam-248616.dbt_marketing\", "
                    "\"bigquery://datateam-248616.dw_prod_intermediate\", "
                    "\"bigquery://datateam-248616.dw_prod_extracts\", "
                    "\"bigquery://datateam-248616.dw_prod\", "
                    "\"bigquery://datateam-248616.dw_prod_webapp\", "
                    "\"bigquery://datateam-248616.dw_prod_snapshots\", "
                    "\"bigquery://datateam-248616.dw_prod_lookup\"]) "
           # "MATCH (d {key: child.key}) "
           # "RETURN d.name LIMIT 25")

           "DETACH DELETE child")


with driver.session() as session:
    re = session.read_transaction(remove_nodes)
    for r in re:
        print(r + "\n")

driver.close()
