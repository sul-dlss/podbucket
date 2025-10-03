import os
from typing import Generator, Optional

from sickle import Sickle
from sickle.iterator import OAIResponseIterator
from lxml.etree import Element

XML_NS = {
    "marc": "http://www.loc.gov/MARC21/slim",
    "oai": "http://www.openarchives.org/OAI/2.0/",
}


def list_records(set_id: str, from_: Optional[str] = None) -> Generator[Element, None, None]:
    oai = Sickle(
        "https://pod.stanford.edu/oai", iterator=OAIResponseIterator, headers=_headers()
    )

    # we are going to get marc21 records for the set
    params = {
        "metadataPrefix": "marc21",
        "set": set_id,
    }

    # optionally add the from date
    if from_:
        params["from"] = from_

    for resp in oai.ListRecords(**params):
        yield from resp.xml.findall(".//oai:record", namespaces=XML_NS)


def _headers() -> dict[str, str]:
    token = os.environ.get("PODBUCKET_POD_TOKEN")
    if token is None:
        raise Exception("PODBUCKET_POD_TOKEN env var isn't set!")
    return {"Authorization": f"Bearer {token}"}
