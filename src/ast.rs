use std::collections::VecDeque;

use std::fmt::Write;

extern crate yaml_rust;

use crate::egg_error::*;
use crate::parser::Symbol;
use crate::source::SourceManager;
use crate::token::Token;

#[derive(Debug)]
pub struct Ast {
    pub nodes: Vec<AstNode>,
}

#[derive(Debug)]
pub struct AstNode {
    pub symbol: Symbol,
    pub children: Vec<usize>,
    pub token: Option<usize>,
}

impl Ast {
    /// Returns a reference to the AST's root node, or an error if none exists.
    pub fn get_root(&self) -> Result<&AstNode> {
        self.nodes.get(0).ok_or(EggError::ParserTreeHasNoRootNode)
    }

    /// Returns a reference to the AST's root node, or an error if none exists.
    pub fn get_root_mut(&mut self) -> Result<&mut AstNode> {
        self.nodes
            .get_mut(0)
            .ok_or(EggError::ParserTreeHasNoRootNode)
    }

    /// Add all the nodes in a syntax tree to this tree.
    /// Make the root of the tree being added a child of the current tree's root.
    pub fn hang_child(mut self, mut child_tree: Ast) -> Result<Self> {
        if matches!(child_tree.get_root()?.symbol, Symbol::_Placeholder) {
            return Err(EggError::ParserReceivedPlaceholder);
        }
        let current_size = self.nodes.len();
        child_tree.offset_ids(current_size);
        self.get_root_mut()?.children.push(current_size);
        self.nodes.append(child_tree.nodes.as_mut());
        Ok(self)
    }

    /// Add all the nodes in a syntax tree to this tree except the placeholder.
    /// Make the root of the tree being added a child of the current tree's root.
    pub fn hang_from_placeholder(mut self, mut child_tree: Ast) -> Result<Self> {
        if !matches!(child_tree.get_root()?.symbol, Symbol::_Placeholder) {
            return Err(EggError::ParserExpectedPlaceholder);
        }
        child_tree.offset_ids(self.nodes.len() - 1);
        let mut child_root = child_tree.nodes.remove(0);
        self.nodes.append(&mut child_tree.nodes);
        self.get_root_mut()?
            .children
            .append(&mut child_root.children);

        Ok(self)
    }

    /// Add a new node to the syntax tree as a child of the root.
    pub fn add_child(mut self, child_node: AstNode) -> Result<Self> {
        let current_size = self.nodes.len();
        self.get_root_mut()?.children.push(current_size);
        self.nodes.push(child_node);
        Ok(self)
    }

    /// Add offset to all node_ids.
    fn offset_ids(&mut self, offset: usize) {
        for node in self.nodes.iter_mut() {
            node.children = node.children.iter().map(|i| i + offset).collect();
        }
    }

    /// Serialize abstract syntax tree with yaml formatting.
    pub fn to_string(&self, tokens: &[Token], source_manager: &SourceManager) -> Result<String> {
        let mut buffer = String::from("---\n");
        let mut queue: VecDeque<(usize, usize)> = VecDeque::from([(0, 0)]);
        while !queue.is_empty() {
            let (node_id, depth) = queue
                .pop_front()
                .expect("Failed to pop node from tree display queue");
            let node = self
                .nodes
                .get(node_id)
                .ok_or(EggError::ParserTreeNodeOutOfBounds)?;
            let children = &self
                .nodes
                .get(node_id)
                .ok_or(EggError::ParserTreeHasNoRootNode)?
                .children;
            let indent = " ".repeat(depth * 2) + "- ";
            match node.symbol {
                Symbol::Lexeme => {
                    let tok = tokens
                        .get(node.token.ok_or(EggError::ParserLexemeNodeMissingToken)?)
                        .ok_or(EggError::ParserTokenOutOfBounds)?;
                    writeln!(&mut buffer, "{indent}{:?}:", tok.lexeme).unwrap();
                    writeln!(
                        &mut buffer,
                        "  {indent}{:?}",
                        tok.get_contents(source_manager)?
                    )
                    .unwrap()
                }
                _ => {
                    if children.is_empty() {
                        writeln!(&mut buffer, "{indent}{:?}", node.symbol).unwrap()
                    } else {
                        writeln!(&mut buffer, "{indent}{:?}:", node.symbol).unwrap()
                    }
                }
            };
            for child_id in children.iter().rev() {
                queue.push_front((*child_id, depth + 1));
            }
        }
        Ok(buffer)
    }

    /// Serialize abstract syntax tree to a vector of YAML node.
    pub fn to_yaml(
        &self,
        tokens: &[Token],
        source_manager: &SourceManager,
    ) -> Result<yaml_rust::Yaml> {
        let as_string = self.to_string(tokens, source_manager)?;
        let as_yaml = yaml_rust::YamlLoader::load_from_str(as_string.as_str()).expect("");
        Ok(as_yaml[0].clone()) // todo: get rid of the need for this clone
    }

    /// Serialize abstract syntax tree to a string then to a YAML node and then back to a string.
    /// This should normally not be used outside of tests comparing the output to generated yaml.
    pub fn to_string_standardized(
        &self,
        tokens: &[Token],
        source_manager: &SourceManager,
    ) -> Result<String> {
        let mut as_yaml = String::new();
        yaml_rust::YamlEmitter::new(&mut as_yaml)
            .dump(&self.to_yaml(tokens, source_manager)?)
            .unwrap();
        Ok(as_yaml)
    }
}
