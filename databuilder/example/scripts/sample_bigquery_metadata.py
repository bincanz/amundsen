# Copyright Contributors to the Amundsen project.
# SPDX-License-Identifier: Apache-2.0

"""
This is a example script for extracting BigQuery usage results
"""

import logging
import os
import sqlite3

from pyhocon import ConfigFactory

from databuilder.extractor.bigquery_metadata_extractor import BigQueryMetadataExtractor
from databuilder.job.job import DefaultJob
from databuilder.loader.file_system_neo4j_csv_loader import FsNeo4jCSVLoader
from databuilder.publisher import neo4j_csv_publisher
from databuilder.publisher.neo4j_csv_publisher import Neo4jCsvPublisher
from databuilder.task.task import DefaultTask
from databuilder.task.neo4j_staleness_removal_task import Neo4jStalenessRemovalTask
from databuilder.transformer.base_transformer import NoopTransformer

logging.basicConfig(level=logging.INFO)

# set env NEO4J_HOST to override localhost
# NEO4J_ENDPOINT = f'bolt://{os.getenv("NEO4J_HOST", "localhost")}:7687' internal-a0bd1612994dd4d0abdda0fb85f43c13-441163252.us-west-2.elb.amazonaws.com
NEO4J_ENDPOINT = 'bolt://localhost:7687'
neo4j_endpoint = NEO4J_ENDPOINT

neo4j_user = 'neo4j'
neo4j_password = 'test'
DATE_TAG = '03-22-2022'

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception:
        logging.exception('exception')
    return None


# todo: Add a second model
# def create_bq_job(metadata_type, gcloud_project):
#     tmp_folder = f'/var/tmp/amundsen/{metadata_type}'
#     node_files_folder = f'{tmp_folder}/nodes'
#     relationship_files_folder = f'{tmp_folder}/relationships'
#
#     bq_meta_extractor = BigQueryMetadataExtractor()
#     csv_loader = FsNeo4jCSVLoader()
#
#     task = DefaultTask(extractor=bq_meta_extractor,
#                        loader=csv_loader,
#                        transformer=NoopTransformer())
#
#     job_config = ConfigFactory.from_dict({
#         f'extractor.bigquery_table_metadata.{BigQueryMetadataExtractor.PROJECT_ID_KEY}': gcloud_project,
#         f'loader.filesystem_csv_neo4j.{FsNeo4jCSVLoader.NODE_DIR_PATH}': node_files_folder,
#         f'loader.filesystem_csv_neo4j.{FsNeo4jCSVLoader.RELATION_DIR_PATH}': relationship_files_folder,
#         f'loader.filesystem_csv_neo4j.{FsNeo4jCSVLoader.SHOULD_DELETE_CREATED_DIR}': True,
#         f'publisher.neo4j.{neo4j_csv_publisher.NODE_FILES_DIR}': node_files_folder,
#         f'publisher.neo4j.{neo4j_csv_publisher.RELATION_FILES_DIR}': relationship_files_folder,
#         f'publisher.neo4j.{neo4j_csv_publisher.NEO4J_END_POINT_KEY}': neo4j_endpoint,
#         f'publisher.neo4j.{neo4j_csv_publisher.NEO4J_USER}': neo4j_user,
#         f'publisher.neo4j.{neo4j_csv_publisher.NEO4J_PASSWORD}': neo4j_password,
#         f'publisher.neo4j.{neo4j_csv_publisher.JOB_PUBLISH_TAG}': 'unique_tag',  # should use unique tag here like {ds}
#     })
#     job = DefaultJob(conf=job_config,
#                      task=task,
#                      publisher=Neo4jCsvPublisher())
#     return job

# todo: Add a second model
def create_bq_job(metadata_type, gcloud_project, label_filter=None):
    tmp_folder = f'/var/tmp/amundsen/{metadata_type}'
    node_files_folder = f'{tmp_folder}/nodes'
    relationship_files_folder = f'{tmp_folder}/relationships'
    bq_meta_extractor = BigQueryMetadataExtractor()
    csv_loader = FsNeo4jCSVLoader()
    job_config = ConfigFactory.from_dict({
        f'extractor.bigquery_table_metadata.{BigQueryMetadataExtractor.PROJECT_ID_KEY}': gcloud_project,
        f'loader.filesystem_csv_neo4j.{FsNeo4jCSVLoader.NODE_DIR_PATH}': node_files_folder,
        f'loader.filesystem_csv_neo4j.{FsNeo4jCSVLoader.RELATION_DIR_PATH}': relationship_files_folder,
        f'loader.filesystem_csv_neo4j.{FsNeo4jCSVLoader.SHOULD_DELETE_CREATED_DIR}': True,
        f'publisher.neo4j.{neo4j_csv_publisher.NODE_FILES_DIR}': node_files_folder,
        f'publisher.neo4j.{neo4j_csv_publisher.RELATION_FILES_DIR}': relationship_files_folder,
        f'publisher.neo4j.{neo4j_csv_publisher.NEO4J_END_POINT_KEY}': neo4j_endpoint,
        f'publisher.neo4j.{neo4j_csv_publisher.NEO4J_USER}': neo4j_user,
        f'publisher.neo4j.{neo4j_csv_publisher.NEO4J_PASSWORD}': neo4j_password,
        f'publisher.neo4j.{neo4j_csv_publisher.JOB_PUBLISH_TAG}': DATE_TAG,  # should use unique tag here like {ds}
    })
    if label_filter:
        job_config[
            'extractor.bigquery_table_metadata.{}'
            .format(BigQueryMetadataExtractor.FILTER_KEY)
            ] = label_filter
    task = DefaultTask(extractor=bq_meta_extractor,
                    loader=csv_loader,
                    transformer=NoopTransformer())
    job = DefaultJob(conf=job_config,
                    task=task,
                    publisher=Neo4jCsvPublisher())
    return job

def remove_job():
    task = Neo4jStalenessRemovalTask()
    job_config_dict = {
        'job.identifier': 'remove_stale_data_job',
        'task.remove_stale_data.neo4j_endpoint': neo4j_endpoint,
        'task.remove_stale_data.neo4j_user': neo4j_user,
        'task.remove_stale_data.neo4j_password': neo4j_password,
        'task.remove_stale_data.staleness_max_pct': 10,
        'task.remove_stale_data.target_nodes': ['Table'],
        'task.remove_stale_data.job_publish_tag': DATE_TAG,
        'task.remove_stale_data.retain_data_with_no_publisher_metadata': True,
        'task.remove_stale_data.dry_run': True
    }
    job_config = ConfigFactory.from_dict(job_config_dict)
    job = DefaultJob(conf=job_config, task=task)
    job.launch()

if __name__ == "__main__":
    # start table job
    # job1 = create_bq_job('bigquery_metadata', 'datateam-248616', 'hack')
    job1 = create_bq_job('bigquery_metadata', 'datateam-248616')

    # import job
    # job1 = create_bq_job('bigquery_metadata', 'spinnaker-dev-315722', 'filter:amundsen')
    job1.launch()

    # remove job
    # remove_job()
