import scrapy

# target database schema

# candidates = {
#     "seat": "P1",
#     "year": "2018",
#     "candidate_name": "ZAHIDI BIN ZAINUL ABIDIN",
#     "candidate_party": "UMNO",
#     "candidate_votes": 15032
# }

# elections = {
#     "seat": "P1",
#     "year": "2018",
#     "total_voters": 46095,
#     "total_votes": 36500
# }

# seats = {
#     "seat": "P1",
#     "seat_name": "Padang Besar",
#     "seat_state": "PERLIS"
# }

layout = [
    {
        "election": "GE14",
        "selector": ".chart.chart-3"
    },
    {
        "election": "GE13",
        "selector": ".chart.chart-2"
    },
    {
        "election": "GE12",
        "selector": ".chart.chart-1"
    },
    {
        "election": "GE11",
        "selector": ".chart.chart-0"
    }
]


class SeatSpider(scrapy.Spider):
    name = "seats"
    start_urls = ["https://undi.info/"]

    def parse(self, response):
        for chart in layout:
            chart_object = response.css(chart["selector"])
            for state_object in chart_object.css(".tab"):
                seat_state = state_object.css(
                    "label>table td>span::text").extract_first().strip()
                for seat_object in state_object.css(".seat-row"):
                    yield {
                        "election": chart["election"],
                        "seat_state": seat_state,
                        "seat_code": seat_object.css(
                            ".seat-code span::text").extract_first().strip(),
                        "seat_name": seat_object.css(
                            ".seat-name::text").extract_first().strip()
                    }
