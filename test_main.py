import pytest
from main import format_time

def test_format_time():
    assert format_time(60) == "00:01"
    assert format_time(0) == "00:00"