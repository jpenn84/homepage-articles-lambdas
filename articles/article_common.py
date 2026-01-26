import json
import os
import boto3
import logging
from datetime import datetime
from decimal import Decimal

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_table():
    table = os.environ.get('table')
    if not table:
        raise ValueError("'table' environment variable is not set")

    logger.info(f"Initializing DynamoDB table: {table}")
    dynamodb = boto3.resource('dynamodb')
    return dynamodb.Table(table)

def format_date(timestamp):
    # Convert timestamp to human readable date
    # Using UTC to ensure consistency
    dt = datetime.utcfromtimestamp(timestamp)
    # %-d removes zero padding on Linux (Lambda environment)
    return dt.strftime('%-d %b %Y')

# Helper class to handle Decimal serialization if needed
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj)
        if isinstance(obj, set):
            return list(obj)
        return super(DecimalEncoder, self).default(obj)

def get_asset_url():
    url = os.environ.get('asset_url', '')
    if url and not url.endswith('/'):
        url += '/'
    return url