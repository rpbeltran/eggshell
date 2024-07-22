#pragma once
#include <cstdint>

#include "sources.h"

enum TokenKind {
  CURLY_OPEN = 0,
  CURLY_CLOSE,
  PAREN_OPEN,
  PAREN_CLOSE,
  SQUARE_OPEN,
  SQUARE_CLOSE
};

class Token {
  TokenKind kind;
  SourceSlice source;

 public:
  Token(TokenKind _kind, SourceSlice _source):
        kind(_kind), source(_source)
  {}

  const TokenKind & get_kind() {
    return kind;
  }

  const SourceSlice & get_location() {
    return source;
  }
};
