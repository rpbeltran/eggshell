#include <vector>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include "lexer.h"
#include "sources.h"
#include "tokens.h"


PYBIND11_MODULE(lexer, m) {
  m.doc() = "Lexing module for eggshell.";

  py::enum_<TokenKind>(m, "TokenKind")
      .value("CURLY_OPEN", TokenKind::CURLY_OPEN)
      .value("CURLY_CLOSE", TokenKind::CURLY_CLOSE)
      .value("PAREN_OPEN", TokenKind::PAREN_OPEN)
      .value("PAREN_CLOSE", TokenKind::PAREN_CLOSE)
      .value("SQUARE_OPEN", TokenKind::SQUARE_OPEN)
      .value("SQUARE_CLOSE", TokenKind::SQUARE_CLOSE)
      .export_values();

  py::class_<SourceSlice>(m, "SourceSlice")
      .def(py::init<uintptr_t, uintptr_t>())
      .def_property_readonly("offset", &SourceSlice::get_offset)
      .def_property_readonly("length", &SourceSlice::get_length);

  py::class_<Token>(m, "Token")
      .def(py::init<TokenKind, SourceSlice>())
      .def_property_readonly("kind", &Token::get_kind)
      .def_property_readonly("location", &Token::get_location);

  m.def("lex", &lex, "Get tokens from source string");
}
