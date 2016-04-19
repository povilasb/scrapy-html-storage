from hamcrest import assert_that, is_
from mock import MagicMock, patch, ANY
import pytest

from scrapy.settings import Settings

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
    downloader = HtmlStorageMiddleware(MagicMock())
    request_mock = make_request_mock(save_html=True)

    downloader.process_response(request_mock, MagicMock(), MagicMock())

    assert_that(write_to_file_mock.call_count, is_(1))


@patch('scrapy_html_storage.filesys.write_to_file')
def test_process_response_saves_response_html_to_file_resolved_by_spider(
        write_to_file_mock):
    downloader = HtmlStorageMiddleware(MagicMock())
    request_mock = make_request_mock(save_html=True)

    spider_mock = MagicMock()
    spider_mock.response_html_path.return_value = '/tmp/response.html'

    downloader.process_response(request_mock, MagicMock(), spider_mock)

    write_to_file_mock.assert_called_with('/tmp/response.html', ANY)


def test_from_settings_constructs_middleware_with_the_specified_settings():
    settings = Settings()
    settings.set('HTML_STORAGE', {'test': 'settings'})

    downloader = HtmlStorageMiddleware.from_settings(settings)

    assert_that(downloader.settings, is_({'test': 'settings'}))


def test_constructor_extracts_expected_settings():
    settings = Settings()
    settings.set('HTML_STORAGE', {'gzip_output': True})

    downloader = HtmlStorageMiddleware(settings)

    assert_that(downloader.gzip_output, is_(True))


def test_constructor_sets_empty_settings_when_middleware_settings_are_not_specified():
    settings = Settings()

    downloader = HtmlStorageMiddleware(settings)

    assert_that(downloader.settings, is_({}))


@pytest.mark.parametrize('setting_name,expected', [
    ('gzip_output', False),
])
def test_contructor_sets_default_settings_values_when_no_settings_are_specified(
        setting_name, expected):
    settings = Settings()
    settings.set('HTML_STORAGE', {})

    downloader = HtmlStorageMiddleware(settings)

    assert_that(downloader.__dict__[setting_name], is_(expected))
