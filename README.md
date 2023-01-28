# eggshell

Egg is an Alternative Shell Language.

It intends to become a proper bash replacement both for productive terminal use and for scripting.
When used in a terminal Egg hopes to be more productive than Bash by offering more intuitive syntax
which means less time spent searching the internet to figure out how to do things. When used in
scripts, it intends to be more maintainable than Bash. Today, many scripts are written first and
Bash because they are doing things that Bash is good at like executing system commands and piping
the outputs to files, but later migrated to other languages like Python because large Bash scripts
are too difficult to maintain. Egg hopes to be a sort of middle ground here.

## Design Goals

Egg has goals:
* Egg should be a productive replacement for Bash when used interactively in terminal
* The syntax for Egg should be both simple and predictable to non-experts
* The syntax for Egg should be terse, and one liners should be facilitated for most tasks
* Scripting in Egg should be a maintainable endevour

Notably, some things are non-goals too:
* Compatibility with Bash syntax is a non-goal, though some basic syntax will be shared, and
generally where Egg differs from Bash there is a preference that the Bash syntax should error in Egg
as opposed to doing something subtly different.
* Blazing fast performance as a general purpose programmming language is a non-goal, as shell 
scripts normally spend most of their computation time inside of other executables anyways
* Although Egg has more typing than Bash, it does not attempt to achieve the level of type safety
found in many general purpose programmig languages

## Status
The status of Egg is that egg is still being drafted.
There is no set standard for Egg, only a laundry list of ideas and an interpretter is under
development but not ready. Currently, there is only support for producing Abstract Syntax Trees of
the most basic Egg Syntax.

## Examples

More documentation coming soon...