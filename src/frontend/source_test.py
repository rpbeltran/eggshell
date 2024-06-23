from .source import *

src_str = (
    "012345678\n"
    "abcdefghi\n"
    "ABCDEFGHI\n"
    "wxyz!"
)


def test_source():
    src = Source(src_str)
    assert src.new_lines == [9, 19, 29]
    for i in range(34):
        assert src.get_line_col(i) == (i // 10, i % 10)


def test_source_manager():
    src_man = SourceManager()
    src_man.add_source("test_src", src_str)
    for i in range(34):
        for j in range(i, 34):
            loc = SourceLocation("test_src", i, j)
            assert src_man.get_source_for_loc(loc) == src_str[i:j]
            assert src_man.get_start_line_col(loc) == (i // 10, i % 10)
            assert src_man.get_end_line_col(loc) == (j // 10, j % 10)
