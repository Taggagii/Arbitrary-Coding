import json

def change_matches(undesireable_urls):
    
    manifest = json.loads(open("manifest.json", "r").read())

    manifest["content_scripts"][0]["matches"] = undesireable_urls

    with open("manifest.json", "w") as f:
        f.write(json.dumps(manifest))

change_matches(["https://www.youtube.com/*"])