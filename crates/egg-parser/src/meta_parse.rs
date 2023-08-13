#![allow(dead_code)]

use std::cmp::Ordering;

use egg_ast::annotations::Annotations;
use egg_ast::ast::*;
use egg_grammar::*;
use egg_source::token::Token;

use crate::errors::*;
use crate::meta_parse_rule::*;
use crate::parser::*;

impl Parser {
    /// Attempt to parse an egg program to a syntax tree.
    pub fn parse(&mut self, tokens: &[Token]) -> Result<Ast> {
        let entry_rule = self
            .rules
            .get(&self.entry)
            .ok_or(Error::ParserTriedToBuildSymbolWithNoRule(self.entry))?;
        if let Some((head, ast)) = self.meta_parse(&self.entry, entry_rule, 0, tokens)? {
            match head.cmp(&tokens.len()) {
                Ordering::Equal => Ok(ast),
                Ordering::Less => Err(Error::ParserUnexpectedToken(tokens[head].clone())),
                Ordering::Greater => Err(Error::ParserHeadPastLastToken),
            }
        } else {
            Err(Error::ParserCouldNotParseProgram)
        }
    }

    fn meta_parse(
        &self,
        target: &Symbol,
        rule: &Rule,
        parser_head: usize,
        tokens: &[Token],
    ) -> Result<Option<(usize, Ast)>> {
        Ok(
            if let Some((new_head, mut ast)) =
                self.meta_parse_helper(rule, &rule.root, parser_head, tokens)?
            {
                ast.get_root_mut().map_err(Error::AstError)?.symbol = *target;
                Some((new_head, ast))
            } else {
                None
            },
        )
    }

    fn meta_parse_helper(
        &self,
        rule: &Rule,
        rule_head: &usize,
        parser_head: usize,
        tokens: &[Token],
    ) -> Result<Option<(usize, Ast)>> {
        let rule_root = rule.blocks.get(*rule_head).unwrap();
        match rule_root {
            Block::Symbol(symbol) => self.meta_parse_symbol(symbol, parser_head, tokens),
            Block::Token(lexeme) => self.meta_parse_token(lexeme, parser_head, tokens),
            Block::_Sequence(children) => {
                self.meta_parse_sequence(rule, children, parser_head, tokens)
            }
            Block::_Any(children) => self.meta_parse_any(rule, children, parser_head, tokens),
            Block::_Maybe(child) => self.meta_parse_maybe(rule, child, parser_head, tokens),
            Block::_Star(child) => self.meta_parse_star(rule, child, parser_head, tokens),
            Block::_Plus(child) => self.meta_parse_plus(rule, child, parser_head, tokens),
            Block::_Discard(child) => self.meta_parse_discard(rule, child, parser_head, tokens),
        }
    }

    /// Return a placeholder parse_tree for a sequence clause.
    fn meta_parse_symbol(
        &self,
        symbol: &Symbol,
        head: usize,
        tokens: &[Token],
    ) -> Result<Option<(usize, Ast)>> {
        let mut ast = Ast {
            nodes: vec![AstNode {
                symbol: Symbol::_Placeholder,
                children: vec![],
                token: None,
                annotations: Annotations::new(),
            }],
        };

        if !self.rules.contains_key(symbol) {
            Err(Error::ParserTriedToBuildSymbolWithNoRule(*symbol))
        } else if let Some((new_head, child_ast)) =
            self.meta_parse(symbol, self.rules.get(symbol).unwrap(), head, tokens)?
        {
            ast = ast.hang_child(child_ast).map_err(Error::AstError)?;
            Ok(Some((new_head, ast)))
        } else {
            Ok(None)
        }
    }

    /// Return a placeholder parse_tree for a sequence clause.
    fn meta_parse_sequence(
        &self,
        rule: &Rule,
        children: &Vec<usize>,
        head: usize,
        tokens: &[Token],
    ) -> Result<Option<(usize, Ast)>> {
        let mut new_head = head;
        let mut ast = Ast {
            nodes: vec![AstNode {
                symbol: Symbol::_Placeholder,
                children: vec![],
                token: None,
                annotations: Annotations::new(),
            }],
        };
        for child in children {
            if let Some((_new_head, new_ast)) =
                self.meta_parse_helper(rule, child, new_head, tokens)?
            {
                new_head = _new_head;
                ast = ast
                    .hang_from_placeholder(new_ast)
                    .map_err(Error::AstError)?;
            } else {
                return Ok(None);
            }
        }
        Ok(Some((new_head, ast)))
    }

