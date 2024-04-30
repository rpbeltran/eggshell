// NOLINTBEGIN(bugprone-unchecked-optional-access)
#include <optional>
#include <string>
#include <vector>

#include "gtest/gtest.h"

#include "./instructionParsers.h"

using namespace YolkParser;  // NOLINT(*-build-using-namespace)

TEST(InstructionParsers, parseStartExpression) {
  StartExpressionParser parser;

  const std::vector<std::string> args = {};

  auto maybe_inst = parser.parse(args);
  ASSERT_TRUE(maybe_inst.has_value());
}

TEST(InstructionParsers, parseEval) {
  // Test `eval`

  EvalParser parser;
  const std::vector<std::string> args = {};

  auto maybe_inst = parser.parse(args);
  ASSERT_TRUE(maybe_inst.has_value());

  EXPECT_FALSE(maybe_inst.value()->get_discard().get_val());

  // Test `eval --discard`

  EvalParser p_discard;
  const std::vector<std::string> args_discard = {"--discard"};

  auto maybe_inst_discard = p_discard.parse(args_discard);
  ASSERT_TRUE(maybe_inst_discard.has_value());

  EXPECT_TRUE(maybe_inst_discard.value()->get_discard().get_val());
}

TEST(InstructionParsers, parsePushName) {
  // Test `push-name --ref <1234567>`

  PushNameParser parser;
  const std::vector<std::string> args = {"--ref", "<1234567>"};

  auto maybe_inst = parser.parse(args);
  ASSERT_TRUE(maybe_inst.has_value());

  EXPECT_EQ(maybe_inst.value()->get_val().get_refid(), 1234567);
}

TEST(InstructionParsers, parsePushNumber) {
  // Test `push-num --val 1234567

  PushNumParser parser;
  const std::vector<std::string> args = {"--val", "1234567"};

  auto maybe_inst = parser.parse(args);
  ASSERT_TRUE(maybe_inst.has_value());

  EXPECT_EQ(maybe_inst.value()->get_val().get_val(), 1234567);
}

TEST(InstructionParsers, parsePushString) {
  // Test `push-str --ref <1234567>`

  PushStringParser parser;
  const std::vector<std::string> args = {"--ref", "<1234567>"};

  auto maybe_inst = parser.parse(args);
  ASSERT_TRUE(maybe_inst.has_value());

  EXPECT_EQ(maybe_inst.value()->get_val().get_refid(), 1234567);
}

TEST(InstructionParsers, parsePushBool) {
  // Test `push-bool --val false`

  PushBoolParser p_false;
  const std::vector<std::string> args_false = {"--val", "false"};

  auto maybe_inst_false = p_false.parse(args_false);
  ASSERT_TRUE(maybe_inst_false.has_value());

  EXPECT_FALSE(maybe_inst_false.value()->get_val().get_val());

  // Test `push-bool --val true`

  PushBoolParser p_true;
  const std::vector<std::string> args_true = {"--val", "true"};

  auto maybe_inst_true = p_true.parse(args_true);
  ASSERT_TRUE(maybe_inst_true.has_value());

  EXPECT_TRUE(maybe_inst_true.value()->get_val().get_val());
}

// NOLINTEND(bugprone-unchecked-optional-access)