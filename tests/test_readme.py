import hashlib
import pathlib
import re
from typing import List

import pytest

README_PATH = pathlib.Path(__file__).parent.parent / "README.md"
README_CHECKSUM_ALLOWED = "072c838ecd280c7eda3305c89274d5b0"


@pytest.fixture
def python_snippets():
    readme_contents_bytes = README_PATH.read_bytes()

    hash_md5 = hashlib.md5(readme_contents_bytes)
    assert hash_md5.hexdigest() == README_CHECKSUM_ALLOWED

    code_snippets = re.findall(
        r"```python(.*?)```", readme_contents_bytes.decode(), re.DOTALL
    )
    yield code_snippets


def test_all_snippets_working(python_snippets: List[str]):
    for snippet in python_snippets:
        exec(snippet)
