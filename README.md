# cointracker-assignment


Sample usage:

pip install -r requirements.txt
python ./archiver.py --address 0xd620AADaBaA20d2af700853C4504028cba7C3333

archiver.py will save the transactions ordered into subfolders organized by address and transaction category. Ex:
- ./transactions/0xd620AADaBaA20d2af700853C4504028cba7C3333/normal/transactions-22563621-22563713.csv
- ./transactions/0xd620AADaBaA20d2af700853C4504028cba7C3333/transfers/transactions-22563621-22563713.csv
