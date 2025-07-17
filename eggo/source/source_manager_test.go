package source

import "testing"

func TestUpsertSource(t *testing.T) {
	manager := NewSourceManager()
	manager.UpsertSource("a", "ardvark")
	manager.UpsertSource("b", "banana")
	b_id := manager.file_paths["b"]
	manager.UpsertSource("c", "chair")
	manager.UpsertSource("b", "bread")

	if len(manager.sources) != 3 {
		t.Fatalf("Expected 3 sources but there were %d", len(manager.sources))
	}
	if manager.sources[b_id].data != "bread" {
		t.Fatalf("Expected b was updated to bred but it was %s", manager.sources[b_id].data)
	}
	if manager.file_paths["b"] != b_id {
		t.Fatalf("Expected id for b to be %d but it was %d", b_id, manager.file_paths["b"])
	}
	if a_actual := manager.sources[manager.file_paths["a"]].data; a_actual != "ardvark" {
		t.Fatalf("Expected b was updated to ardvark but it was %s", a_actual)
	}
	if c_actual := manager.sources[manager.file_paths["c"]].data; c_actual != "chair" {
		t.Fatalf("Expected b was updated to ardvark but it was %s", c_actual)
	}
}

type GetCodeSliceForLocationTestCase struct {
	offest         int
	length         int
	expect_error   bool
	expected_slice string
}

func TestGetCodeSliceForLocation(t *testing.T) {
	manager := NewSourceManager()
	manager.UpsertSource("", "01234567890123456789")

	test_cases := []GetCodeSliceForLocationTestCase{
		{0, 10, false, "0123456789"},
		{5, 10, false, "5678901234"},
		{0, 20, false, "01234567890123456789"},
		{0, 100, true, ""},
		{100, 10, true, ""},
		{100, 10, true, ""},
		{-1, 10, true, ""},
	}

	for _, tc := range test_cases {

		SourceLocation := SourceLocation{
			file_path: "",
			offset:    tc.offest,
			length:    tc.length,
		}

		slice, err := manager.GetCodeSliceForLocation(SourceLocation)

		if !tc.expect_error && err != nil {
			t.Fatalf("Unexpected error for offset %d and length %d: %v", tc.offest, tc.length, err)
		}
		if tc.expect_error && err == nil {
			t.Fatalf("Expected error for offset %d and length %d but there was none", tc.offest, tc.length)
		}
		if slice != tc.expected_slice {
			t.Fatalf("Expected slice for offset %d and length %d to be %q but it was %q", tc.offest, tc.length, tc.expected_slice, slice)
		}
	}
}
