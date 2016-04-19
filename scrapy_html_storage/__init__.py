"""Downloader middlewares.
"""

import scrapy_html_storage.filesys as fs


class HtmlStorageMiddleware(object):
    """Scrapy downloader middleware that stores HTML files to local file system.
    """

    def __init__(self, settings):
        """
        Args:
            settings (scrapy.settings.Settings)
        """
        self.settings = settings.get('HTML_STORAGE', {})
        self.gzip_output = self.settings.get('gzip_output', False)


    @classmethod
    def from_settings(self, settings):
        """Contruct middleware with scrapy settings.

        Args:
            settings (scrapy.settings.Settings)

        Returns:
            HtmlStorageMiddleware:
        """
        return HtmlStorageMiddleware(settings)


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
            self._save_html_to(spider.response_html_path(request), response.body)

        return response


    def _save_html_to(self, path, html_body):
        """Store html to file.

        Optionally file will be gzipped.

        Args:
            str(path): file path to save html to. '.gz' suffix is appended
                in case of gzipping.
        """
        if self.gzip_output:
            fs.write_to_gzip(path + '.gz', html_body)
        else:
            fs.write_to_file(path, html_body)


def should_save_html(request):
    """
    Args:
        request (scrapy.http.request.Request)

    Returns:
        bool: True if this request should be stored to disk, False otherwise.
    """
    return 'save_html' in request.meta
