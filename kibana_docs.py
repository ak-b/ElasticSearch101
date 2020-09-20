# domain name, or server's IP address, goes in the 'hosts' list
#elastic_client = ElasticSearch(hosts=["localhost"])
#Elasticsearch _search query in the form of a Python dictionary
search_param= {}
"""
The only two required parameters for the Search API in Python are 
1. Index you want to search,
2. Body of the Elasticsearch query 
"""
# User makes a request on client side
user_request = "some_param"

# dictionary structured like an Elasticsearch query:
query_body = {
  "query": {
    "bool": {
      "must": {
        "match": {      
          "some_field": user_request
        }
      }
    }
  }
}
#response = elastic_client.search(index="some_index", body=search_param)
#Results take the form of a nested dictionary– a dictionary made up of dictionaries.
#To access a key’s value, use ["hits"]["hits"]
#print ("query hits:", result["hits"]["hits"])

'''
MAKE ANOTHER CALL THAT RETURNS
MORE THAN 10 HITS BY USING THE 'size' PARAM
'''
#result = elastic_client.search(index="some_index", body=query_body, size=999)
#all_hits = result['hits']['hits']

# see how many "hits" it returned using the len() function
#print ("total hits using 'size' param:", len(result["hits"]["hits"]))

"""
Index — Database
Datatype — Type of the document
Id — Id of the document


# iterate the nested dictionaries inside the ["hits"]["hits"] list
for num, doc in enumerate(all_hits):
    print ("DOC ID:", doc["_id"], "--->", doc, type(doc), "\n")

    # Use 'iteritems()` instead of 'items()' if using Python 2
    for key, value in doc.items():
        print (key, "-->", value)

    # print a few spaces between each doc for readability
    print ("\n\n")

ELASTIC SEACRH QUERY
ElasticSearch is a great open-source search tool that’s built on Lucene (like SOLR) but is natively JSON + RESTful
More details can be found: https://wiki.cisco.com/display/AS13445/Elastic+Search

Throughout {endpoint} refers to the ElasticSearch index type (aka table). 
Note that ElasticSearch often let’s you run the same queries on both “indexes” (aka database) and types.
If you were just using ElasticSearch standalone,
An example of an endpoint would be: http://localhost:9200/gold-prices/monthly-price-table.
Key urls:
Query: {endpoint}/_search (in ElasticSearch < 0.19 this will return an error if visited without a query parameter)
Query example: {endpoint}/_search?size=5&pretty=true
Schema (Mapping): {endpoint}/_mapping
(ElasticSearch will converts dates to ISO 8601 format so you can search as 1900-01-01 to 1920-02-03).

There are two options for how a query is sent to the search endpoint:
1. Either as the value of a source query parameter e.g.:
 {endpoint}/_search?source={Query-as-JSON}
2. In the request body, e.g.:
 curl -XGET {endpoint}/_search -d 'Query-as-JSON'

 Queries are JSON objects with the following structure (each of the main sections has more detail below):
  {
        size: # number of results to return (defaults to 10)
        from: # offset into results (defaults to 0)
        fields: # list of document fields that should be returned - http://elasticsearch.org/guide/reference/api/search/fields.html
        sort: # define sort order - see http://elasticsearch.org/guide/reference/api/search/sort.html

        query: {
            # "query" object following the Query DSL: http://elasticsearch.org/guide/reference/query-dsl/
            # details below
        },

        facets: {
            # facets specifications
            # Facets provide summary information about a particular field or fields in the data
        }

        # special case for situations where you want to apply filter/query to results but *not* to facets
        filter: {
            # filter objects
            # a filter is a simple "filter" (query) on a specific field.
            # Simple means e.g. checking against a specific value or range of values
        },
    }
  Query results look like:
  {
    # some info about the query (which shards it used, how long it took etc)
    ...
    # the results
    hits: {
        total: # total number of matching documents
        hits: [
            # list of "hits" returned
            {
                _id: # id of document
                score: # the search index score
                _source: {
                    # document 'source' (i.e. the original JSON document you sent to the index
                }
            }
        ]
    }
    # facets if these were requested
    facets: {
        ...
    }
}
High performance equivalent using filters:
term: filter on a value for a field
range: filter for a field having a range of values (>=, <= etc)
geo_bbox: geo bounding box
geo_distance: geo distance

ElasticSeach, and hence the Data API, have a standard RESTful API. Thus:
POST      {endpoint}         : INSERT
PUT/POST  {endpoint}/  : UPDATE (or INSERT)
DELETE    {endpoint}/  : DELETE
if __name__ == '__main__':
	es = connect_elasticsearch()
	if es is not None:
        search_object = {'query': {'match': {'calories': '102'}}}
        search(es, 'recipes', json.dumps(search_object))
        """
