from podbucket import resourcesync

import dotenv

dotenv.load_dotenv()


def test_get_streams():
    streams = resourcesync.get_streams()
    assert (
        streams["stanford"]
        == "https://pod.stanford.edu/organizations/stanford/streams/2024-08-27/normalized_resourcelist/marcxml"
    )


def test_get_resources():
    resources = resourcesync.get_resources(
        "https://pod.stanford.edu/organizations/stanford/streams/2024-08-27/normalized_resourcelist/marcxml"
    )
    assert len(resources) > 0
    assert resources[0].url
    assert resources[0].mediatype
    assert resources[0].length
    assert resources[0].fixity
