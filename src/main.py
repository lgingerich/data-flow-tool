import httpx
from datetime import datetime
from typing import Any, Dict, List, Union
from genson import SchemaBuilder

def fetch_data(url):
    try:
        response = httpx.get(url)
        response.raise_for_status()
        
        if 'application/json' in response.headers.get('content-type', ''):
            data = response.json()
        else:
            data = response.text
        
        return response, data
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None, None

def collect_metadata(response):
    return {
        "url": str(response.url),
        "status_code": response.status_code,
        "response_time": int(datetime.strptime(response.headers.get('date'), "%a, %d %b %Y %H:%M:%S %Z").timestamp() * 1000),
        "elapsed_time": int(response.elapsed.total_seconds() * 1000),
        "content_type": response.headers.get('content-type'),
        "encoding": response.encoding,
        "transfer_encoding": response.headers.get('transfer-encoding'),
        "content_encoding": response.headers.get('content-encoding'),
        "connection": response.headers.get('connection'),
        "age": response.headers.get('age'),
        "cache_control": response.headers.get('cache-control'),
        "strict_transport_security": response.headers.get('strict-transport-security'),
        "vary": response.headers.get('vary'),
        "x_matched_path": response.headers.get('x-matched-path'),
        "server": response.headers.get('server'),
    }

def infer_schema(data):
    builder = SchemaBuilder()
    builder.add_object(data)
    return builder.to_schema()

# Example usage
# url = "https://api.coingecko.com/api/v3/coins/ethereum/market_chart?vs_currency=usd&days=7&interval=daily"
# url = "https://api.llama.fi/v2/historicalChainTvl/arbitrum"
url = "https://l2beat.com/api/scaling/tvl"
# url = "https://api.github.com"
response, data = fetch_data(url)

if response and data:
    metadata = collect_metadata(response)
    schema = infer_schema(data)
    print("Metadata:", metadata)
    print("\nInferred Schema:", schema)
    print("\nData:", data)
else:
    print("Failed to fetch data")