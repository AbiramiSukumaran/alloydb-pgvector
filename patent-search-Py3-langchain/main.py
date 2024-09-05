import functions_framework


class settings:
    project_id = "<<PROJECT_ID>>"
    region = "us-central1"
    cluster_name = "<<CLUSTER_NAME>>"
    instance_name = "<<INSTANCE_NAME>>"
    database_name = "<<DB_NAME>>"
    user = "<<USER_NAME>>"
    password = "<<PASSWORD>>"


import json


from langchain_google_alloydb_pg import (
    AlloyDBEngine,
    AlloyDBLoader,
)


@functions_framework.http
def hello_http(request):
    request_json = request.get_json()
    search_text = request_json.get("search")
    query = f"""
    SELECT id || ' - ' || title as literature FROM patents_data ORDER BY abstract_embeddings <=> embedding('textembedding-gecko@003', '{search_text}')::vector LIMIT 10;
    """

    loader = AlloyDBLoader.create_sync(engine=getDbEngine(), query=query, format="JSON")

    documents = loader.load()
    ans = [{**json.loads(doc.page_content), **doc.metadata} for doc in documents]
    return json.dumps(ans)


def getDbEngine():
    engine = AlloyDBEngine.from_instance(
        project_id=settings.project_id,
        instance=settings.instance_name,
        region=settings.region,
        cluster=settings.cluster_name,
        database=settings.database_name,
        user=settings.user,
        password=settings.password,
    )
    return engine
