# Test the main function output in console "Hello, world!"

from folder_replicator.__main__ import _print_hello


def test_main(capsys):
    """
    Test the main function output in console "Hello, world!
    """

    _print_hello()
    captured = capsys.readouterr()
    assert "Hello, world!" in captured.out
    assert captured.err == ""
