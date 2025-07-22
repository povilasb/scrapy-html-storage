# About

A [Scrapy downloader middleware](https://docs.scrapy.org/en/latest/topics/downloader-middleware.html) that stores response HTMLs to disk.

## Usage

Turn downloader on, e.g. specifying it in `settings.py`:

```python
DOWNLOADER_MIDDLEWARES = {
    'scrapy_html_storage.HtmlStorageMiddleware': 10,
}
```

None of responses by default are saved to disk.
You must select for which requests the response HTMLs will be saved:

```python
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
```

The file path where HTML will be stored is resolved with spider method
`response_html_path`. E.g.:

```python
class TargetSpider(scrapy.Spider):
    def response_html_path(self, request):
        """
        Args:
            request (scrapy.http.request.Request): request that produced the
                response.
        """
        return 'html/last_response.html'
```

## Configuration

HTML storage downloader middleware supports such options:

* **gzip_output** (bool) - if True, HTML output will be stored in gzip format.
  Default is False.
* **save_html_on_status** (list) - if not empty, sets list of response codes
  whitelisted for html saving. If list is empty or not provided, all response
  codes will be allowed for html saving.

Sample:

```python
HTML_STORAGE = {
    "gzip_output": True,
    "save_html_on_status": [200, 202],
    "save_by_url" = [
        "https://website.com/index.html",
        ".*",
        "website.com/section-\w+.html", 
    ]
}
``` 