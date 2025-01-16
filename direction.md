So now we need a rss service that stores the articles in a in-memory database and add a analysis modal hosted llm inference service to access all the articles.

1. Create a RSS polling service that polls the rss feeds and stores the articles in a in-memory database.
2. Create a analysis modal hosted llm inference service to access all the articles. (Model: )
3. Create a message broker to send the articles to the llm inference service.(Use UUID to identify the articles)
4. Run tests for the RSS polling service and analysis modal hosted llm inference service.


So now we need a rss service that stores the articles in a in-memory database and add a analysis modal hosted llm inference service to access all the articles.

1. Create a RSS polling service that polls the rss feeds and stores the articles in a in-memory database.
2. Create a analysis modal hosted llm inference service to access all the articles. (Model: )
3. Create a message broker to send the articles to the llm inference service.(Use UUID to identify the articles)
    - Add a SSE endpoint to send the articles to the client.(/articles, /analysis, /stream)
        - /articles: Send the right amount of articles to the client based on their status code
        - /stream: Connect client to a stream subscription
        - /analysis: Send the analysis to the client
4. Create a configuration file (config.py) to store the configuration
    - Feed URL: https://ambcrypto.com/feed/
    - Model: g
    - Polling interval: 120 seconds
    - Redis host: localhost
    - Redis port: 6379
    - Redis password: 2025
    - Redis db: 0
    - (message broker)
    - Redis JSON datastructure
        - 
    - JSON datastructure for the analysis
5. Run test for RSS polling service and analysis modal hosted llm inference service.

6. Create a docker


RSS Polling
- Autocalling script
    - Fetch the articles from the feed
    - Parse the articles
    - Store the articles in the database
- Settings:
    - Feed URL
    - Polling interval
    - Redis host
    - Redis port
    - Redis password
    - Redis db
Modal
- ollama llm inference service
    - Q: Deployment On-demand or timeout?
    - Call the model with the articles
    - Update the articles with the analysis
- Settings:
    - Model
    - Redis host
    - Redis port
    - Redis password
    - Redis db
