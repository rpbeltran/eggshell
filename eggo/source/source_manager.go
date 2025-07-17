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

func (manager *SourceManager) UpsertSource(filepath string, contents string) {
	source := NewSource(filepath, contents)
	if source_id, has_source := manager.file_paths[filepath]; !has_source {
		manager.file_paths[filepath] = len(manager.sources)
		manager.sources = append(manager.sources, source)
	} else {
		manager.sources[source_id] = source
	}
}

func (manager *SourceManager) GetCodeSliceForLocation(location SourceLocation) (string, error) {
	if source_id, has_source := manager.file_paths[location.file_path]; has_source {
		source := manager.sources[source_id]
		if location.offset < 0 || location.offset+location.length > source.length {
			return "", fmt.Errorf("offset %d is out of range; source has length %d", location.offset, source.length)
		}
		return source.data[location.offset : location.offset+location.length], nil
	}
	return "", fmt.Errorf("no source found for file %s", location.file_path)
}
