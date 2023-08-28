
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

program := exec_chain*

## Pipelines

exec_chain := exec pipe_exec
           |  exec redirect_exec
           |  exec

exec := STRING_LITERAL+

pipe_exec := PIPE exec_chain

redirect_exec := (REDIRECT | REDIRECT_APPEND) redirect_target

redirect_target := STRING_LITERAL (pipe_exec | redirect_exec)?
