package source

import "fmt"

type SourceManager struct {
	file_paths map[string]int
	sources    []Source
}

func NewSourceManager() SourceManager {
	return SourceManager{
		file_paths: make(map[string]int),
		sources:    make([]Source, 0),
	}
}

func (manager *SourceManager) UpsertSource(filepath string, contents string, append_newline bool) {
	source := NewSource(filepath, contents, append_newline)
	if source_id, has_source := manager.file_paths[filepath]; !has_source {
		manager.file_paths[filepath] = len(manager.sources)
		manager.sources = append(manager.sources, source)
	} else {
		manager.sources[source_id] = source
	}
}

func (manager *SourceManager) GetCodeSliceForLocation(location SourceLocation) (string, error) {
	if source_id, has_source := manager.file_paths[location.FilePath]; has_source {
		source := manager.sources[source_id]
		if location.Offset < 0 || location.Offset+location.Length > source.length {
			return "", fmt.Errorf("offset %d is out of range; source has length %d", location.Offset, source.length)
		}
		return source.data[location.Offset : location.Offset+location.Length], nil
	}
	return "", fmt.Errorf("no source found for file %s", location.FilePath)
}
