# alloydb-pgvector
## Use Case: Vector Search for Patents Data (using Embeddings for Text Data)
User wants to search for a specific text in patent literature stored in AlloyDB, meaning-driven, not just keyword-driven. The app data is stored in AlloyDB, uses pgvector extension for embeddings and Cosine Similarity for Vector Search. The app is deployed as a Cloud Function endpoint.

# What is AlloyDB ?
AlloyDB is a fully managed, PostgreSQL-compatible database service that offers enterprise-grade performance, availability, and scale. AlloyDB offers a number of features that make it a good choice for demanding transactional and analytical workloads, including:
### High performance: 
AlloyDB is designed to be highly performant for both transactional and analytical workloads. It uses a number of techniques to achieve this, including a shared-nothing architecture, columnar storage, and vectorized execution.
### High availability: 
AlloyDB offers a 99.99% uptime SLA, inclusive of maintenance. It uses a number of techniques to achieve this, including synchronous replication, automatic failover, and hot backups.
### Scale: 
AlloyDB can scale to meet the needs of even the most demanding applications. It can be scaled up to support up to 128 vCPUs and 1 TB of memory per instance, and it can be scaled out to support up to 100 instances per cluster.
### Security: 
AlloyDB is designed with security in mind. It uses a number of features to protect your data, including encryption, auditing, and access control.
### Compliance: 
AlloyDB is designed to meet the needs of organisations with demanding compliance requirements. It supports a number of compliance standards, including HIPAA, PCI DSS, and SOC 2.

# What is Cloud Function ?
Cloud Function is a lightweight compute solution for developers to create single-purpose, stand-alone functions that respond to Cloud events without needing to manage a server or runtime environment.

The above text is from: https://medium.com/google-cloud/connect-to-alloydb-for-postgresql-using-cloud-functions-9baef13ac5ca

# Demo Steps
1. Create the AlloyDB cluster, instance, database and table

CREATE TABLE patents_data ( 
    id VARCHAR(25),
    type VARCHAR(25),
    number VARCHAR(20),
    country VARCHAR(2),
    date VARCHAR(20),
    abstract VARCHAR(300000),
    title VARCHAR(100000),
    kind VARCHAR(5),
    num_claims BIGINT,
    filename VARCHAR(100),
    withdrawn BIGINT)  ;

2. Create Extensions:

   CREATE EXTENSION vector;

   CREATE EXTENSION google_ml_integration;

3. Grant Permission:
   
  GRANT EXECUTE
  ON
    FUNCTION embedding TO postgres;

4. Alter the table to add a Vector column for storing the Embeddings:

   alter table patents_data ADD column abstract_embeddings vector(768);

5. Insert DML:

   Refer to the file "insert_scripts.sql" in this repo

6. Grant Vertex AI User ROLE to the AlloyDB service account PRINCIPAL:

   You can do this from IAM on Google Cloud Console

7. Test if embedding function works on a test string:

  SELECT embedding( 'textembedding-gecko@001', 'AlloyDB is a managed, cloud-hosted SQL database service.');

8. Update the abstract_embeddings Vector field:

   update patents_data set abstract_embeddings = embedding( 'textembedding-gecko@001', abstract);

9. Query to check if Cosine Similarity works (Vector Search by Text):

  SELECT * FROM patents_data ORDER BY abstract_embeddings <=> embedding('textembedding-gecko@001', 'A new Natural Language Processing related Machine Learning Model')::vector LIMIT 10;

10. Create Cloud Functions, deploy and test it on the web!
