from hamcrest import assert_that, is_
from mock import MagicMock, patch, ANY

from scrapy_html_storage import HtmlStorageMiddleware, should_save_html


def make_request_mock(save_html=False, query='', results_page=None):
    """Constructs HTTP Request mock object.
    """
    request_mock = MagicMock()
    request_mock.meta = {
        'save_html': save_html,
        'query': query,
        'results_page': results_page,
    }

    return request_mock


def test_should_save_html_returns_true_when_request_metainformation_has_special_key_set():
    request_mock = make_request_mock(save_html=True)

    save = should_save_html(request_mock)

    assert_that(save, is_(True))


@patch('scrapy_html_storage.filesys.write_to_file')
def test_process_response_stores_response_body_to_file_if_request_asks_for_it(
        write_to_file_mock):
    downloader = HtmlStorageMiddleware()
    request_mock = make_request_mock(save_html=True)

    downloader.process_response(request_mock, MagicMock(), MagicMock())

    assert_that(write_to_file_mock.call_count, is_(1))


@patch('scrapy_html_storage.filesys.write_to_file')
def test_process_response_saves_response_html_to_file_resolved_by_spider(
        write_to_file_mock):
    downloader = HtmlStorageMiddleware()
    request_mock = make_request_mock(save_html=True)

    spider_mock = MagicMock()
    spider_mock.response_html_path.return_value = '/tmp/response.html'

    downloader.process_response(request_mock, MagicMock(), spider_mock)

    write_to_file_mock.assert_called_with('/tmp/response.html', ANY)
