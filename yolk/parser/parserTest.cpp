#include <string>
#include <vector>

#include "gtest/gtest.h"

#include "./parser.h"

using namespace YolkParser;  // NOLINT(*-build-using-namespace)

TEST(YolkParser, parseLines) {

  const std::vector<std::string> lines = {"",
                                          "start-expression",
                                          "",
                                          "eval",
                                          "eval --discard",
                                          "push-name --ref <0>",
                                          "push-num --val 1",
                                          "push-str --ref <0>",
                                          "push-bool --val false",
                                          ""};
  const int empty_lines = 3;

  Parser parser(lines);

  EXPECT_FALSE(parser.has_error());
  EXPECT_EQ(parser.instruction_count(), lines.size() - empty_lines);
}

TEST(YolkParser, parseBadLines) {
  const std::vector<std::string> lines = {"start-expression --unknown_arg"};
  Parser parser(lines);
  EXPECT_TRUE(parser.has_error());
}