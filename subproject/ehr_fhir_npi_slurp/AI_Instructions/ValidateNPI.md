Validate NPI
=======================

In order to validate whether an NPI is valid or not, the npiregistry at 
has to be checked.. 

The logic to do this is already recorded in Step40_extract_csv_data.py

Because this process is slow, we have cached the results in ./prod_data/valid_npi_list.csv
This csv file has two columns, 'npi' and 'is_invalid' 
The two row values are either 'Invalid NPI' or 'Valid NPI'

Lets modify our Slupring ETL to use this file. 

There should be a class, that loads the current version of this file into an array, and then has a is_this_npi_valid function 

is_this_npi_valid should first see if the npi in the argument is present in its currenty map and then use 

url = f"https://npiregistry.cms.hhs.gov/api/?version=2.1&number={clean_npi}"

AS in Step40_extract_csv_data.py

When the NPI is not in the cache. Then the object should add the rvalidity result to the internal memory so that it gets further requests to validate this npi without using the API again. 

This class should have a destructor (__del__()) function, which saves all of the data that was added to the cache back to the csv file so that future runs of the ETL can remember the validity status of the NPI seen for the first time during the current ETL run.
