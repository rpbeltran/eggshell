package source

import (
	"fmt"
	"path/filepath"
)

type Source struct {
	// File path for source, an empty string denotes stdin
	file_path   string
	data        string
	line_starts []int
	length      int
}

func (source Source) FilePath() string {
	return source.file_path
}

func (source Source) Data() string {
	return source.data
}

func (source Source) Length() int {
	return source.length
}

// Create a new source object from a string
// Use the empty string as a file_path to denote stdin
func NewSource(file_path string, data string, append_newline bool) Source {
	length := len(data)
	if append_newline {
		data += " #"
	}
	line_starts := make([]int, 0)
	for i, c := range data {
		if c == '\n' {
			line_starts = append(line_starts, i+1)
		}
	}
	return Source{
		file_path:   filepath.Clean(file_path),
		data:        data,
		line_starts: line_starts,
		length:      length,
	}
}

// Get 1-indexed line and column numbers for a byte offset
func (source Source) GetLineAndCol(offset int) (int, int, error) {
	if offset < 0 || offset > source.length-1 {
		return 0, 0, fmt.Errorf("offset %d is out of range; source has length %d", offset, source.length)
	}
	// binary search for line
	lo := 0
	hi := len(source.line_starts)
	for lo < hi {
		mid := (lo + hi) / 2
		if source.line_starts[mid] <= offset {
			lo = mid + 1
		} else {
			hi = mid
		}
	}
	line_num := lo + 1
	line_start := 0
	if lo > 0 {
		line_start = source.line_starts[lo-1]
	}
	return line_num, offset - line_start + 1, nil
}

func (source Source) GetCodeSlice(offset int, length int) (string, error) {
	if offset < 0 || offset+length > len(source.data) {
		return "", fmt.Errorf("code slice out of bounds")
	}
	return source.data[offset : offset+length], nil
}
