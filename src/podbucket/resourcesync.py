import datetime
import os
import re
from dataclasses import dataclass

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
        org = re.search(r"organizations/(.+?)/", loc.text).group(1)
        streams[org] = loc.text

    return streams


def get_resources(url: str) -> list[Resource]:
    doc = get_xml(url)

    resources = []
    for url in doc.findall("sitemap:url", namespaces):
        md = url.find("rs:md", namespaces)
        loc = url.find("sitemap:loc", namespaces).text
        lastmod = url.find("sitemap:lastmod", namespaces).text

        resources.append(
            Resource(
                url=loc,
                mediatype=md.attrib["type"],
                length=int(md.attrib["length"]),
                fixity=md.attrib["hash"],
                lastmod=datetime.datetime.fromisoformat(lastmod),
            )
        )

    return resources


def get_xml(url: str) -> ET.Element:
    resp = get(url)
    resp.raise_for_status()

    return ET.fromstring(resp.text)


def get(url) -> httpx.Response:
    token = os.environ.get("PODBUCKET_POD_TOKEN")
    return httpx.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=60.0)
