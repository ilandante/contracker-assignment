# cointracker-assignment


## Sample usage:

pip install -r requirements.txt
python ./archiver.py --address 0xd620AADaBaA20d2af700853C4504028cba7C3333

archiver.py will save the transactions ordered into subfolders organized by address and transaction category. Ex:
- ./transactions/0xd620AADaBaA20d2af700853C4504028cba7C3333/normal/transactions-22563621-22563713.csv
- ./transactions/0xd620AADaBaA20d2af700853C4504028cba7C3333/transfers/transactions-22563621-22563713.csv

## Arguments

I've set up the script to allow for some arguments:
--overwrite_csv: If set to True, will overwrite previously processed blocks
--start_block: block to start reading transactions from
--end_block: block to stop reading transactions from
--address: ETH address to use

Sample usage with arguments:
python ./archiver.py --address 0xd620AADaBaA20d2af700853C4504028cba7C3333
python ./archiver.py --overwrite_csv True --address 0xd620AADaBaA20d2af700853C4504028cba7C3333

These start/stop parameters allow this script to be used in AWS lambda or other multiprocessing architectures.
Some improvements could be made to manage multiprocessing within the script itself by using
"multiprocessing.pool import ThreadPool" or "from multiprocessing import Pool".

My Ethereum token is provided for the purposes of this POC, both as a default and as a .env.dev env var: 
CLIENT_ETH_TOKEN

This token can be updated and ideally, the final .env file should not be uploaded to any repo, but managed privately.
