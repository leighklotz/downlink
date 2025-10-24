#!/usr/bin/env python3
"""
downlink.cli

Entry point for the `downlink` console script. Provides a small CLI to download
one or more URLs with a progress bar (requests + tqdm).
"""
from __future__ import annotations

import argparse
import os
import sys
from urllib.parse import urlsplit, unquote
from typing import List, Optional

import requests
from tqdm import tqdm


def _suggest_filename_from_url(url: str) -> str:
    path = urlsplit(url).path
    name = os.path.basename(path) or "download"
    return unquote(name)


def download_url(url: str, output_path: Optional[str] = None, chunk_size: int = 8192) -> str:
    """
    Download `url` and save to `output_path` (if provided) or inferred filename.
    Returns the path to the saved file.
    """
    if output_path is None:
        fname = _suggest_filename_from_url(url)
        output_path = os.path.join(os.getcwd(), fname)

    # If output_path is a directory, append filename
    if os.path.isdir(output_path):
        fname = _suggest_filename_from_url(url)
        output_path = os.path.join(output_path, fname)

    # Make sure parent directory exists
    parent = os.path.dirname(os.path.abspath(output_path)) or "."
    os.makedirs(parent, exist_ok=True)

    with requests.get(url, stream=True, timeout=10) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0)) if r.headers.get("content-length") else None
        desc = os.path.basename(output_path)
        disable_tqdm = os.getenv("TQDM_DISABLE", "0") == "1"
        with open(output_path, "wb") as f, tqdm(
            total=total, unit="B", unit_scale=True, unit_divisor=1024, desc=desc, leave=True, disable=disable_tqdm
        ) as bar:
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    bar.update(len(chunk))

    return output_path


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="downlink", description="Download one or more URLs with a progress bar.")
    p.add_argument("urls", nargs="+", help="URLs to download")
    p.add_argument("-o", "--output", help="Output filename (for a single URL) or directory (when downloading multiple files)")
    p.add_argument("-d", "--dir", dest="directory", help="Directory to save files into (alternative to -o)")
    p.add_argument("-q", "--quiet", action="store_true", help="Suppress progress output (still saves files)")
    return p.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)

    out = args.output
    directory = args.directory
    quiet = args.quiet

    # If output provided and multiple URLs, treat output as directory
    if out and len(args.urls) > 1:
        directory = out

    if directory and not os.path.isdir(directory):
        os.makedirs(directory, exist_ok=True)

    saved_paths = []
    try:
        for url in args.urls:
            if directory:
                target = directory
            elif out and len(args.urls) == 1:
                target = out
            elif out and len(args.urls) > 1:
                target = out
            else:
                target = None

            if quiet:
                os.environ["TQDM_DISABLE"] = "1"

            saved = download_url(url, output_path=target)
            saved_paths.append(saved)

            if quiet and "TQDM_DISABLE" in os.environ:
                del os.environ["TQDM_DISABLE"]

        for path in saved_paths:
            print(path)
        return 0
    except KeyboardInterrupt:
        print("Download cancelled.", file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())