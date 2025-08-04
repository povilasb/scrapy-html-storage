import re
import typing as t

from scrapy.http import Request, Response
from scrapy.settings import Settings
from scrapy.crawler import Crawler
from scrapy.spiders import Spider

import scrapy_html_storage.filesys as fs


class HtmlStorageMiddleware(object):
    """Scrapy downloader middleware that stores HTML files to local file system.
    """

    def __init__(self, settings: Settings):
        self.settings = settings.get('HTML_STORAGE', {})
        self.gzip_output = self.settings.get('gzip_output', False)
        self.save_html_on_codes = self.settings.get('save_html_on_codes', [])
        self._save_by_url = [re.compile(pattern) for pattern in self.settings.get('save_by_url', [])] 

    @classmethod
    def from_crawler(cls, crawler: Crawler) -> "HtmlStorageMiddleware":
        return cls(crawler.settings)


    def process_response(self, request: Request, response: Response, spider: Spider) -> Response:
        """Stores response HTML body to file."""
        if self._should_save_html(request, response):
            self._save_html_to(
                spider.response_html_path(request),  # type: ignore - it is not defined in Spider, but exists during the runtime.
                response.text,
            )

        return response


    def _save_html_to(self, path: str, html_body: str) -> None:
        """Store html to file.

        Optionally file will be gzipped.

        Args:
            str(path): file path to save html to.
        """
        if self.gzip_output:
            fs.write_to_gzip(path, html_body)
        else:
            fs.write_to_file(path, html_body)


    def _should_save_html(self, request: Request, response: Response) -> bool:
        """Check if this request should be stored to disk."""
        if not should_save_html_according_response_code(
            response.status,
            self.save_html_on_codes
        ):
            return False

        explicit_save_html = request.meta.get('save_html')
        if explicit_save_html is not None:
            return explicit_save_html

        for pattern in self._save_by_url:
            if pattern.match(request.url):
                return True

        return False




def should_save_html_according_response_code(code: int, allowed_list: t.List[int]) -> bool:
    """
    Args:
        code (int): response status code
        allowed_list (list): list of response status codes allowed to save html

    Returns:
        bool: True if allowed_list is empty (save all responses), or response
              code in allowed list.
    """
    return not allowed_list or code in allowed_list
