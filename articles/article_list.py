import json
import logging
import os
from decimal import Decimal
from botocore.exceptions import ClientError
from article_common import *

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def format_article_list_item(item, asset_url):
    article_id = int(item['timestamp'])
    hero_format = item.get('heroFormat', 'jpg')
    
    return {
        'id': article_id,
        'date': format_date(article_id),
        'interest': item.get('interest'),
        'heroImage': f"{asset_url}{article_id}/hero.{hero_format}",
        'summary': item.get('summary'),
        'title': item.get('title'),
        'topics': list(item.get('topics', []))
    }

def handle_article_list(event, table, asset_url):
    params = event.get('queryStringParameters') or {}
    try:
        page = int(params.get('page', 1))
    except (ValueError, TypeError) as e:
        # silently swallow bad page query value and set it to 1
        page = 1
    
    if page < 1: 
        page = 1
        
    page_size = 20
    
    try:
        # Scan the table to get all items since we don't have an index for sorting
        response = table.scan()
        items = response.get('Items', [])
        
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response.get('Items', []))
            
    except ClientError as e:
        logger.error(f"DynamoDB scan failed: {e}")
        return {'statusCode': 500, 'body': json.dumps({'message': 'Internal Error'})}
        
    if not items:
        return {'statusCode': 204, 'body': json.dumps({'message': 'No content'})}
        
    # Sort items by timestamp in descending order
    items.sort(key=lambda x: x.get('timestamp', 0), reverse=True)

    # Pagination
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    
    if start_index >= len(items):
        return {'statusCode': 404, 'body': json.dumps({'message': 'Article list not found'})}
        
    paginated_items = items[start_index:end_index]
    result = [format_article_list_item(item, asset_url) for item in paginated_items]
    
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(result, cls=DecimalEncoder)
    }

def lambda_handler(event, context):
    asset_url = get_asset_url()
        
    try:
        table = get_table()
        logger.info(table.table_status)
    except Exception as e:
        logger.error(f"DynamoDB table error: {str(e)}")
        table = None
        
    # Default to article list logic if not status
    if table is None:
            return {'statusCode': 404, 'body': json.dumps({'message': 'Article list not found'})}
    return handle_article_list(event, table, asset_url)