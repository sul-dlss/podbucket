import pandas

from podbucket.convert import marcxml_to_parquet


def test_convert(tmp_path):
    marcxml_url = (
        "https://pod.stanford.edu/file/475329/stanford-2025-05-26-delta-marcxml.xml.gz"
    )

    parquet_path = marcxml_to_parquet(marcxml_url, output_dir=tmp_path)
    assert parquet_path.is_file()

    df = pandas.read_parquet(parquet_path)
    assert len(df) > 0
    assert df["F245"].iloc[0] == "El puente de los asesinos / Arturo Pérez-Reverte."
