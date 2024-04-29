#include <optional>

#include "gtest/gtest.h"

#include "./flags.h"

using namespace YolkParser;

const auto reference_value = std::optional<FlagValue>{FlagValue{.value=0, .is_reference=true}};
const auto literal_value = std::optional<FlagValue>{FlagValue{.value=0, .is_reference=false}};
const auto none_value = std::optional<FlagValue>{};

TEST(ParserFlags, ValidateRefID) {
  auto flag = Flag("foo", RefID);

  EXPECT_TRUE(flag.validate(reference_value));
  EXPECT_FALSE(flag.validate(literal_value));
  EXPECT_FALSE(flag.validate(none_value));
}

TEST(ParserFlags, ValidateNum) {
  auto flag = Flag("foo", Num);

  EXPECT_FALSE(flag.validate(reference_value));
  EXPECT_TRUE(flag.validate(literal_value));
  EXPECT_FALSE(flag.validate(none_value));
}

TEST(ParserFlags, ValidateVoid) {
  auto flag = Flag("foo", None);

  EXPECT_FALSE(flag.validate(reference_value));
  EXPECT_FALSE(flag.validate(literal_value));
  EXPECT_TRUE(flag.validate(none_value));
}

TEST(ParserFlags, ValidateBool) {
  auto flag = Flag("foo", Bool);

  EXPECT_FALSE(flag.validate(reference_value));
  EXPECT_TRUE(flag.validate(literal_value));
  EXPECT_FALSE(flag.validate(none_value));
}