use std::collections::VecDeque;

use crate::ast::*;

#[cfg(test)]
use crate::errors::*;

pub struct PostOrderAstIterator<'a> {
    ast: &'a Ast,
    queue: VecDeque<(usize, usize)>,
    root: Option<usize>,
    child_index: usize,
    postorder: VecDeque<usize>,
}

impl<'a> Iterator for PostOrderAstIterator<'a> {
    type Item = (usize, &'a AstNode);
    fn next(&mut self) -> Option<Self::Item> {
        self.postorder.pop_front().map(|next_i| {
            (
                next_i,
                self.ast
                    .get_node(next_i)
                    .expect("Iterator pointed to node out of bounds"),
            )
        })
    }
}

impl<'a> PostOrderAstIterator<'a> {
    pub fn new(ast: &'a Ast) -> Self {
        let mut iter = Self {
            ast,
            queue: VecDeque::from([]),
            root: Some(0),
            child_index: 0,
            postorder: VecDeque::new(),
        };
        iter.compute_post_order();
        iter
    }

    fn compute_post_order(&mut self) {
        loop {
            if let Some(root) = self.root {
                self.queue.push_back((root, self.child_index));
                self.child_index = 0;
                let root_children = &self
                    .ast
                    .nodes
                    .get(root)
                    .expect("Traversal went out of bounds")
                    .children;
                if root_children.is_empty() {
                    self.root = None;
                } else {
                    self.root = Some(root_children[0])
                }
            } else if !self.queue.is_empty() {
                let (mut temp, mut temp_childindex) =
                    self.queue.pop_back().expect("Traversal popped empty queue");
                self.postorder.push_back(temp);

                while !self.queue.is_empty() {
                    let (peek, _) = *self.queue.back().expect("Traversal popped empty queue");
                    if temp_childindex
                        != &self
                            .ast
                            .nodes
                            .get(peek)
                            .expect("Traversal went out of bounds")
                            .children
                            .len()
                            - 1
                    {
                        break;
                    }
                    (temp, temp_childindex) =
                        self.queue.pop_back().expect("Traversal popped empty queue");
                    self.postorder.push_back(temp);
                }

                if !self.queue.is_empty() {
                    let (peek, _) = *self.queue.back().expect("Traversal popped empty queue");
                    let peek_children = &self
                        .ast
                        .nodes
                        .get(peek)
                        .expect("Traversal went out of bounds")
                        .children;
                    self.root = Some(*peek_children.get(temp_childindex + 1).expect("msg"));
                    self.child_index = temp_childindex + 1;
                }
            } else {
                break;
            }
        }
    }
}

#[test]
fn test_postorder() -> Result<()> {
    let ast = crate::test_utils::example_ast();

    let expected_postorder: Vec<usize> = Vec::from([
        3, 4, 2, 6, 9, 8, 11, 14, 13, 16, 18, 17, 15, 12, 10, 7, 5, 1, 21, 22, 20, 24, 26, 25, 23,
        19, 0,
    ]);
    let postorder: Vec<usize> = PostOrderAstIterator::new(&ast).map(|(i, _)| i).collect();
    egg_testutils::utils::assert_vecs_equal(&expected_postorder, &postorder)
        .map_err(Error::TestCaseFailedAssertion)
}
