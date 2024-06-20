import bisect
from typing import Dict, NamedTuple, Optional, Tuple


class SourceLocation(NamedTuple):
    file_path: str
    start_offset: int
    end_offset: int
    src: Optional[str] = None


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
    sources: Dict[str, Source] = {}

    @classmethod
    def add_source(cls, path, src):
        cls.sources[path] = Source(src)

    @classmethod
    def get_source_for_loc(cls, loc: SourceLocation) -> str:
        if loc.src is None:
            return cls.sources[loc.file_path].source[
                loc.start_offset : loc.end_offset
            ]
        return loc.src

    @classmethod
    def get_start_line_col(cls, loc: SourceLocation) -> Tuple[int, int]:
        return cls.sources[loc.file_path].get_line_col(loc.start_offset)

    @classmethod
    def get_end_line_col(cls, loc: SourceLocation) -> Tuple[int, int]:
        return cls.sources[loc.file_path].get_line_col(loc.end_offset)
