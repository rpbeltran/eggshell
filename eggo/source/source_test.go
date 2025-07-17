package source

import "testing"

type LineAndColTestCase struct {
	offset        int
	expect_error  bool
	expected_line int
	expected_col  int
}

func TestGetLineAndCol(t *testing.T) {
	test_src := "01234\n" +
		"67890\n" +
		"23456\n" +
		"89012\n" +
		"45678\n"

	source := NewSource("", test_src)
	test_cases := []LineAndColTestCase{
		{0, false, 1, 1},
		{1, false, 1, 2},
		{5, false, 1, 6},
		{6, false, 2, 1},
		{7, false, 2, 2},
		{10, false, 2, 5},
		{11, false, 2, 6},
		{12, false, 3, 1},
		{19, false, 4, 2},
		{26, false, 5, 3},
		{29, false, 5, 6},
		{30, true, 0, 0},
		{-1, true, 0, 0},
		{100, true, 0, 0},
	}

	for _, tc := range test_cases {
		if line, col, err := source.GetLineAndCol(tc.offset); !tc.expect_error && err != nil {
			t.Fatalf("For offest %d, unexpected error: %v", tc.offset, err)
		} else if tc.expect_error && err == nil {
			t.Fatalf("For offest %d, expected out of bounds error, got none", tc.offset)
		} else if line != tc.expected_line {
			t.Fatalf("For offest %d, expected line %d, got %d", tc.offset, tc.expected_line, line)
		} else if col != tc.expected_col {
			t.Fatalf("For offest %d, expected col %d, got %d", tc.offset, tc.expected_col, col)
		}
	}
}
