import datetime
import os
import re
from dataclasses import dataclass
from pathlib import Path

import xml.etree.ElementTree as ET

import httpx

namespaces = {
    "sitemap": "http://www.sitemaps.org/schemas/sitemap/0.9",
    "rs": "http://www.openarchives.org/rs/terms/",
}


@dataclass
class Resource:
    url: str
    mediatype: str
    length: int
    fixity: str
    lastmod: datetime.datetime


def get_streams() -> dict:
    """
    Returns a dictionary that maps organization names to their stream url.
    """
    doc = get_xml(
        "https://pod.stanford.edu/organizations/normalized_resourcelist/marcxml"
    )

    streams = {}
    for sitemap in doc.findall("sitemap:sitemap", namespaces):
        loc = sitemap.find("sitemap:loc", namespaces)
        if loc is None or loc.text is None:
            raise Exception("Missing <loc> element in sitemap index")

        if match := re.search(r"organizations/(.+?)/", loc.text):
            org = match.group(1)
        else:
            raise Exception(f"Missing organization name in URL {loc.text}")

        streams[org] = loc.text

    return streams


def get_resources(sitemap_url: str) -> list[Resource]:
    doc = get_xml(sitemap_url)

    resources = []
    for url in doc.findall("sitemap:url", namespaces):
        lastmod = url.find("sitemap:lastmod", namespaces)
        if lastmod is None or lastmod.text is None:
            raise Exception(f"Missing <lastmod> in {url}")

        loc = url.find("sitemap:loc", namespaces)
        if loc is None or loc.text is None:
            raise Exception(f"Missing <loc> URL in {url}")

        md = url.find("rs:md", namespaces)
        if md is None or loc is None or lastmod is None:
            raise Exception(f"Invalid ResourceSync resource in {url}")

        resources.append(
            Resource(
                url=loc.text,
                mediatype=md.attrib["type"],
                length=int(md.attrib["length"]),
                fixity=md.attrib["hash"],
                lastmod=datetime.datetime.fromisoformat(lastmod.text),
            )
        )

    return resources


def get_xml(url: str) -> ET.Element:
    """
    Get the XML at a URL, parse it, and return the document.
    """
    resp = get(url)
    resp.raise_for_status()

    return ET.fromstring(resp.text)


def get(url: str) -> httpx.Response:
    """
    Get a POD URL and return the response.
    """
    return httpx.get(url, headers=_headers(), timeout=60)


def download(url: str, path: Path) -> Path:
    """
    Download a POD URL to a given path.
    """
    with path.open("wb") as output:
        with httpx.stream("GET", url, headers=_headers(), timeout=60) as resp:
            for data in resp.iter_bytes():
                output.write(data)

    return path


def _headers():
    token = os.environ.get("PODBUCKET_POD_TOKEN")
    if token is None:
        raise Exception("PODBUCKET_POD_TOKEN env var isn't set!")
    return {"Authorization": f"Bearer {token}"}
