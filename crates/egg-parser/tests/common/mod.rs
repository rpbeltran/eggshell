#![allow(dead_code)]
use egg_parser::ast::Ast;
use egg_source::source_file::SourceFile;
use egg_source::source_manager::SourceManager;

use std::fmt;
use std::fs;

use std::io::prelude::*;
use std::path::PathBuf;

use egg_parser::errors::*;
use egg_parser::token::Token;

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
    pub source_manager: SourceManager,
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
            source_manager: SourceManager::new(),
            test_cases: Vec::new(),
        };
        suite
    }

    /// Load all testcases into the suite.
    pub fn load_tests(&mut self) -> Result<()> {
        for result in fs::read_dir("tests/data").map_err(|e| Error::FileReadError(e))? {
            let path = &result.map_err(|e| Error::FileReadError(e))?.path();
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
            .map_err(Error::TestFileNotFound)?
            .read_to_string(&mut file_buf)
            .map_err(Error::TestLineReadFailed)?;

        let test_docs =
            yaml_rust::YamlLoader::load_from_str(&file_buf).map_err(|e| Error::TestYamlError {
                file: test_file.clone(),
                line: e.marker().line(),
            })?;

        let tests = test_docs[0].as_vec().ok_or(Error::TestYamlLineError)?;

        for (test_num, test) in tests.iter().enumerate() {
            let input = test["input"]
                .as_vec()
                .ok_or(Error::TestYamlLineError)?
                .iter()
                .map(|x| x.as_str().ok_or(Error::TestYamlLineError))
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
        test_suite.source_manager.get_file(test_case.file_id).map_err(Error::SourceError)?.contents
    );
    Err(Error::TestCaseFailedAssertion {
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
    Err(Error::InternalTestCaseFailedAssertion {
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

/// Serialize abstract syntax tree to a vector of YAML node.
pub fn ast_to_yaml(
    ast: &Ast,
    tokens: &[Token],
    source_manager: &SourceManager,
) -> Result<yaml_rust::Yaml> {
    let as_string = ast.to_string(tokens, source_manager)?;
    let as_yaml = yaml_rust::YamlLoader::load_from_str(as_string.as_str()).expect("");
    Ok(as_yaml[0].clone()) // todo: get rid of the need for this clone
}

/// Serialize abstract syntax tree to a string then to a YAML node and then back to a string.
pub fn ast_to_string_standardized(
    ast: &Ast,
    tokens: &[Token],
    source_manager: &SourceManager,
) -> Result<String> {
    let mut as_yaml = String::new();
    yaml_rust::YamlEmitter::new(&mut as_yaml)
        .dump(&ast_to_yaml(&ast, tokens, source_manager)?)
        .unwrap();
    Ok(as_yaml)
}
