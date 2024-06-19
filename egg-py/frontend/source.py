import bisect
from typing import Dict, NamedTuple, Tuple


class SourceLocation(NamedTuple):
    file_path: str
    start_offset: int
    end_offset: int


class Source:
    def __init__(self, source: str):
        self.source = source
        self.new_lines = self.get_new_lines(source)

    @staticmethod
    def get_new_lines(source: str):
        return [i for i, c in enumerate(source) if c == '\n']

    def get_line_col(self, offset: int) -> Tuple[int, int]:
        line = bisect.bisect_left(self.new_lines, offset)
        if line == 0:
            return line, offset
        col = offset - self.new_lines[line - 1] - 1
        return line, col


class SourceManager:
    def __init__(self):
        self.sources: Dict[str, Source] = {}

    def add_source(self, path, src):
        self.sources[path] = Source(src)

    def get_source_for_loc(self, loc: SourceLocation) -> str:
        return self.sources[loc.file_path].source[
            loc.start_offset : loc.end_offset
        ]

    def get_start_line_col(self, loc: SourceLocation) -> Tuple[int, int]:
        return self.sources[loc.file_path].get_line_col(loc.start_offset)

    def get_end_line_col(self, loc: SourceLocation) -> Tuple[int, int]:
        return self.sources[loc.file_path].get_line_col(loc.end_offset)
