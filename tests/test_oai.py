import datetime

from podbucket import oai
from podbucket.oai import XML_NS


def test_list_records() -> None:
    """
    Use ListRecords to fetch Stanford POD records that were updated since yesterday.
    """
    yesterday = datetime.date.today() - datetime.timedelta(days=1)

    # stanford is set id 503
    for count, rec in enumerate(oai.list_records("503", from_=yesterday.isoformat())):
        # get the timestamp from the OAI record and ensure it looks right
        ds = datetime.date.fromisoformat(
            rec.find(".//oai:header/oai:datestamp", namespaces=XML_NS).text
        )
        assert ds >= yesterday, f"timestamp is after {yesterday.isoformat()}"
        breakpoint()

        # if the status for the record is "deleted" we can skip looking for the metadata
        if (
            rec.find(".//oai:header", namespaces=XML_NS).attrib.get("status")
            == "deleted"
        ):
            continue

        # make sure there is marc metadata is present in the oai record
        marc = rec.find(".//marc:record", namespaces=XML_NS)
        assert marc, "marc record found in oai record"

        # if we are collecting too many records assume something is wrong and abort
        if count > 100_000:
            raise Exception("ListRecords is returning too much!")

    assert count > 0, "found some records"
