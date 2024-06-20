# Test the main function output in console "Hello, world!"

from folder_replicator.__main__ import main


def test_main(capsys):
    """
    Test the main function output in console "Hello, world!
    """

    main()
    captured = capsys.readouterr()
    assert captured.out == "Hello, world!\n"
    assert captured.err == ""
