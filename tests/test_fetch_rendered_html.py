"""Tests for Playwright page snapshot race handling in downlink.cli."""

from unittest.mock import MagicMock, patch

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from downlink.cli import _page_content_with_retry, fetch_rendered_html


NAVIGATION_ERROR = PlaywrightError(
    "Page.content: Unable to retrieve content because the page is navigating and changing the content."
)


def test_page_content_retries_after_navigation_race():
    page = MagicMock()
    page.wait_for_load_state.return_value = None
    page.content.side_effect = [NAVIGATION_ERROR, "<html>ok</html>"]

    result = _page_content_with_retry(page, "https://example.com/article")

    assert result == "<html>ok</html>"
    assert page.content.call_count == 2
    page.wait_for_timeout.assert_called()


def test_page_content_returns_none_after_exhausted_retries():
    page = MagicMock()
    page.wait_for_load_state.return_value = None
    page.content.side_effect = NAVIGATION_ERROR

    result = _page_content_with_retry(page, "https://example.com/article", attempts=3)

    assert result is None
    assert page.content.call_count == 3


def test_page_content_falls_back_when_networkidle_times_out():
    page = MagicMock()

    def wait_for_load_state(state, timeout=None):
        if state == "networkidle":
            raise PlaywrightTimeoutError("networkidle timeout")
        return None

    page.wait_for_load_state.side_effect = wait_for_load_state
    page.content.return_value = "<html>settled</html>"

    result = _page_content_with_retry(page, "https://example.com/")

    assert result == "<html>settled</html>"
    states = [call.args[0] for call in page.wait_for_load_state.call_args_list]
    assert "networkidle" in states
    assert "load" in states


def test_fetch_rendered_html_waits_for_networkidle_before_content():
    fake_page = MagicMock()
    fake_browser = MagicMock()
    fake_context = MagicMock()
    fake_context.new_page.return_value = fake_page
    fake_browser.new_context.return_value = fake_context

    chromium = MagicMock()
    chromium.launch.return_value = fake_browser

    playwright_cm = MagicMock()
    playwright_cm.__enter__.return_value.chromium = chromium
    playwright_cm.__exit__.return_value = None

    fake_page.content.return_value = "<html><body>hi</body></html>"

    with patch("downlink.cli.sync_playwright", return_value=playwright_cm):
        result = fetch_rendered_html("https://example.com/", "TestAgent/1.0")

    assert result == "<html><body>hi</body></html>"
    fake_page.goto.assert_called_once_with(
        "https://example.com/", wait_until="domcontentloaded", timeout=10000
    )
    # Initial settle after goto uses networkidle.
    assert any(
        call.args and call.args[0] == "networkidle"
        for call in fake_page.wait_for_load_state.call_args_list
    )
    fake_browser.close.assert_called_once()


def test_fetch_rendered_html_does_not_raise_on_content_navigation_error():
    fake_page = MagicMock()
    fake_browser = MagicMock()
    fake_context = MagicMock()
    fake_context.new_page.return_value = fake_page
    fake_browser.new_context.return_value = fake_context

    chromium = MagicMock()
    chromium.launch.return_value = fake_browser

    playwright_cm = MagicMock()
    playwright_cm.__enter__.return_value.chromium = chromium
    playwright_cm.__exit__.return_value = None

    fake_page.content.side_effect = NAVIGATION_ERROR

    with patch("downlink.cli.sync_playwright", return_value=playwright_cm):
        result = fetch_rendered_html("https://example.com/redirecty", "TestAgent/1.0")

    assert result is None
    fake_browser.close.assert_called_once()
