# Test the main function output in console "Hello, world!"

from folder_replicator.__main__ import main


def test_main(capsys):
    """
    Test the main function output in console "Hello, world!
    """

    main()
    captured = capsys.readouterr()
    assert "Hello, world!" in captured.out
    assert captured.err == ""
