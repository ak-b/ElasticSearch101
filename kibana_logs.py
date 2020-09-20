"""
This python script IS a ROUGH DRAFT to showcase the use case of extracting embryonic connection logs when
the PER-CLIENT HOST LIMIT is breached
Input: Start and End Date a.k.a TIMESTAMPS and GEOLOCATION a.k.a DC:SJC,DFW,YYZ,JFK,IAD,LHR,AMS,SIN,NRT,SYD
Output: Top 2 talkers with specification for 
(a)log source
(b)timestamp
(grouped) message : c,d,e,f
(c)source IP and port
(d)destination IP and port
(d)embryonic connection limit breached
(f)number of clients connected 
"""

import json,requests
from requests.auth import HTTPBasicAuth
import datetime
from datetime import datetime
import logging
import re
import tabulate
from tabulate import tabulate

def connect_elasticsearch():
    _es = None
    #_es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if _es.ping():
        print('Yay Connect')
    else:
        print('Awww it could not connect!')
    return _es


#PLACEHOLDER FOR _search
def search():
    """
    Add a geolocation map for CLP search URL
    Provide user input params for (A) timestamp (B) GEOLOCATION/DC
    """
    url = "https://clpsj-infra.webex.com/esapi/*-infra-*/_search"
    payload = "{\n  \"version\": true,\n  \"size\": 2,\n  \"sort\": [\n    {\n      \"@timestamp\": {\n        \"order\": \"desc\",\n        \"unmapped_type\": \"boolean\"\n      }\n    }\n  ],\n  \"_source\": {\n    \"excludes\": []\n  },\n  \"aggs\": {\n    \"2\": {\n      \"date_histogram\": {\n        \"field\": \"@timestamp\",\n        \"interval\": \"3h\",\n        \"time_zone\": \"UTC\",\n        \"min_doc_count\": 1\n      }\n    }\n  },\n  \"stored_fields\": [\n    \"*\"\n  ],\n  \"script_fields\": {},\n  \"docvalue_fields\": [\n    {\n      \"field\": \"@timestamp\",\n      \"format\": \"date_time\"\n    }\n  ],\n  \"query\": {\n    \"bool\": {\n      \"must\": [\n        {\n          \"query_string\": {\n            \"query\": \"\\\"Embryonic\\\"\",\n            \"analyze_wildcard\": true,\n            \"default_field\": \"*\"\n          }\n        },\n        {\n          \"range\": {\n            \"@timestamp\": {\n              \"gte\": 1599045724923,\n              \"lte\": 1599650524923,\n              \"format\": \"epoch_millis\"\n            }\n          }\n        }\n      ],\n      \"filter\": [],\n      \"should\": [],\n      \"must_not\": []\n    }\n  },\n  \"highlight\": {\n    \"pre_tags\": [\n      \"@kibana-highlighted-field@\"\n    ],\n    \"post_tags\": [\n      \"@/kibana-highlighted-field@\"\n    ],\n    \"fields\": {\n      \"*\": {}\n    },\n    \"fragment_size\": 2147483647\n  }\n}"
    headers = {
	  'Authorization': 'Basic YWtiYW5zYWw6TmV3c2Nvb3RlcjEyM0A=',
	  'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data = payload)
    results = json.loads(response.text)
    print(" Kibana Embryonic Connections Logs")
    for i in range(2):
	    result_a = results['hits']['hits'][i]['_source']['logsource']
	    result_b = results['hits']['hits'][i]['_source']['@timestamp']
	    result_c = results['hits']['hits'][i]['_source']['message']
	    result_x = results['hits']['hits'][i]['_source']['host']
	    client_perhost = str(re.findall(r"\S+\d+?[0]",result_c)[1])
	    srcip_port=str(re.findall(r"\S+\d+?[1]",result_c)[1])
	    destip_port= str(re.findall(r"\S+\d+?[3]",result_c)[1])
	    c= str(re.findall(r"-\d{0,3}",client_perhost)[0])
	    d= str(re.findall(r"\d+$", client_perhost)[0])
	    e= str(re.findall(r"^\d+.\d+.\d+.\d+",srcip_port)[0])
	    f= str(re.findall(r"\d+$",srcip_port)[0])
	    g= str(re.findall(r"^\d+.\d+.\d+.\d+",destip_port)[0])
	    h= str(re.findall(r"\d+$",destip_port)[0])
	    l = [["Logsource", result_a], ["Timestamp", result_b],["Host", result_x],["Clients", c],["Per-host Limit",d],["SrcIp",e],['SrcPort',f],["DestIp",g],['DestPort',h]]
	    table = tabulate(l, headers=['Entity', 'Value'], tablefmt='orgtbl')
	    print("Entry #{}".format(i+1))
	    print(table)
	    print("\n")

if __name__ == '__main__':
  logging.basicConfig(level=logging.ERROR)
  search()
