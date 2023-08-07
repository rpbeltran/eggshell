
# This Document is a WIP

# Tokens

## Commands
- COMMAND

## Data
- STRING_LITERAL

## Redirection operators
- PIPE
- REDIRECT
- REDIRECT_APPEND


# Grammar

// todo: refactor to accept empty programs
program := exec_chain*

## Pipelines

exec_chain := exec_single pipe_exec
           |  exec_single redirect_exec
           |  exec_single

exec := COMMAND STRING_LITERAL*

pipe_exec := PIPE exec_chain

redirect_exec := (REDIRECT | REDIRECT_APPEND) redirect_target

redirect_target := STRING_LITERAL (pipe_exec | redirect_exec)?
