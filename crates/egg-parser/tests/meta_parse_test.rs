mod common;

use indoc::indoc;

use egg_grammar::*;
use egg_parser::errors::*;
use egg_parser::meta_parse::*;

#[test]
fn check_meta_parser() -> Result<()> {
    let mut test_cases: Vec<(Rule, String)> = Vec::new();

    test_cases.push((
        Rule::from_sym(Symbol::Program),
        indoc! {"
        ---
        - Symbol<Program>
        "}
        .into(),
    ));
    test_cases.push((
        Rule::from_sym(Symbol::ExecChain).maybe(),
        indoc! {"
        ---
        - Maybe
          - Symbol<ExecChain>
        "}
        .into(),
    ));
    test_cases.push((
        Rule::from_sym(Symbol::ExecChain).star(),
        indoc! {"
        ---
        - Star
          - Symbol<ExecChain>
        "}
        .into(),
    ));
    test_cases.push((
        Rule::from_sym(Symbol::ExecChain).plus(),
        indoc! {"
        ---
        - Plus
          - Symbol<ExecChain>
        "}
        .into(),
    ));
    test_cases.push((
        Rule::from_sym(Symbol::Program).then_sym(Symbol::ExecChain),
        indoc! {"
        ---
        - Sequence
          - Symbol<Program>
          - Symbol<ExecChain>
        "}
        .into(),
    ));
    test_cases.push((
        Rule::from_sym(Symbol::Program).or_sym(Symbol::ExecChain),
        indoc! {"
        ---
        - Any
          - Symbol<Program>
          - Symbol<ExecChain>
        "}
        .into(),
    ));
    test_cases.push((
        Rule::from_sym(Symbol::Program)
            .then_tok(Lexeme::Redirect)
            .then_one_of(&mut vec![
                Block::Symbol(Symbol::ExecChain),
                Block::Token(Lexeme::Pipe),
                Block::Token(Lexeme::Literal),
            ]),
        indoc! {"
        ---
        - Sequence
          - Symbol<Program>
          - Token<Redirect>
          - Any
            - Symbol<ExecChain>
            - Token<Pipe>
            - Token<Literal>
        "}
        .into(),
    ));
    test_cases.push((
        Rule::from_sym(Symbol::Program).then_star(Block::Token(Lexeme::Redirect)),
        indoc! {"
        ---
        - Sequence
          - Symbol<Program>
          - Star
            - Token<Redirect>
        "}
        .into(),
    ));
    test_cases.push((
        Rule::from_sym(Symbol::Program).then_plus(Block::Token(Lexeme::Pipe)),
        indoc! {"
        ---
        - Sequence
          - Symbol<Program>
          - Plus
            - Token<Pipe>
        "}
        .into(),
    ));
    test_cases.push((
        Rule::from_tok(Lexeme::Redirect)
            .or_sym(Symbol::RedirectExec)
            .then_sym(Symbol::RedirectTarget),
        indoc! {"
        ---
        - Sequence
          - Any
            - Token<Redirect>
            - Symbol<RedirectExec>
          - Symbol<RedirectTarget>
        "}
        .into(),
    ));
    test_cases.push((
        Rule::from_tok(Lexeme::Redirect).then_maybe(Block::Symbol(Symbol::RedirectTarget)),
        indoc! {"
        ---
        - Sequence
          - Token<Redirect>
          - Maybe
            - Symbol<RedirectTarget>
        "}
        .into(),
    ));

    // Test then(rule)
    test_cases.push((
        Rule::from_tok(Lexeme::Redirect).then(Rule::from_tok(Lexeme::Pipe)),
        indoc! {"
        ---
        - Sequence
          - Token<Redirect>
          - Token<Pipe>
        "}
        .into(),
    ));
    test_cases.push((
        Rule::from_tok(Lexeme::Pipe)
            .then(Rule::from_tok(Lexeme::Redirect).or_sym(Symbol::RedirectExec)),
        indoc! {"
        ---
        - Sequence
          - Token<Pipe>
          - Any
            - Token<Redirect>
            - Symbol<RedirectExec>
        "}
        .into(),
    ));
    test_cases.push((
        Rule::from_tok(Lexeme::Pipe).then(
            Rule::from_tok(Lexeme::Redirect)
                .or_sym(Symbol::RedirectExec)
                .then_sym(Symbol::Exec),
        ),
        indoc! {"
        ---
        - Sequence
          - Token<Pipe>
          - Any
            - Token<Redirect>
            - Symbol<RedirectExec>
          - Symbol<Exec>
        "}
        .into(),
    ));
    test_cases.push((
        Rule::from_tok(Lexeme::Literal).then(
            Rule::from_sym(Symbol::PipeExec)
                .or_sym(Symbol::RedirectExec)
                .maybe(),
        ),
        indoc! {"
        ---
        - Sequence
          - Token<Literal>
          - Maybe
            - Any
              - Symbol<PipeExec>
              - Symbol<RedirectExec>
        "}
        .into(),
    ));
    test_cases.push((
        Rule::from_sym(Symbol::Exec).then(
            Rule::from_sym(Symbol::PipeExec)
                .or_sym(Symbol::RedirectExec)
                .maybe(),
        ),
        indoc! {"
        ---
        - Sequence
          - Symbol<Exec>
          - Maybe
            - Any
              - Symbol<PipeExec>
              - Symbol<RedirectExec>
        "}
        .into(),
    ));

    for (i, (rule, expectation)) in test_cases.iter().enumerate() {
        let rule_str = rule.to_string()?;
        if rule_str != *expectation {
            return common::raise_internal_test_error(
                "Meta Parser".into(),
                i,
                format!(
                    "Meta Parser Rule does not match expectations:\nRule:\n{}\nExpected rule: \n{}\n", 
                    rule_str,
                    expectation
                ).into(),
            );
        }
    }

    Ok(())
}
