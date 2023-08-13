use std::collections::VecDeque;
use std::fmt::Write;

use egg_grammar::*;

use crate::errors::*;

/// Building block of a parse gen rule.
/// usize typed blocks refer to arena style IDs of other blocks.
#[derive(Debug)]
pub enum Block {
    /// Match a parsed AST symbol.
    Symbol(Symbol),
    /// Match a token.
    Token(Lexeme),

    /// Denote Conjunction operator: (X1  X2  X3 ...)
    /// Should not be directly instantiated outside of metaparse implementation.
    _Sequence(Vec<usize>),
    /// Denote Disjunction operator: (X1 | X2 | X3 | ...)
    /// Should not directly be instantiated outside of metaparse implementation.
    _Any(Vec<usize>),
    /// Denote Optionals: X?.
    /// Should not be directly instantiated outside of metaparse implementation.
    _Maybe(usize),
    /// Denote Kleene Closures: X*
    /// Should not be directly instantiated outside of metaparse implementation.
    _Star(usize),
    /// Denote Nonempty Kleene Closures: X+
    /// Should not be directly instantiated outside of metaparse implementation.
    _Plus(usize),
    /// Denote discard subtree.
    /// Should not be directly instantiated outside of metaparse implementation.
    _Discard(usize),
}

#[derive(Debug)]
pub struct Rule {
    pub blocks: Vec<Block>,
    pub root: usize,
}

impl Rule {
    /// Construct a Rule to match a symbol.
    pub fn from_sym(symbol: Symbol) -> Self {
        Self::from(Block::Symbol(symbol))
    }

    /// Construct a Rule to match a token.
    pub fn from_tok(lexeme: Lexeme) -> Self {
        Self::from(Block::Token(lexeme))
    }

    /// Construct a Rule to match an block.
    pub fn from(block: Block) -> Self {
        Self {
            blocks: vec![block],
            root: 0,
        }
    }

    pub fn get_root(&mut self) -> &mut Block {
        self.blocks.get_mut(self.root).unwrap()
    }

    /// Match this concatenated with another rule.
    pub fn then(mut self, mut rule: Rule) -> Self {
        // new_blocks : [ old_blocks | new_blocks | seq? ]

        let old_len = self.blocks.len();
        rule.increment_blocks(old_len);
        self.blocks.append(&mut rule.blocks);

        let rule_root_i = rule.root + old_len;

        if let Block::_Sequence(children) = self.get_root() {
            children.push(rule_root_i);
        } else if let Block::_Sequence(rule_children) = self.blocks.get_mut(rule_root_i).unwrap() {
            // Add the current root to the start of the new rule's sequence
            rule_children.insert(0, self.root);
            self.root = rule_root_i;
        } else {
            self.blocks
                .push(Block::_Sequence(vec![self.root, rule_root_i]));
            self.root = self.blocks.len() - 1;
        }
        self
    }

    fn increment_blocks(&mut self, offset: usize) {
        fn inc_vec(v: &mut [usize], offset: usize) {
            v.iter_mut().for_each(|x| *x += offset);
        }

        for block in self.blocks.iter_mut() {
            match block {
                Block::_Sequence(children) => inc_vec(children, offset),
                Block::_Any(children) => inc_vec(children, offset),
                Block::_Maybe(child) => *child += offset,
                Block::_Star(child) => *child += offset,
                Block::_Plus(child) => *child += offset,
                Block::_Discard(child) => *child += offset,
                Block::Symbol(_) => {}
                Block::Token(_) => {}
            }
        }
    }

    /// Match this concatenated with an blocks.
    pub fn then_block(mut self, block: Block) -> Self {
        self.blocks.push(block);
        let new_id = self.blocks.len() - 1;
        if let Block::_Sequence(children) = self.get_root() {
            children.push(new_id);
        } else {
            self.blocks.push(Block::_Sequence(vec![self.root, new_id]));
            self.root = new_id + 1;
        }
        self
    }

    /// Match this concatenated with a symbol.
    pub fn then_sym(self, symbol: Symbol) -> Self {
        self.then_block(Block::Symbol(symbol))
    }

    /// Match this concatenated with a token.
    pub fn then_tok(self, lexeme: Lexeme) -> Self {
        self.then_block(Block::Token(lexeme))
    }

    /// Match this then one of the following.
    pub fn then_one_of(mut self, blocks: &mut Vec<Block>) -> Self {
        // blocks = [ old_blocks | new_blocks | any | sequence? ]
        let any_block =
            Block::_Any((self.blocks.len()..self.blocks.len() + blocks.len()).collect());
        self.blocks.append(blocks);
        self.blocks.push(any_block);
        let any_id = self.blocks.len() - 1;

        if let Block::_Sequence(blocks) = self.get_root() {
            blocks.push(any_id);
        } else {
            self.blocks.push(Block::_Sequence(vec![self.root, any_id]));
            self.root = self.blocks.len() - 1;
        }
        self
    }

    /// Match this then maybe the following.
    pub fn then_maybe(mut self, block: Block) -> Self {
        // blocks = [ old_blocks | new_block | maybe | sequence? ]
        let maybe_block = Block::_Maybe(self.blocks.len());
        self.blocks.push(block);
        self.blocks.push(maybe_block);
        let any_id = self.blocks.len() - 1;

        if let Block::_Sequence(blocks) = self.get_root() {
            blocks.push(any_id);
        } else {
            self.blocks.push(Block::_Sequence(vec![self.root, any_id]));
            self.root = self.blocks.len() - 1;
        }
        self
    }

