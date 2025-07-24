import requests
import json
import csv
import os
import time
import pandas as pd

from typing import Dict, Optional, List
from io import StringIO
from sqlalchemy import create_engine
from dotenv import load_dotenv

class FIPSCountyETL:
    def __init__(self, config_path: str = "./config/fips_states.json", 
                 table_name: str = "ndh.fips_county"):
        self.config_path = config_path
        self.table_name = table_name
        self.fips_states = self.load_config() 

    def load_config(self) -> List[Dict]:
        try:
            with open(self.config_path, "r") as file:
                fips_states = json.load(file)
            
            return fips_states
        except Exception as e:
            print("Something went wrong loading the config:", e)
            raise

    def handle_request(self, url: str, max_retries: int = 3) -> Optional[requests.Response]:
        for attempt in range(max_retries):
            try:
                response = requests.get(url, timeout = 30) # important to note that we get responses back as .txt and not .json
                response.raise_for_status()

                return response
            except requests.RequestException as e:
                if attempt == max_retries - 1:
                    print(f"Failed to fetch after 3 attempts: {e}")
                    return None
                else:
                    sleep = 2 ** attempt
                    print(f"Attempt {attempt} failed so retrying in {sleep} seconds.")

                    time.sleep(sleep)
            except Exception as e:
                print("Something went wrong with handling a request:", e)
                raise
        return None

    def extract(self) -> str:
        raw_data = ""
        
        for state in self.fips_states:
            filename = f'st{state["code"]}_{state["abbrev"]}_cou2020.txt'
            url = f"https://www2.census.gov/geo/docs/reference/codes2020/cou/{filename}"
            
            response = self.handle_request(url)

            if not response:
                print(f"Skipping state {state['abbrev']} because request failed!")
                continue # should this be break or continue?
            
            # hack we need to do so that the headers for each file dont get added into the raw data 
            if not raw_data:
                raw_data = response.text
            else:
                raw_data += '\n'.join(response.text.split('\n')[1:])
        
        if not raw_data:
            print("Something went wrong during extraction and raw_data is empty.")
            raise
        
        print("Phase 1 - Extraction has finished")
        return raw_data

    def transform(self) -> pd.DataFrame:
        raw_data = self.extract()
        transform_data = []

        try:
            parsed_data = csv.DictReader(StringIO(raw_data), delimiter="|")
            
            for row in parsed_data:
                # row validation here? do we need tho since we know the type / format of data being fetched
                FIPS_row = {
                    "id": row["STATEFP"] + row["COUNTYFP"],
                    "name": row["COUNTYNAME"],
                    "fips_state_id": row["STATEFP"]
                }
                
                transform_data.append(FIPS_row)
                # print(f"Loaded {row["COUNTYNAME"]} successfully! \n")
        
        except Exception as e:
            print("Something went wrong during tranformation", e)
            raise
        
        df = pd.DataFrame(transform_data)
        # df.to_csv("output.csv", index=False)
        print("Phase 2 - Transformation has finished")

        return df

    def load(self):
        transformed_data = self.transform()
        
        load_dotenv("config/.env")
        
        connection_string = (
            f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
            f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        )

        engine = create_engine(connection_string)
        
        try:
            with engine.begin() as conn:
                transformed_data.to_sql(
                    name = self.table_name,
                    con = conn,
                    if_exists = "replace",
                    index = False,
                    method = "multi"
                )

            print(f"  Successfully loaded {len(transformed_data)} records to {self.table_name} table!")
            
        except Exception as e:
            print("Something went wrong loading the transformed data:", e)
            raise
        finally:
            engine.dispose()
            print("Phase 3 - Loading has finished")


    def run_pipeline(self):
        try:
            print("Starting FIPS County ETL pipeline!\n")
            self.load()
            print("\nPipeline completed successfully!")

        except Exception as e:
            print("Something went wrong with the pipeline:", e)
            raise

def main():
    pipeline = FIPSCountyETL()
    pipeline.run_pipeline()

if __name__ == "__main__":
    main()