# type: ignore

import sys
import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

# Add src to Python path so we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "data"))

# Import existing functions
from scraper import fetch_ebay_search_results
from data_cleaner import clean_pokemon_data
from data_to_csv import write_to_csv
from utils import load_links


def extract_task():
    """Wrapper for main scraping function"""
    links = load_links()

    try:
        result = fetch_ebay_search_results()
        print(f"Extraction completed: {result}")
        return result
    except Exception as e:
        print(f"Extraction failed: {e}")
        raise


def transform_task():
    """Clean the scraped data"""
    try:
        result = clean_pokemon_data()
        print(f"Cleaning completed: {result}")
        return result
    except Exception as e:
        print(f"Cleaning failed: {e}")
        raise


def load_task():
    """Save cleaned data to CSV"""
    try:
        result = write_to_csv()
        print(f"Loading completed: {result}")
        return result
    except Exception as e:
        print(f"Loading failed: {e}")
        raise


dag = DAG(
    dag_id="pokemon_etl_pipeline",
    start_date=datetime(2025, 6, 15),
    schedule_interval="0 2 * * *",
    catchup=False,
    default_args={"retries": 2, "retry_delay": timedelta(minutes=5)},
)

# Tasks
extract = PythonOperator(task_id="daily_scraper", python_callable=extract_task, dag=dag)


transform = PythonOperator(
    task_id="clean_pokemon_data", python_callable=transform_task, dag=dag
)

load = PythonOperator(task_id="save_to_csv", python_callable=load_task, dag=dag)

# Set dependencies
extract >> transform >> load
