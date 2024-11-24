from mktimeline import __version__, some_function


def test_version():
    assert __version__ == '0.1.0'

def test_functionality():
    result = some_function()
    assert result == 'expected result'
