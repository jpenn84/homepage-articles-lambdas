# articles

This lambda serves json for the article list and article pages

## Requirements
These are the requirements for this lambda

### S3
- S3 URI: `s3Url` in .env file
- Object path: `baseUrl` in .env file

### Dynamo DB
- ARN: `ddbArn` in .env file

### Input from Dynamo DB
Exmple item:
```
{
  "timestamp": {
    "N": "1767718800"
  },
  "interest": {
    "S": "software_engineering"
  },
  "heroFormat": {
    "S": "jpg"
  },
  "summary": {
    "S": "I let an AI write about my experience letting an AI create my web page."
  },
  "title": {
    "S": "I Vibe-Coded My Home Page"
  },
  "topics": {
    "SS": [
      "AI",
      "Software"
    ]
  }
}
```

### Endpoints
There should be 2 endpoints:
- Article List - `articles?page={page}`
- Article Page - `article/{id}`

#### Article list:
Example response:
```
[
  {
      id: 1767718800,
      date: "6 Jan 2026"
      interest: "software_engineering",
      heroImage: "https://www.example.com/homepage-articles/1767718800/hero.jpg",
      summary: "An article about AI software engineering.",
      title: "Example Title AI Software",
      topics: ["AI", "Software"]
  }
]
```

Requirements:
- This should be an array of objects. Each object should have the following properties:
  - id: the numeric ID of the article
  - date: the date of the article
  - interest: the interest of the article
  - heroImage: the URL of the hero image
  - summary: a short summary of the article
  - title: the title of the article
  - topics: an array of topics related to the article
- Array should return 20 objects with pagination with page numbers.
- Results should be sorted by ID in descending order


#### Article Page:
Example response:
```
{
    id: 1767718800,
    content: "https://www.example.com/homepage-articles/1767718800/1767718800.html",
    date: "6 Jan 2026"
    interest: "software_engineering",
    heroImage: "https://www.example.com/homepage-articles/1767718800/hero.jpg",
    title: "Example Title AI Software",
    topics: ["AI", "Software"]
}
```
Requirements:
- This should be an object with the following properties:
  - id: the numeric ID of the article
  - content: the URL of the article inner HTML content
  - date: the date of the article
  - interest: the interest of the article
  - heroImage: the URL of the hero image
  - title: the title of the article
  - topics: an array of topics related to the article

### Data translation
This is how the data should be converted from Dynamo DB to the applicable json payload
- Article ID
  - input: `timestamp`
  - output: `id`

- Content inner HTML URL
  - creation: concatenate `$baseUrl` + `id` + "/" + `id` + ".html"
  - output: `content`

- Date
  - input: `timestamp`
  - translation: convert the timestamp to a human readable date that can be converted for a user's local time zone.
  - output: `date`

- Interest
  - input: `interest`
  - output: `interest`

- Hero image URL
  - creation:  concatenate "`$baseUrl` + `id` + "/hero." + `heroFormat`
  - output: `heroImage`

- Summary
  - input: `summary`
  - output: `summary`

- Title
  - input: `title`
  - output: `title`

- Topics
  - input: `topics`
  - output: `topics`

### Response codes and messages

Endpoint: Article List
1. Article list not found
    - Return a 404
    - Error Message: "Article list not found"

2. No Content
    - Endpoint: Article List
    - Return a 204
    - Message: "No content"

Endpoint: Article Page
1. Article Page not found
    - Return a 404
    - Error Message: "Article not found"

2. {id} URL param is not an integer
    - Return a 400
    - Error Message: "Invalid article ID"

