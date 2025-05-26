# Get transactions and export as CSV
# Source: aioetherscan code from https://github.com/ape364/aioetherscan?tab=readme-ov-file

import argparse
import asyncio
import csv
from dotenv import load_dotenv
import logging
import os

from aioetherscan import Client
from aiohttp_retry import ExponentialRetry
from asyncio_throttle import Throttler

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

CLIENT_ETH_TOKEN = os.getenv("CLIENT_ETH_TOKEN") or 'E1233XJWIF2ZQVZR6F1ER15ANVJXM13QTJ'


def main(start_block:int, end_block:int, overwrite_csv:bool, address:str):
    transaction_categories = ["normal", "internal", "transfers"]

    for category in transaction_categories:
        base_filename = f"transactions/{address}/{category}/transactions-{start_block}-{end_block}.csv"

        if not overwrite_csv and os.path.exists(base_filename):
            logger.info(f"Block has already been archived and script was set to not overwrite: {base_filename}")
        else:
            asyncio.run(process_transactions(start_block, end_block, transaction_category=category,
                                             base_filename=base_filename, address=address))


async def process_transactions(start_block:int, end_block:int, transaction_category:str, base_filename:str, address:str):
    throttler = Throttler(rate_limit=2, period=1.0)
    retry_options = ExponentialRetry(attempts=2)

    c = Client(CLIENT_ETH_TOKEN, throttler=throttler, retry_options=retry_options)

    transaction_wrapper_mapping = {
        "normal": c.extra.generators.normal_txs,
        "internal": c.extra.generators.internal_txs,
        "transfers": c.extra.generators.token_transfers,
    }

    transaction_generator_call = transaction_wrapper_mapping.get(transaction_category)

    transactions = []
    try:
        async for t in transaction_generator_call(
                address=address,
                start_block=start_block,
                end_block=end_block
        ):
            transactions.append(t)

    finally:
        await c.close()
        if not transactions:
            logger.info(f"No transactions found in block {start_block}-{end_block}")
        else:
            logger.info(f"Found {len(transactions)} transactions in block {start_block}-{end_block}. Writing to CSV.")
            save_to_csv(base_filename, transactions)


def save_to_csv(filename, transactions):
    fieldnames = list(transactions[0].keys())

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', newline='', encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(transactions)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Etherium transactions archiver. Retrieves Etherium transactions by block and stores them as CSV files.')
    parser.add_argument('--overwrite_csv', help='Overwrite csv files if they exist', default=False)
    parser.add_argument('--start_block', help='Start reading from this block', type=int, default=22563621)
    parser.add_argument('--end_block', help='Stop reading from this block (inclusive?)', type=int, default=22563713)
    parser.add_argument('--address', help='Eth address', type=str, default='0xd620AADaBaA20d2af700853C4504028cba7C3333')
    args = parser.parse_args()

    main(args.start_block, args.end_block, args.overwrite_csv, args.address)
