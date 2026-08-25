#!/usr/bin/env python3
# This is the original Playwright-based implementation adapted as a package entry point.
# pip install playwright markdownify
# python -m playwright install

import os
import argparse
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from markdownify import markdownify as md
from markdownify import MarkdownConverter

DEFAULT_USER_AGENT = """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"""

class SpacePreservingConverter(MarkdownConverter):
    """Drop hyperlinks while ensuring words don't run together."""
    
    def convert_a(self, el, text, *args, **kwargs):
        return f" {text}" if text else ""

    def convert_img(self, el, text, *args, **kwargs):
        return " "

    def convert_br(self, el, text, *args, **kwargs):
        return "  \n"

def _page_content_with_retry(page, url: str, attempts: int = 3) -> str:
    """Snapshot page HTML, retrying if the page is still navigating."""
    last_error = None
    for attempt in range(attempts):
        try:
            # Prefer a settled document before reading content. networkidle can
            # hang on long-polling sites, so fall back to load/domcontentloaded.
            try:
                page.wait_for_load_state("networkidle", timeout=5000)
            except PlaywrightTimeoutError:
                try:
                    page.wait_for_load_state("load", timeout=3000)
                except PlaywrightTimeoutError:
                    page.wait_for_load_state("domcontentloaded", timeout=2000)
            return page.content()
        except PlaywrightTimeoutError as e:
            # Load-state waits timed out; still try a content snapshot.
            last_error = e
            try:
                return page.content()
            except Exception as content_error:
                last_error = content_error
        except Exception as e:
            last_error = e
            message = str(e).lower()
            if "navigating" not in message or attempt + 1 >= attempts:
                break
            # Brief pause so client-side redirects / meta-refresh can finish.
            page.wait_for_timeout(500 * (attempt + 1))
    print(f"Error retrieving content from {url}: {last_error}")
    return None


def fetch_rendered_html(url: str, user_agent: str) -> str:
    """Fetches the rendered HTML content of a URL using Playwright."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=user_agent)
        page = context.new_page()
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=10000)
            # Extra settle after the initial document so late redirects finish.
            try:
                page.wait_for_load_state("networkidle", timeout=10000)
            except PlaywrightTimeoutError:
                page.wait_for_timeout(1000)
        except PlaywrightTimeoutError:
            print(f"Timeout while loading {url}, attempting to extract partial content.")
        except Exception as e:
            print(f"Error navigating to {url}: {e}")
            browser.close()
            return None
        content = _page_content_with_retry(page, url)
        browser.close()
    return content


def fetch_and_convert_to_markdown(url, user_agent, drop_links=False):
    """Fetches HTML and converts to Markdown using a custom safe converter."""
    html = fetch_rendered_html(url, user_agent)
    if not html:
        return None

    if drop_links:
        markdown_text = SpacePreservingConverter().convert(html)
    else:
        from markdownify import markdownify as md
        markdown_text = md(html)

    return markdown_text

def main(argv=None):
    parser = argparse.ArgumentParser(description="Convert a webpage to Markdown.")
    parser.add_argument("url", type=str, help="The URL of the webpage to convert.")
    parser.add_argument("--user-agent", type=str, help="Optional User Agent header to send.")
    parser.add_argument("--drop-links", action="store_true", help="Drop hyperlinks and image links.")
    
    args = parser.parse_args(argv)
    
    user_agent = args.user_agent or os.getenv("USER_AGENT", None) or DEFAULT_USER_AGENT

    markdown_text = fetch_and_convert_to_markdown(args.url, user_agent, args.drop_links)

    if markdown_text:
        print(markdown_text)

if __name__ == "__main__":
    main()
