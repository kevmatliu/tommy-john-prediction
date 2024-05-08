from pathlib import Path

import scrapy
import json
from urllib.parse import urlencode

class InjurySpider(scrapy.Spider):
    name = "injury"
    prev = 0

    common_url = "https://www.prosportstransactions.com/baseball/Search/SearchResults.php"
    allowed_domains = ["prosportstransactions.com"]
    def start_requests(self):
        for i in range(0, 43750, 25): 
            params = {
                "Player": "",
                "Team": "",
                "BeginDate": "2008-01-01",
                "EndDate": "",
                "DLChkBx": "yes",
                "InjuriesChkBx": "yes",
                "submit": "Search",
                "start": i
            }
            url = f"{self.common_url}?{urlencode(params)}"
            yield scrapy.Request(url, callback=self.parse)
            
    def parse(self, response):
        for row in response.css("table.datatable tr"):
            if row.css("td:nth-child(1)::text").get() == "\xa0Date":
                continue
            yield {
                "date": row.css("td:nth-child(1)::text").get(),
                "team": row.css("td:nth-child(2)::text").get(),
                "acquired": row.css("td:nth-child(3)::text").get(),
                "relinquished": row.css("td:nth-child(4)::text").get(),
                "notes": row.css("td:nth-child(5)::text").get(),
                "url": response.url,
            }