    /// Match this then possibly any amount of the new block.
    pub fn then_star(mut self, block: Block) -> Self {
        // blocks = [ old_blocks | new_block | maybe | sequence? ]
        let maybe_block = Block::_Star(self.blocks.len());
        self.blocks.push(block);
        self.blocks.push(maybe_block);
        let any_id = self.blocks.len() - 1;

        if let Block::_Sequence(blocks) = self.get_root() {
            blocks.push(any_id);
        } else {
            self.blocks.push(Block::_Sequence(vec![self.root, any_id]));
            self.root = self.blocks.len() - 1;
        }
        self
    }

    /// Match this then one or more of the new block.
    pub fn then_plus(mut self, block: Block) -> Self {
        // blocks = [ old_blocks | new_block | maybe | sequence? ]
        let maybe_block = Block::_Plus(self.blocks.len());
        self.blocks.push(block);
        self.blocks.push(maybe_block);
        let any_id = self.blocks.len() - 1;

        if let Block::_Sequence(blocks) = self.get_root() {
            blocks.push(any_id);
        } else {
            self.blocks.push(Block::_Sequence(vec![self.root, any_id]));
            self.root = self.blocks.len() - 1;
        }
        self
    }

    /// Match this or another rule.
    pub fn or(mut self, mut rule: Rule) -> Self {
        // new_blocks : [ old_blocks | new_blocks | any? ]

        let old_len = self.blocks.len();
        rule.increment_blocks(old_len);
        self.blocks.append(&mut rule.blocks);

        let rule_root_i = rule.root + old_len;

        if let Block::_Any(children) = self.get_root() {
            children.push(rule_root_i);
        } else if let Block::_Any(rule_children) = self.blocks.get_mut(rule_root_i).unwrap() {
            // Add the current root to the start of the new rule's sequence
            rule_children.insert(0, self.root);
            self.root = rule_root_i;
        } else {
            self.blocks.push(Block::_Any(vec![self.root, rule_root_i]));
            self.root = self.blocks.len() - 1;
        }
        self
    }

    /// Match this or a block.
    fn or_block(mut self, block: Block) -> Self {
        self.blocks.push(block);
        let new_id = self.blocks.len() - 1;
        if let Block::_Any(blocks) = self.get_root() {
            blocks.push(new_id);
        } else {
            self.blocks.push(Block::_Any(vec![self.root, new_id]));
            self.root = new_id + 1;
        }
        self
    }

    /// Match this or a symbol.
    pub fn or_sym(self, symbol: Symbol) -> Self {
        self.or_block(Block::Symbol(symbol))
    }

    /// Match this or an token.
    pub fn or_tok(self, lexeme: Lexeme) -> Self {
        self.or_block(Block::Token(lexeme))
    }

    /// Match one or zero of this.
    pub fn maybe(mut self) -> Self {
        self.blocks.push(Block::_Maybe(self.root));
        self.root = self.blocks.len() - 1;
        self
    }

    /// Match zero or more of this.
    pub fn star(mut self) -> Self {
        self.blocks.push(Block::_Star(self.root));
        self.root = self.blocks.len() - 1;
        self
    }

    /// Match one or zero of this.
    pub fn plus(mut self) -> Self {
        self.blocks.push(Block::_Plus(self.root));
        self.root = self.blocks.len() - 1;
        self
    }

    /// Don't include this subtree in the AST.
    pub fn discard(mut self) -> Self {
        self.blocks.push(Block::_Discard(self.root));
        self.root = self.blocks.len() - 1;
        self
    }

    pub fn to_string(&self) -> Result<String> {
        let mut buffer = String::from("---\n");
        let mut queue: VecDeque<(usize, usize)> = VecDeque::from([(self.root, 0)]);
        while !queue.is_empty() {
            let (node_id, depth) = queue
                .pop_front()
                .expect("Failed to pop node from tree display queue");
            let node = self
                .blocks
                .get(node_id)
                .ok_or(Error::ParserTreeNodeOutOfBounds)?;
            let indent = " ".repeat(depth * 2) + "- ";

            let children = match node {
                Block::Symbol(_) => Vec::new(),
                Block::Token(_) => Vec::new(),
                Block::_Sequence(children) => children.clone(),
                Block::_Any(children) => children.clone(),
                Block::_Maybe(child) => vec![*child],
                Block::_Star(child) => vec![*child],
                Block::_Plus(child) => vec![*child],
                Block::_Discard(child) => vec![*child],
            };

            match node {
                Block::Symbol(sym) => writeln!(&mut buffer, "{indent}Symbol<{:?}>", sym).unwrap(),
                Block::Token(tok) => writeln!(&mut buffer, "{indent}Token<{:?}>", tok).unwrap(),
                Block::_Sequence(_) => writeln!(&mut buffer, "{indent}Sequence").unwrap(),
                Block::_Any(_) => writeln!(&mut buffer, "{indent}Any").unwrap(),
                Block::_Maybe(_) => writeln!(&mut buffer, "{indent}Maybe").unwrap(),
                Block::_Star(_) => writeln!(&mut buffer, "{indent}Star").unwrap(),
                Block::_Plus(_) => writeln!(&mut buffer, "{indent}Plus").unwrap(),
                Block::_Discard(_) => writeln!(&mut buffer, "{indent}Discard").unwrap(),
            };

            for child_id in children.iter().rev() {
                queue.push_front((*child_id, depth + 1));
            }
        }
        Ok(buffer)
    }
}
