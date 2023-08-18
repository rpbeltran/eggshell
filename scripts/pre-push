#!/bin/bash -euo pipefail

# Presubmit checks to match Github Actions

#
# How you would implement this in egg:
# Note: unsupported syntax is naturally subject to change
#
# fn run_test(cmd) {
#     (async --quet `@cmd`).then(say @cmd ++ _.ok ? "OK." : "FAILED!!!")
# }
# run_test "cargo build --workspace --verbose"
# run_test "cargo test  --workspace --verbose"
# run_test "cargo clippy --workspace -- -D warnings"
# run_test "cargo fmt --check --all"
#

run_test() {
    out=$($1 2>&1) || (echo -e "\`$1\`:  FAILED!!! \n\n$out" && false)
    echo "\`$1\`:  OK."
}

run_test "cargo build --workspace --verbose" &
run_test "cargo test  --workspace --verbose" &
run_test "cargo clippy --workspace -- -D warnings" &
run_test "cargo fmt --check --all" &

wait
