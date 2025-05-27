from pathlib import Path
from podbucket.convert import convert_marcxml


def test_convert(tmp_path):
    marcxml_url = (
        "https://pod.stanford.edu/file/473765/stanford-2025-05-20-delta-marcxml.xml.gz"
    )
    parquet_path = convert_marcxml(marcxml_url, name="stanford", storage_root=tmp_path)
    #assert parquet_path
    #assert parquet_path.is_file()
