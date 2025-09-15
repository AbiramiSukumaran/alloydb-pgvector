# Deploy Retail Shopping App via langchain

`main.py` contains the steps needed to deploy the patent search app:
https://codelabs.developers.google.com/patent-search-alloydb-gemini#2


## Command to deploy to GCF

```
# Replace placeholder variables, such as `<<PROJECT_ID>>`
gcloud functions deploy <<CLOUD_FUNCTION_NAME>> \
    --entry-point main.py \
    --runtime python312 \
    --trigger-http \
    --allow-unauthenticated

# Define endpoint
CLOUD_FUNCTIONS_ENDPOINT=https://us-central1-<<PROJECT_ID>>.cloudfunctions.net/<<CLOUD_FUNCTION_NAME>>
```

# Testing the endpoint

## To test via local server use gcf_deploy

```
venv312/bin/python debug_gcf.py

# For testing locally
CLOUD_FUNCTIONS_ENDPOINT=localhost:5000
```

## For testing on GCF hosted server

```
CLOUD_FUNCTIONS_ENDPOINT=<GCF_Endpoint>
```

## Call the API

```
curl -s -X POST \
  $CLOUD_FUNCTIONS_ENDPOINT \
  -H 'Content-Type: application/json' \
  -d '{"search": "A new Natural Language Processing related Machine Learning Model"}' \
  | jq .
```

## Demos

### 1. Locally hosted server
![Locally hosted server](https://raw.githubusercontent.com/vishwarajanand/alloydb-pgvector/main/patent-search-Py3-langchain/demo/demo-local.png?raw=true "Locally hosted server")

### 2. GCF hosted server
![GCF hosted server](https://raw.githubusercontent.com/vishwarajanand/alloydb-pgvector/main/patent-search-Py3-langchain/demo/demo-hosted.png?raw=true "GCF hosted server")

## Sql scripts

```
-- CREATE EXTENSION vector;
-- CREATE EXTENSION google_ml_integration;
-- GRANT EXECUTE ON FUNCTION embedding TO postgres;
-- CREATE TABLE patents_data ( id VARCHAR(25), type VARCHAR(25), number VARCHAR(20), country VARCHAR(2), date VARCHAR(20), abstract VARCHAR(300000), title VARCHAR(100000), kind VARCHAR(5), num_claims BIGINT, filename VARCHAR(100), withdrawn BIGINT) ;
-- ALTER TABLE patents_data ADD column abstract_embeddings vector(768);

-- INSERT SCRIPTS: https://github.com/AbiramiSukumaran/alloydb-pgvector/blob/main/insert_scripts.sql
-- insert into patents_data(id, type, number, country, date, abstract, title, kind, num_claims, filename, withdrawn) values('10326103','utility','10326103','US','6/18/2019','A display device includes a first substrate having a display area and a non-display area around the display area, a seal pattern in the non-display area and offset from the display area, and one or more buffer patterns between the seal pattern and the display area and having a viscosity of 5000 cps to 50000 cps.','Display device having buffer patterns','B2',15,'ipg190618.xml',0);

-- UPDATE patents_data set abstract_embeddings = embedding( 'textembedding-gecko@003', abstract);
SELECT id || ' - ' || title as literature FROM patents_data ORDER BY abstract_embeddings <=> embedding('textembedding-gecko@003', 'A new Natural Language Processing related Machine Learning Model')::vector LIMIT 10;
```
