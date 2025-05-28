# podbucket

[![Tests](https://github.com/sul-dlss/podbucket/actions/workflows/test.yml/badge.svg)](https://github.com/sul-dlss/podbucket/actions/workflows/test.yml)

podbucket is a command line utility for converting [POD](https://pod.stanford.edu/) MARC XML data into Parquet files and storing them in an Amazon S3 bucket for use in data analysis tools like Spark, Presto, or services like AWS Athena.

## Install

First install [uv] to get a working Python environment and then setup podbucket 

```
$ uvx podbucket config
```

You'll be prompted for your POD API key, S3 bucket and AWS credentials which will be saved.

Then you can run it for all providers:

```
$ uvx podbucket convert
```

or a single provider:

```
$uvx podbucket convert --org stanford
```

## Develop

You'll want to clone this repository, make changes and then run the tests:

```
$ uv run pytest
```

[POD]: https://pod.stanford.edu/
[uv]: https://docs.astral.sh/uv/
