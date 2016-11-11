from hamcrest import assert_that, is_, has_properties
from mock import MagicMock, patch, ANY
import pytest

from scrapy.settings import Settings

from scrapy_html_storage import HtmlStorageMiddleware


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

def make_response_mock(response_status):
    """ Constructs HTTP Response mock object.
    """
    response_mock = MagicMock()
    response_mock.status = response_status

    return response_mock


def make_allowed_response_codes_list():
    return range(200, 300)


def make_downloader(save_html_on_codes=[]):
    settings = Settings()
    settings.set('HTML_STORAGE', {
        'gzip_output': True,
        'save_html_on_codes': save_html_on_codes
    })
    return HtmlStorageMiddleware(settings)


@pytest.mark.parametrize('response_status,as_expected', [
    (200, True),
    (299, True),
    (300, False),
    (404, False),
])
def test_should_save_html_returns_true_when_request_metainformation_has_special_key_set_and_appropriate_response_status(response_status, as_expected):
    request_mock = make_request_mock(save_html=True)
    response_mock = make_response_mock(response_status=response_status)
    downloader = make_downloader(make_allowed_response_codes_list())

    save = downloader._should_save_html(request_mock, response_mock)

    assert_that(save, is_(as_expected))


@pytest.mark.parametrize('response_status', [200, 299, 300, 404])
def test_should_save_html_returns_true_when_request_metainformation_has_special_key_set_and_allowed_resonse_codes_list_is_empty(response_status):
    request_mock = make_request_mock(save_html=True)
    response_mock = make_response_mock(response_status=response_status)
    downloader = make_downloader()

    save = downloader._should_save_html(request_mock, response_mock)

    assert_that(save, is_(True))


@patch('scrapy_html_storage.filesys.write_to_file')
def test_process_response_stores_response_body_to_file_if_request_asks_for_it(
        write_to_file_mock):
    downloader = HtmlStorageMiddleware(Settings())
    request_mock = make_request_mock(save_html=True)
    response_mock = make_response_mock(response_status=200)

    downloader.process_response(request_mock, response_mock, MagicMock())

    assert_that(write_to_file_mock.call_count, is_(1))


@patch('scrapy_html_storage.filesys.write_to_file')
def test_process_response_saves_response_html_to_file_resolved_by_spider(
        write_to_file_mock):
    downloader = HtmlStorageMiddleware(Settings())
    request_mock = make_request_mock(save_html=True)
    response_mock = make_response_mock(response_status=200)

    spider_mock = MagicMock()
    spider_mock.response_html_path.return_value = '/tmp/response.html'

    downloader.process_response(request_mock, response_mock, spider_mock)

    write_to_file_mock.assert_called_with('/tmp/response.html', ANY)


@patch('scrapy_html_storage.filesys.write_to_gzip')
def test_process_response_stores_response_body_to_gzip_file_if_this_setting_is_on(
        write_to_gzip_mock):
    downloader = HtmlStorageMiddleware(Settings())
    downloader.gzip_output = True
    request_mock = make_request_mock(save_html=True)
    response_mock = make_response_mock(response_status=200)

    downloader.process_response(request_mock, response_mock, MagicMock())

    assert_that(write_to_gzip_mock.call_count, is_(1))


def test_from_settings_constructs_middleware_with_the_specified_settings():
    settings = Settings()
    settings.set('HTML_STORAGE', {'test': 'settings'})

    downloader = HtmlStorageMiddleware.from_settings(settings)

    assert_that(downloader.settings, is_({'test': 'settings'}))


def test_constructor_extracts_expected_settings():
    settings = Settings()
    save_html_on_codes = make_allowed_response_codes_list()
    settings.set('HTML_STORAGE', {
        'gzip_output': True,
        'save_html_on_codes': save_html_on_codes
    })

    downloader = HtmlStorageMiddleware(settings)

    assert_that(downloader, has_properties(dict(
        gzip_output=True,
        save_html_on_codes=save_html_on_codes
    )))


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
