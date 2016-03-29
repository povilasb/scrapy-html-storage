=====
About
=====

This is Scrapy downloader middleware that stores response HTMLs to disk.

Usage
=====

Turn downloader on, e.g. specifying it in `settings.py`::

    DOWNLOADER_MIDDLEWARES = {
        'scrapy_html_storage.HtmlStorageMiddleware': 10,
    }

None of responses by default are saved to disk.
You must select for which requests the response HTMLs will be saved::

       def parse(self, response):
        """Processes start urls.

        Args:
            response (HtmlResponse): scrapy HTML response object.
        """
        yield scrapy.Request(
            'http://target.com',
            callback=self.parse_target,
            meta={
              'save_html': True,
            }
        )

The file path where HTML will be stored is resolved with spider method
`response_html_path`. E.g.::

    class TargetSpider(scrapy.Spider):
        def response_html_path(self, request):
        """
        Args:
            request (scrapy.http.request.Request): request that produced the
                response.
        """
        return 'html/last_response.html'
