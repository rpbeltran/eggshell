package lexer

type MaxMunchResult struct {
	token  TokenType
	length int
}

type mmNode struct {
	children map[byte]mmNode
	terminal bool
	result   MaxMunchResult
}

func newMMNode(depth int, patterns map[string]TokenType) mmNode {
	children := make(map[byte]mmNode)
	child_data := make(map[byte](map[string]TokenType))

	terminal := false
	var result MaxMunchResult

	for pattern, token := range patterns {
		if len(pattern) == depth {
			terminal = true
			result = MaxMunchResult{
				token:  token,
				length: depth,
			}
		} else {
			c := pattern[depth]
			if child_data[c] == nil {
				child_data[c] = make(map[string]TokenType)
			}
			child_data[c][pattern] = token
		}
	}
	for head, data := range child_data {
		children[head] = newMMNode(depth+1, data)
	}
	return mmNode{
		children: children,
		terminal: terminal,
		result:   result,
	}
}

type MaxMuchTrie struct {
	root      mmNode
	FirstByte map[byte]bool
}

func NewMMTrie(patterns map[string]TokenType) MaxMuchTrie {
	first_bytes := make(map[byte]bool)
	for pattern := range patterns {
		first_bytes[pattern[0]] = true
	}

	return MaxMuchTrie{
		root:      newMMNode(0, patterns),
		FirstByte: first_bytes,
	}
}

func (trie *MaxMuchTrie) LargestPrefix(data string, start_from int) (MaxMunchResult, bool) {
	var head *mmNode
	head = &trie.root
	for i := start_from; i < len(data); i++ {
		c := data[i]
		if child, has_child := head.children[c]; has_child {
			head = &child
		} else {
			break
		}
	}
	if head.terminal {
		return head.result, true
	}
	return MaxMunchResult{}, false
}
