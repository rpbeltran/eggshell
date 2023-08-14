use std::collections::VecDeque;

use std::fmt::Write;

use egg_grammar::Symbol;
use egg_source::source_manager::SourceManager;
use egg_source::token::Token;

use crate::annotations::Annotations;
use crate::errors::*;
use crate::iterators::*;

#[derive(Debug)]
pub struct Ast {
    pub nodes: Vec<AstNode>,
}

#[derive(Debug, PartialEq)]
pub struct AstNode {
    pub symbol: Symbol,
    pub children: Vec<usize>,
    pub token: Option<usize>,
    pub annotations: Annotations,
}

impl<'a> Ast {
    /// Returns a reference to the AST's root node, or an error if none exists.
    pub fn get_root(&self) -> Result<&AstNode> {
        self.nodes.get(0).ok_or(Error::ParserTreeHasNoRootNode)
    }

    /// Returns a reference to the AST's root node, or an error if none exists.
    pub fn get_root_mut(&mut self) -> Result<&mut AstNode> {
        self.nodes.get_mut(0).ok_or(Error::ParserTreeHasNoRootNode)
    }

    /// Returns a reference to one of the ASTs nodes, or an error if the index does not exist.
    pub fn get_node(&self, i: usize) -> Result<&AstNode> {
        self.nodes.get(i).ok_or(Error::ParserTreeNodeOutOfBounds)
    }

    /// Returns a reference to one of the ASTs nodes, or an error if the index does not exist.
    pub fn get_node_mut(&mut self, i: usize) -> Result<&mut AstNode> {
        self.nodes
            .get_mut(i)
            .ok_or(Error::ParserTreeNodeOutOfBounds)
    }

    /// Add all the nodes in a syntax tree to this tree.
    /// Make the root of the tree being added a child of the current tree's root.
    pub fn hang_child(mut self, mut child_tree: Ast) -> Result<Self> {
        if matches!(child_tree.get_root()?.symbol, Symbol::_Placeholder) {
            return Err(Error::ParserReceivedPlaceholder);
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
            return Err(Error::ParserExpectedPlaceholder);
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
                .ok_or(Error::ParserTreeNodeOutOfBounds)?;
            let children = &self
                .nodes
                .get(node_id)
                .ok_or(Error::ParserTreeHasNoRootNode)?
                .children;
            let indent = " ".repeat(depth * 2) + "- ";
            match node.symbol {
                Symbol::Lexeme => {
                    let tok = tokens
                        .get(node.token.ok_or(Error::ParserLexemeNodeMissingToken)?)
                        .ok_or(Error::ParserTokenOutOfBounds)?;
                    writeln!(&mut buffer, "{indent}{:?}:", tok.lexeme).unwrap();
                    writeln!(
                        &mut buffer,
                        "  {indent}{:?}",
                        tok.get_contents(source_manager)
                            .map_err(Error::SourceError)?
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

    pub fn postorder(&'a self) -> PostOrderAstIterator<'a> {
        PostOrderAstIterator::new(self)
    }
}
