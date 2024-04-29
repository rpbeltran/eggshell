// NOLINTBEGIN(bugprone-unchecked-optional-access)
// NOLINTBEGIN(*-non-private-member-variables-in-classes)
#include <cassert>
#include <memory>
#include <optional>
#include <string>
#include <unordered_map>
#include <vector>

#include "gtest/gtest.h"

#include "../instruction/instructionArgs.h"
#include "../instruction/instructions.h"
#include "./flags.h"
#include "./instructionParser.h"

using namespace YolkParser;  // NOLINT(*-build-using-namespace)

class TestInstruction : public Instructions::StartInstruction {
 public:
  bool hasReqNone{false};
  Instructions::NameArgument reqName;
  Instructions::NumberArgument reqNum;
  Instructions::BooleanArgument reqBool;

  bool hasOptNone{false};
  bool hasOptName{false};
  bool hasOptNum{false};
  bool hasOptBool{false};
  Instructions::NameArgument optName;
  Instructions::NumberArgument optNum;
  Instructions::BooleanArgument optBool;
};

class TestParser : public InstructionParser<TestInstruction> {
  static std::vector<Flag> _required_flags;
  static std::vector<Flag> _optional_flags;

  auto parse_flags(std::unordered_map<std::string, std::optional<FlagValue>> &
                       flags) -> TestInstruction override {
    TestInstruction inst;

    assert(!flags["reqNone"].has_value());

    inst.hasReqNone = true;
    inst.reqName.set_refid(flags["reqName"].value().value);
    inst.reqNum.set_val(flags["reqNum"].value().value);
    inst.reqBool.set_val(flags["reqBool"].value().value);

    if (flags.contains("optNone")) {
      assert(!flags["optNone"].has_value());
      inst.hasOptNone = true;
    } else {
      inst.hasOptNone = false;
    }
    if (flags.contains("optName")) {
      inst.optName.set_refid(flags["optName"].value().value);
      inst.hasOptName = true;
    } else {
      inst.hasOptName = false;
    }
    if (flags.contains("optNum")) {
      inst.optNum.set_val(flags["optNum"].value().value);
      inst.hasOptNum = true;
    } else {
      inst.hasOptNum = false;
    }
    if (flags.contains("optBool")) {
      inst.optBool.set_val(flags["optBool"].value().value);
      inst.hasOptBool = true;
    } else {
      inst.hasOptBool = false;
    }
    return inst;
  }

 public:
  explicit TestParser()
      : InstructionParser<TestInstruction>(
            std::make_shared<std::vector<Flag>>(_required_flags),
            std::make_shared<std::vector<Flag>>(_optional_flags)) {}
};

std::vector<Flag> TestParser::_required_flags = {
    Flag("reqNone", None),
    Flag("reqName", RefID),
    Flag("reqNum", Num),
    Flag("reqBool", Bool),
};

std::vector<Flag> TestParser::_optional_flags = {
    Flag("optNone", None),
    Flag("optName", RefID),
    Flag("optNum", Num),
    Flag("optBool", Bool),
};

TEST(InstructionParser, parseReqOnly) {
  TestParser test_parser;

  const std::vector<std::string> args = {"--reqNone", "--reqName", "<13>", "--reqNum",
                                   "7",         "--reqBool", "true"};

  auto maybe_inst = test_parser.parse(args);

  ASSERT_TRUE(maybe_inst.has_value());

  auto inst = maybe_inst.value();

  EXPECT_TRUE(inst.hasReqNone);
  EXPECT_EQ(inst.reqName.get_refid(), 13);
  EXPECT_EQ(inst.reqNum.get_val(), 7);
  EXPECT_EQ(inst.reqBool.get_val(), 1);

  EXPECT_FALSE(inst.hasOptNone);
  EXPECT_FALSE(inst.hasOptName);
  EXPECT_FALSE(inst.hasOptNum);
  EXPECT_FALSE(inst.hasOptBool);
}

TEST(InstructionParser, parseOpt) {
  TestParser test_parser;

  const std::vector<std::string> args = {
      "--reqNone", "--reqName", "<13>",      "--reqNum",  "7",
      "--reqBool", "true",      "--optNone", "--optName", "<99999>",
      "--optNum",  "78",        "--optBool", "true"};

  auto maybe_inst = test_parser.parse(args);

  ASSERT_TRUE(maybe_inst.has_value());

  auto inst = maybe_inst.value();

  EXPECT_TRUE(inst.hasReqNone);
  EXPECT_EQ(inst.reqName.get_refid(), 13);
  EXPECT_EQ(inst.reqNum.get_val(), 7);
  EXPECT_EQ(inst.reqBool.get_val(), 1);

  EXPECT_TRUE(inst.hasOptNone);
  EXPECT_EQ(inst.optName.get_refid(), 99999);
  EXPECT_EQ(inst.optNum.get_val(), 78);
  EXPECT_EQ(inst.optBool.get_val(), 1);
}

TEST(InstructionParser, parseOptMissingRequired) {
  TestParser test_parser;

  const std::vector<std::string> args = {"--reqNone", "--reqName", "<13>", "--reqNum",
                                   "7"};
  auto maybe_inst = test_parser.parse(args);
  EXPECT_FALSE(maybe_inst.has_value());
}

TEST(InstructionParser, parseOptMissingBoolLit) {
  TestParser test_parser;

  const std::vector<std::string> args = {"--reqNone", "--reqName", "<13>",
                                   "--reqNum",  "7",         "--reqBool"};
  auto maybe_inst = test_parser.parse(args);
  EXPECT_FALSE(maybe_inst.has_value());
}

TEST(InstructionParser, parseOptMissingNumLit) {
  TestParser test_parser;

  const std::vector<std::string> args = {"--reqNone", "--reqName", "<13>",
                                   "--reqNum",  "--reqBool", "true"};
  auto maybe_inst = test_parser.parse(args);
  EXPECT_FALSE(maybe_inst.has_value());
}

TEST(InstructionParser, parseOptMissingNameLit) {
  TestParser test_parser;

  const std::vector<std::string> args = {"--reqNone", "--reqName", "--reqNum",
                                   "7",         "--reqBool", "true"};
  auto maybe_inst = test_parser.parse(args);
  EXPECT_FALSE(maybe_inst.has_value());
}

TEST(InstructionParser, parseOptNoneHasArg) {
  TestParser test_parser;

  const std::vector<std::string> args = {"--reqNone", "7", "--reqName", "<13>",
                                   "--reqNum",  "7", "--reqBool", "true"};
  auto maybe_inst = test_parser.parse(args);
  EXPECT_FALSE(maybe_inst.has_value());
}

TEST(InstructionParser, parseOptLitHasRef) {
  TestParser test_parser;

  const std::vector<std::string> args = {"--reqNone", "--reqName", "<13>", "--reqNum",
                                   "<7>",       "--reqBool", "true"};
  auto maybe_inst = test_parser.parse(args);
  EXPECT_FALSE(maybe_inst.has_value());
}

TEST(InstructionParser, parseOptRefHasLit) {
  TestParser test_parser;

  const std::vector<std::string> args = {"--reqNone", "--reqName", "13",  "--reqNum",
                                   "7",         "--reqBool", "true"};
  auto maybe_inst = test_parser.parse(args);
  EXPECT_FALSE(maybe_inst.has_value());
}

// NOLINTEND(*-non-private-member-variables-in-classes)
// NOLINTEND(bugprone-unchecked-optional-access)