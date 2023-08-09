mod common;

use common::*;
use eggshell::egg_error::*;
use eggshell::lexer_util::Lexer;

#[test]
fn check_tokens() -> Result<()> {
    let mut suite = TestSuite::new();
    suite.load_tests()?;

    let lexer = Lexer::new();
    for (test_number, test_case) in suite.test_cases.iter().enumerate() {
        if let Some(expected) = &test_case.expected_tokens {
            let file = suite.source_manager.get_file(test_case.file_id)?;
            let tokens = lexer
                .tokenize(&file)
                .map_err(|e| EggError::TestCaseFailedWithError {
                    test_file: test_case.file.clone(),
                    test_number: test_number,
                    error: Box::new(e),
                })?;

            let mut token_infos: Vec<common::TokenInfo> = Vec::new();
            for token in tokens {
                token_infos.push(common::TokenInfo {
                    lexeme_name: format!("{:?}", token.lexeme),
                    contents: file.get_slice(&token.location).map_err(|e| {
                        EggError::TestCaseFailedWithError {
                            test_file: test_case.file.clone(),
                            test_number: test_number,
                            error: Box::new(e),
                        }
                    })?,
                });
            }

            if !vecs_equal(&token_infos, &expected) {
                return raise_test_error(
                    &suite,
                    test_case,
                    test_number,
                    format!(
                        "Lexer output does not match expectations:
                    Lexer Output: {:?},
                    Expected Tokens: {:?}",
                        token_infos, expected
                    ),
                );
            }
        }
    }
    Ok(())
}
