<!-- PROJECT LOGO -->
# Log Query Interface 

## Log Ingestor API:    
The Log Ingestor API is responsible for efficiently handling vast volumes of log data sent in a specific format over HTTP. It ensures scalability to handle high log volumes, mitigates potential bottlenecks, and ingests logs via an HTTP server running on port 3000 by default.

Endpoint:

POST /ingest: Endpoint to ingest logs in bulk. Logs are sent in JSON format via HTTP POST requests.

## Query Interface API
The Query Interface API provides a user-friendly interface (Web UI or CLI) for searching logs using full-text search and specific field filters. It offers efficient and quick search results based on various log attributes.

Endpoints:

GET /search: Endpoint for full-text search across logs. Supports filters for level, message, resourceId, timestamp, traceId, spanId, commit, and metadata.parentResourceId.
Query Parameters:

The GET /search endpoint supports the following query parameters:
- q: Full-text search query.  
- level: Filter logs by log level.  
- message: Filter logs by log message.  
- resourceId: Filter logs by resource ID.   
- timestamp: Filter logs by timestamp.    
- traceId: Filter logs by trace ID.     
- spanId: Filter logs by span ID.     
- commit: Filter logs by commit hash.     
- metadata.parentResourceId: Filter logs by parent resource ID.     


### Built With

- Flask
- SQLLite
- HTML CSS



<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Prerequisites
- clone the Repository
- inside directory create and activate virtual environment
```
python -m venv env
```
- install following packages :    
```
pip install Flask
pip install Flask-RESTful
pip install db-sqlite3

```
- run the app by
```
flask --app logIngestor run -h localhost -p 3000
```



<!-- USAGE EXAMPLES -->
## Usage

- ingest the logs on `http://127.0.0.1:3000/ingest`     
- search the logs on `http://127.0.0.1:3000/`


<!-- CONTRIBUTING -->
## Features
- provides UI for filtering on multiple parameters    
- search between specific date ranges
- logs can be ingested in realtime 

## Snapshots

![Alt text](image.png)
![Alt text](image-1.png)



