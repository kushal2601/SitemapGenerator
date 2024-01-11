import requests
import re

from SitemapHandler import add_url_to_sitemap

class HttpException(Exception):
    def __init__(self, status_code  , message):
        self.status_code = status_code
        self.message = message
    def __str__(self):
        return f"HTTP Exception: {self.status_code} - {self.message}"

def get_formatted_title_text(title):
    if not title:
        return ""

    formatting_list = [
        ("c#", "-csharp-"),
        ("C#", "-csharp-"),
        ("F#", "-fsharp-"),
        ("f#", "-fsharp-"),
        (".net", "-dotnet-"),
        (".Net", "-dotnet-"),
        (".NET", "-dotnet-"),
        ("/", "-or-"),
        ("&", "-and-"),
    ]

    current_title = title

    for item in formatting_list:
        current_title = re.sub(re.escape(item[0]), item[1], current_title, flags=re.IGNORECASE)

    current_title = re.sub(r'\+\+', '-plusplus-', current_title)
    current_title = re.sub(r'\$', '-usd-', current_title)

    return current_title

def get_formatted_location_text(location):
    if not location:
        return ""

    formatting_list = [
        ("/", "-or-"),
        ("&", "-and-"),
    ]

    current_location = location

    for item in formatting_list:
        current_location = re.sub(re.escape(item[0]), item[1], current_location)

    return current_location

def remove_special_characters(input_str):
    chars_to_remove = set('+,~:;=?@#|\'<>.^*()%!{"}_[]\\')
    result = ''.join(char for char in input_str if char not in chars_to_remove)
    return result

def get_formatted_indexingUrl(job):
    job_id = job['JobId']
    job_title = job['JobTitle']
    job_location = job['Location']
    regex_to_replace_space = r'[-\s]+'
    
    formatted_job_title = get_formatted_title_text(job_title)
    formatted_job_location = get_formatted_location_text(job_location)
    
    job_description_slug = f"{formatted_job_title}-{formatted_job_location}-{job_id}"
    slug_without_special_chars = remove_special_characters(job_description_slug)
    cleaned_slug = re.sub(regex_to_replace_space, "-", slug_without_special_chars)
    
    encoded_job_description_slug = cleaned_slug.lower().lstrip('-')
    formatted_indexing_url = indexingUrl_format.replace("{job_description_slug}", encoded_job_description_slug)
    
    return formatted_indexing_url


url = "https://es.goarya.com:9243/internalprofiles/jobs/_search"
indexingUrl_format = "https://mycareers.net/jobs/{job_description_slug}"
headers = {
    "Content-Type": "application/json"
}

data = {
    "size": 40,
    "track_total_hits": True,
    "_source": ["Title", "JobId", "Location","CreatedDate"],
    "query": {
        "bool": {
            "must": [
                {
                    "match": {
                        "Organization": "547088"
                    }
                },
                {
                    "match": {
                        "AryaJobStatus": "Open"
                    }
                }
            ]
        }
    },
    "sort": [
        {
            "CreatedDate": {
                "order": "desc"
            },
        }
    ]
}

total_jobs = 40
is_initial_hit = True
last_hit_id = None
urlIndex = 0

while total_jobs > 0 :
    try:
        if not is_initial_hit:
            data["search_after"] = last_hit_id
        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()

        if response.status_code != 200:
            raise HttpException(response_data["status"],response_data["error"]["caused_by"]["reason"])

        is_initial_hit = False
        #get all the hits
        hits = response_data["hits"]["hits"]
        
        if not hits:
            break
        
        for hit_info in hits:
            job_title = hit_info["_source"]["Title"]["Value"]
            job_location = hit_info["_source"]["Location"]
            job_created_date = hit_info["_source"]["CreatedDate"]
            job_id = hit_info["_source"]["JobId"]
            last_hit_id = hit_info["sort"]

            current_job = {
                "JobId" : job_id,
                "JobTitle" : job_title,
                "Location" : job_location
            }

            formatted_indexingUrl = get_formatted_indexingUrl(current_job)
            add_url_to_sitemap(formatted_indexingUrl, urlIndex)
            urlIndex += 1
    except Exception as e:
        print(e)