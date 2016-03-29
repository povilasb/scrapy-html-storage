"""Downloader middlewares.
"""

import scrapy_html_storage.filesys as fs


class HtmlStorageMiddleware(object):
    """Scrapy downloader middleware that stores HTML files to local file system.
    """
    def process_response(self, request, response, spider):
        """Stores response HTML body to file.

        Args:
            request (scrapy.http.request.Request): request which triggered
                this response.
            response (scrapy.http.Response)
            spider: (scrapy.Spider): spider that triggered the request.
                Spiders must set 'started_crawling' field to Unix timestamp.

        Returns:
            scrapy.http.response.Response: unmodified response object.
        """
        if should_save_html(request):
            save_to = spider.response_html_path(request)
            fs.write_to_file(save_to, response.body)

        return response


def should_save_html(request):
    """
    Args:
        request (scrapy.http.request.Request)

    Returns:
        bool: True if this request should be stored to disk, False otherwise.
    """
    return 'save_html' in request.meta