    /// Return a placeholder parse_tree for an any clause.
    fn meta_parse_any(
        &self,
        rule: &Rule,
        options: &Vec<usize>,
        head: usize,
        tokens: &[Token],
    ) -> Result<Option<(usize, Ast)>> {
        for child in options {
            if let Some((new_head, ast)) = self.meta_parse_helper(rule, child, head, tokens)? {
                return Ok(Some((new_head, ast)));
            }
        }
        Ok(None)
    }

    /// Return a placeholder parse_tree for a maybe clause.
    fn meta_parse_maybe(
        &self,
        rule: &Rule,
        child: &usize,
        head: usize,
        tokens: &[Token],
    ) -> Result<Option<(usize, Ast)>> {
        Ok(self
            .meta_parse_helper(rule, child, head, tokens)?
            .or_else(|| {
                Some((
                    head,
                    Ast {
                        nodes: vec![AstNode {
                            symbol: Symbol::_Placeholder,
                            children: vec![],
                            token: None,
                            annotations: Annotations::new(),
                        }],
                    },
                ))
            }))
    }

    /// Return a placeholder parse_tree for a zero or more clause.
    fn meta_parse_star(
        &self,
        rule: &Rule,
        child: &usize,
        head: usize,
        tokens: &[Token],
    ) -> Result<Option<(usize, Ast)>> {
        let mut new_head = head;
        let mut ast = Ast {
            nodes: vec![AstNode {
                symbol: Symbol::_Placeholder,
                children: vec![],
                token: None,
                annotations: Annotations::new(),
            }],
        };

        while let Some((_new_head, new_ast)) =
            self.meta_parse_helper(rule, child, new_head, tokens)?
        {
            new_head = _new_head;
            ast = ast
                .hang_from_placeholder(new_ast)
                .map_err(Error::AstError)?;
        }

        Ok(Some((new_head, ast)))
    }

    /// Return a placeholder parse_tree for a one or more clause.
    fn meta_parse_plus(
        &self,
        rule: &Rule,
        child: &usize,
        head: usize,
        tokens: &[Token],
    ) -> Result<Option<(usize, Ast)>> {
        Ok(
            if let Some((new_head, new_ast)) = self.meta_parse_star(rule, child, head, tokens)? {
                if new_ast.nodes.len() > 1 {
                    Some((new_head, new_ast))
                } else {
                    None
                }
            } else {
                None
            },
        )
    }

    /// Ensures a match exists for rule, but returns an empty _placeholder tree.
    fn meta_parse_discard(
        &self,
        rule: &Rule,
        child: &usize,
        head: usize,
        tokens: &[Token],
    ) -> Result<Option<(usize, Ast)>> {
        Ok(
            if let Some((new_head, _)) = self.meta_parse_helper(rule, child, head, tokens)? {
                Some((
                    new_head,
                    Ast {
                        nodes: vec![AstNode {
                            symbol: Symbol::_Placeholder,
                            children: vec![],
                            token: None,
                            annotations: Annotations::new(),
                        }],
                    },
                ))
            } else {
                None
            },
        )
    }

    /// Return an AST for a lexeme.
    fn meta_parse_token(
        &self,
        lexeme: &Lexeme,
        head: usize,
        tokens: &[Token],
    ) -> Result<Option<(usize, Ast)>> {
        Ok(if self.recognize_token(lexeme, head, tokens) {
            Some((
                head + 1,
                Ast {
                    nodes: vec![AstNode {
                        symbol: Symbol::_Placeholder,
                        children: vec![],
                        token: None,
                        annotations: Annotations::new(),
                    }],
                }
                .add_child(self.token_to_node(head))
                .map_err(Error::AstError)?,
            ))
        } else {
            None
        })
    }

    /// Build a SyntaxTreeNode object from the token at head.
    fn token_to_node(&self, head: usize) -> AstNode {
        AstNode {
            symbol: Symbol::Lexeme,
            children: vec![],
            token: Some(head),
            annotations: Annotations::new(),
        }
    }

    /// Check if the token at head has the given lexeme.
    fn recognize_token(&self, lexeme: &Lexeme, head: usize, tokens: &[Token]) -> bool {
        match tokens.get(head) {
            Some(token) => &token.lexeme == lexeme,
            None => false,
        }
    }
}

impl Default for Parser {
    fn default() -> Self {
        Self::new()
    }
}
