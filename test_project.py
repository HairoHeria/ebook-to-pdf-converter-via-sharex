from project import valid_dir
from project import valid_ebook_pages
from project import valid_ebook_name


def test_valid_dir():
    assert valid_dir(r"C:\Users\Desktop")
    assert valid_dir(r"D:\Documents\CS50")
    assert not valid_dir(r"C:\Users\My:Folder")
    assert not valid_dir(r"C:\\Users\\My*Folder")
    assert not valid_dir(r"C:\\\\")
    assert not valid_dir(r"C:\\|Users")
    assert not valid_dir(r"cat")


def test_valid_ebook_name():
    assert valid_ebook_name(r"Biology")
    assert valid_ebook_name(r"Rhythm of War")
    assert not valid_ebook_name(r"<Math>")
    assert not valid_ebook_name(r"Strike/Out")
    assert not valid_ebook_name(r"Meaning of Life?")


def test_valid_ebook_pages():
    assert valid_ebook_pages(5)
    assert valid_ebook_pages(100)
    assert not valid_ebook_pages(0)
    assert not valid_ebook_pages(-10)
