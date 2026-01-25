# articles

This lambda serves json for the article list and article pages. It takes data from a DynamoDB and translates it for 2 endpoints:
- Article List - A 20-object paginated list of articles
- Article Page - The individual article page data

The output contains article metadata and points to S3 URLs 

Additionally, there is a Status endpoint for basic health checks.

## Requirements
See [requirements.md](requirements.md) for software requirements.

## Environmental variables
- S3 URI: `s3Url` in .env file
- Object path: `baseUrl` in .env file
- ARN: `ddbArn` in .env file
