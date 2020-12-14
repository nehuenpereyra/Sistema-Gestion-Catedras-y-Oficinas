from flask import request, url_for

def url_for_page(url, page, **kwargs):
    args = {**request.args.copy(), **kwargs}
    args["page"] = page
    return url_for(url, **args)
