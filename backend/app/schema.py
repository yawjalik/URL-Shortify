# Schema

from fastapi import Query
from pydantic import BaseModel
from typing import List

class Tags:
    tags_metadata = [
        {
            "name": "URL",
            "description": "Includes function that shorten URL"
        },
        {
            "name": "Getting stats",
            "description": "Include functions that returns statistics of URLs"
        },
        {
            "name": "Redirect",
            "description": "Enter url hash to redirect"
        }
    ]

class StandardResponse(BaseModel):
    message:str = Query(None, title="Message to return")

class ShortenResponseData(BaseModel):
    original_url:str = Query(..., title="Original URL")
    shortened_url:str = Query(..., title="Shortened URL")

class StatsResponseData(BaseModel):
    original_url:str = Query(..., title="Original URL")
    shortened_url:str = Query(..., title="Shortened URL")
    datetime_created:str = Query(..., title="URL datetime created")

class DetailedStatsResponseData(BaseModel):
    original_url:str = Query(..., title="Original URL")
    shortened_url:str = Query(..., title="Shortened URL")
    number_of_clicks:int = Query(..., title="Number of accesses to URL")
    datetime_created:str = Query(..., title="URL created datetime")
    datetime_accessed:List[str] = Query(..., title="List of URL accessed datetime")


class Schema:
    
    class ShortenRequest(BaseModel):
        url:str = Query(..., title="Input the URL to shorten", max_length=200)

        class Example:
            examples = {
                'example 1': {
                    'summary': 'YouTube website',
                    'description': 'Official website of YouTube',
                    'value': {
                        'url': 'https://www.youtube.com'
                    }
                }
            }
    
    class ShortenResponse(StandardResponse):
        data:ShortenResponseData = Query(None)

    class StatsResponse(StandardResponse):
        data:List[StatsResponseData] = Query(None)
    
    class StatsByHashResponse(StandardResponse):
        data:DetailedStatsResponseData = Query(None)

    class StatsByOriginalURLRequest(BaseModel):
        url:str = Query(..., title='Input the URL for getting stats')

        class Example:
            examples = {
                'example 1': {
                    'summary': 'YouTube website',
                    'description': 'Official website of YouTube',
                    'value': {
                        'url': 'https://www.youtube.com'
                    }
                }
            }
        
    class StatsByOriginalURLResponse(StandardResponse):
        data:DetailedStatsResponseData = Query(None)