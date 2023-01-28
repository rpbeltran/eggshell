#![allow(dead_code)]
use eggshell::source::SourceFile;

use std::fmt;
use std::fs;

use std::io::prelude::*;
use std::path::PathBuf;

use eggshell::egg_error::*;
use eggshell::source;

extern crate yaml_rust;

#[derive(PartialEq)]
pub struct TokenInfo {
    pub lexeme_name: String,
    pub contents: String,
}

impl fmt::Debug for TokenInfo {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}:{{{}}}", self.lexeme_name, self.contents)
    }
}

pub struct TestSuite {
    pub source_manager: source::SourceManager,
    pub test_cases: Vec<TestCase>,
}

pub struct TestCase {
    pub file: PathBuf,
    pub expected_tokens: Option<Vec<TokenInfo>>,
    pub expected_syntax_tree: Option<String>,
    pub file_id: usize,
}

impl TestSuite {
    pub fn new() -> Self {
        let suite = TestSuite {
            source_manager: source::SourceManager::new(),
            test_cases: Vec::new(),
        };
        suite
    }

    /// Load all testcases into the suite.
    pub fn load_tests(&mut self) -> Result<()> {
        for result in fs::read_dir("tests/data").map_err(|e| EggError::FileReadError(e))? {
            let path = &result.map_err(|e| EggError::FileReadError(e))?.path();
            if path.to_string_lossy().ends_with(".yaml") {
                self.parse_yaml_tests(path)?;
            }
        }
        Ok(())
    }

    /// Parse a test file into test cases.
    fn parse_yaml_tests(&mut self, test_file: &PathBuf) -> Result<()> {
        let mut file_buf: String = String::new();
        fs::File::open(test_file.clone())
            .map_err(EggError::TestFileNotFound)?
            .read_to_string(&mut file_buf)
            .map_err(EggError::TestLineReadFailed)?;

        let test_docs =
            yaml_rust::YamlLoader::load_from_str(&file_buf).map_err(EggError::TestYamlError)?;

        let tests = test_docs[0].as_vec().ok_or(EggError::TestYamlLineError)?;

        for (test_num, test) in tests.iter().enumerate() {
            let input = test["input"]
                .as_vec()
                .ok_or(EggError::TestYamlLineError)?
                .iter()
                .map(|x| x.as_str().ok_or(EggError::TestYamlLineError))
                .collect::<Result<Vec<&str>>>()?
                .join("\n")
                + "\n";

            let mut line_indexes: Vec<usize> = input.match_indices('\n').map(|(i, _)| i).collect();
            line_indexes.insert(0, 0);

            let expected_tokens = test["tokens"].as_vec().map(|tokens| {
                tokens
                    .iter()
                    .map(|token| TokenInfo {
                        lexeme_name: token["lexeme"].as_str().unwrap_or("").to_string(),
                        contents: token["contents"].as_str().unwrap_or("").to_string(),
                    })
                    .collect::<Vec<TokenInfo>>()
            });

            let mut expected_syntax_tree = String::new();
            let mut emitter = yaml_rust::YamlEmitter::new(&mut expected_syntax_tree);
            emitter.dump(&test["syntax tree"]).unwrap();

            let char_count = input.len();
            self.source_manager.files.push(SourceFile {
                contents: input,
                file_id: test_num,
                line_indexes,
                char_count,
            });

            self.source_manager
                .file_paths
                .push(PathBuf::from(test_num.to_string()));

            self.test_cases.push(TestCase {
                file: test_file.clone(),
                file_id: test_num,
                expected_tokens,
                expected_syntax_tree: if expected_syntax_tree == "---\n~" {
                    None
                } else {
                    Some(expected_syntax_tree)
                },
            });
        }
        Ok(())
    }
}

impl Default for TestSuite {
    fn default() -> Self {
        Self::new()
    }
}

/// Print a formatted error message and return an EggError::TestCaseFailedAssertion;
pub fn raise_test_error(
    test_suite: &TestSuite,
    test_case: &TestCase,
    test_number: usize,
    error: String,
) -> Result<()> {
    eprintln!(
        "\n------------------\nTest Case Failed!!!!\nTest {} in {}\n{}\nInput:\n{}\n------------------\n",
        test_number,
        test_case.file.clone().to_string_lossy(),
        error,
        test_suite.source_manager.get_file(test_case.file_id)?.contents
    );
    Err(EggError::TestCaseFailedAssertion {
        test_file: test_case.file.clone(),
        test_number,
        error,
    })
}

/// Print a formatted error message and return an EggError::InternalTestCaseFailedAssertion;
pub fn raise_internal_test_error(
    category: Box<str>,
    test_number: usize,
    error: Box<str>,
) -> Result<()> {
    eprintln!(
        "\n------------------\n{}Test Case Failed!!!!\nTest {}\n{}\n------------------\n",
        category, test_number, error,
    );
    Err(EggError::InternalTestCaseFailedAssertion {
        category: "Meta Parse".into(),
        test_number,
        error,
    })
}

#[allow(dead_code)]
/// Compare vectors item by item.
/// Returns true iff the vectors are equal length and associated items are equal.
pub fn vecs_equal<T: std::cmp::PartialEq>(a: &Vec<T>, b: &Vec<T>) -> bool {
    (a.len() == b.len()) && (0..a.len()).all(|i| a[i] == b[i])
}
