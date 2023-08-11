use egg_parser::errors::*;
use egg_parser::lexer_util::Lexer;
use egg_parser::parser;

mod common;
use common::*;

#[test]
fn check_parser() -> Result<()> {
    let mut suite = TestSuite::new();
    suite.load_tests()?;

    for (test_number, test_case) in suite.test_cases.iter().enumerate() {
        if let Some(expected_syntax_tree) = &test_case.expected_syntax_tree {
            let file = suite.source_manager.get_file(test_case.file_id)?;

            let lexer = Lexer::new();
            let tokens = lexer
                .tokenize(&file)
                .map_err(|e| Error::TestCaseFailedWithError {
                    test_file: test_case.file.clone(),
                    test_number: test_number,
                    error: Box::new(e),
                })?;

            let mut token_infos: Vec<TokenInfo> = Vec::new();
            for token in tokens.iter() {
                token_infos.push(TokenInfo {
                    lexeme_name: format!("{:?}", token.lexeme),
                    contents: file.get_slice(&token.location).map_err(|e| {
                        Error::TestCaseFailedWithError {
                            test_file: test_case.file.clone(),
                            test_number: test_number,
                            error: Box::new(e),
                        }
                    })?,
                });
            }

            let mut parser = parser::Parser::new();
            let ast = parser.parse(&tokens)?;
            let syntax_tree_yaml =
                ast_to_string_standardized(&ast, &tokens, &suite.source_manager)?;

            if &syntax_tree_yaml != expected_syntax_tree {
                return raise_test_error(
                    &suite,
                    test_case,
                    test_number,
                    format!(
                        "Parser output does not match expectations:\nParse Output:\n{}\nExpected syntax tree: \n{}\n",
                        syntax_tree_yaml, expected_syntax_tree,
                    ),
                );
            }
        }
    }
    Ok(())
}
