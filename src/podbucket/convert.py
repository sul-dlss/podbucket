import gzip
import logging
import re
import shutil
from pathlib import Path

from marctable import to_parquet
from podbucket.resourcesync import download


logger = logging.getLogger(__name__)


def convert_marcxml(marcxml_url: str, storage_root: Path):
    filename = marcxml_url.split("/")[-1]

    marcxml_gz_path = storage_root / filename
    marcxml_path = storage_root / re.sub(r"\.xml.gz$", ".xml", filename)
    parquet_path = storage_root / re.sub(r"\.xml\.gz$", ".parquet", filename)

    logger.info(f"downloading {marcxml_url} to {marcxml_gz_path}")
    download(marcxml_url, marcxml_gz_path)
    decompress(marcxml_gz_path, marcxml_path)
    to_parquet(marcxml_path, parquet_path)

    return parquet_path


def decompress(in_path: Path, out_path: Path) -> None:
    with gzip.open(in_path, "rb") as in_fh:
        with out_path.open("wb") as out_fh:
            shutil.copyfileobj(in_fh, out_fh)
