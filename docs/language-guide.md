
# THIS DOCUMENT IS A WIP AND DOES NOT GET UPDATED IN REAL TIME AS CHANGES ARE MADE
# THERE ARE ALREADY OUT OF DATE THINGS IN HERE THAT HAVE NOT BEEN UPDATED YET
# MORE DOCUMENTATION IS COMING SOON....

# Egg Language Overiew

This document presents a proposed specification for the egg shell language. It assumes familiarity
with Bash and will present much of the language via comparison to the equivalent Bash syntax when
available.

## Design Goals, Philosophies and Inspirations

Egg is designed to be a productive shell-first language, which means it makes different tradeoffs
than most general purpose programming languages. One of the main reasons for this is that general
purpose code is usually read more times than it's written, while shell commands are normally written
more times than they are read. This means general purpose languages like Python or Golang must
prioritize maintainability, safety, and clarity while a shell language should focus on providing
terse and obvious syntax and avoid getting in the way. Another important observation is that while
most code is written in an editor like vim or VS Code, shell code is normally composed inside the
input field of terminal where one-liners are more ergonomic than multiline code blocks.

Egg, like bash, can also be used in scripts (`.egg` files) and tries to be as suitable for this as
possible without compromising in it's primary arena.

It's impossible to design a shell language without having the existing syntax of bash in mind, and
first asking the extent to which the new shell language will strive to be similar or different to
bash, which most users are already familiar with. Egg does not try to be a Bash clone, but borrows
the things that Bash does well while paving it's own way (or stealing from non-bash languages) where
Bash leaves things to be desired.

Bash's syntax for navigating the filesystem, running executables, piping the output of one command
into the input of another and writing to files is clean, clear (to the initiated), and concise.
Frankly, it leaves little to be improved on, and the syntax for these things is so ingrained into
the community's muscle memory that any changes here would be hard to swallow, and so for the most
basic tasks, egg will look a lot like bash with only very minor changes. But beyond, that, Bash
becomes more clumsy and verbose. Simple and frequently used constructions like for loops in bash are
awkward and do not lend themselves to clear one liners, and the syntax for conditionals is similarly
verbose and peculiarly non-obvious.

## The Basics

### Executing Executables

You can run an executable located in the `PATH`, in the current working directory (cwd), or from a
relative path rooted in the cwd by entering it's name followed by it's arguments. This is similar to
the syntax used in bash, except that where Bash requires executables in the cwd to be preceded by
`./`, egg does not.

Egg Examples:
```
>  ls -l
>  clang my_c_program.c -o my_c_program.out
>  bin/my_c_program.out
>  my_egg_script.egg
```

Equivalent Bash:
```
>  ls -l
>  clang my_c_program.c -o bin/my_c_program.out
>  bin/my_c_program.out
>  ./my_egg_script.egg
```

Arguments do not normally need to be surrounded with quotations, but can be to avoid incorrect
parsing in cases such as: `ls "this/path/has spaces in it"`.

### Navigating the Filesystem

Navigating the filesystem in egg is the same as in Bash. 

You can adjust the CWD using the `cd` command which accepts either a relative or absolute path. The 
`~` symbol is replaced with the user's home directory when used inside of a path:
```
cd path/relative/to/cwd
cd /absolute/path
cd ~/path/relative/to/home
```

And you can write the CWD to standard out with the `pwd` (Print Working Directory) command.

As a note, the `ls` command is actually an executable found in the user's path, not a Bash builtin
as sometimes assumed, which means support for `ls` was never in question! The same is true for other
important commands like `cat`, `chmod`, `grep`, `mkdir`, `rm`, `touch`, etc. In fact, Bash has only
a few real builtins, and so most of the basic commands you rely on in terminal are available in egg.

### Writing to Standard Out

Egg, like most languages, has a print function! The print function in egg is `say`, and works like
`echo` in Bash.

```
>  say "hello world"
"Hello world"
>  say goodbye world
goodbye world
```

The `say` keyword was selected because it's short and clear.

### Redirecting Standard Out

The basic syntax for piping standard output (stdout) from one command to the standard input (stdin)
of another, and for writing the stdout of a command to a file is the same as in Bash:

```
>  cat logs.txt | grep "error:" > error_logs.txt
```

The `|` operator pipes the output of `cat logs.txt` to the input of `grep "error:"`. The `>`
operator writes the output of `cat logs.txt | grep "error:"` to the file `error_logs.txt`.

The `>` operator overwrites all original contents of the output file while a similar operator, `>>`
appends to the end of the file.

### Redirecting Standard Error and Other File Descriptors

Sometimes rather than piping or writing stdout, we would rather pipe or write the standard error
(stderr) of one command to another command or file.

In Bash, this is achieved for the `>` and `>>` operators by adding the id for the intended file
descriptor to the beginning of the operator (ex. `foo 2> file`). Bash does not support specifying
file descriptors for the pipe  operator `|` however, so we have to either swap stdout and stderr, 
as in `foo 3>&1 1>&2- 2>&3- | grep "fatal"` or else bypass the pipe operator altogether by
using process substitution as in `foo 2> >(grep "fatal")`. In general, we can say that Bash has
terse but non-obvious syntax for working with stderr and other file descriptors.

In egg, we can instead select the wanted file descriptors by surrounding an expression in
parenthesis, and using the `.out`, `.err`, `.both`, properties, or calling the
`.fds(<fd_ids>)` method.

Egg Examples:
```
(foo -args).out > infos.txt # Functionally equivalent to foo -args > infos.txt 
(foo -args).err > errors.txt
(foo -args).both > infos_and_errors.txt

# or...

(foo -args).fds(1) > infos.txt
(foo -args).fds(2) > errors.txt
(foo -args).fds(1,2) > infos_and_errors.txt
```

Equivalent Bash:
```
foo -args 1> infos.txt # Functionally equivalent to foo -args > infos.txt 
foo -args 2> errors.txt
foo -args > infos_and_errors.txt 2>&1 # Most portable syntax, see alternative below
foo -args &> infos_and_errors.txt # Better, but not available in all versions of Bash
```

This works just as well with pipes, as in the following Egg example:
```
(foo).err | grep "fatal"
```

Although We will cover data types, properties and methods more in later sections, to explain the Egg
examples above we note that most commands in egg have a return type of `Data`. The `Data` type has
several methods, including the ones used above. The properties `data.out`, `data.err` and
`data.all_fds` are of type `Stream` and the method `fds(...)` returns a `Stream`.

Additionally, a convenient member of `Stream` which may be helpful is the `read()` method 

### Error Handling

Sometimes commands fail. We may want to do different things depending on whether or not a command
was successful. The most basic and terse syntax for this in Egg uses the `&&` and `||` operators
which work the same in egg as they do in Bash.

`cmd1 && cmd2` operator executes `cmd2` iff `cmd1` succeeds with an exit code of zero.

`cmd1 || cmd2` operator executes `cmd2` iff `cmd1` fails with a nonzero exit code.

Though perhaps less conducive to use for simple terminal commands, `try/catch` blocks are also
supported, and provide an alternate syntax which may be helpful for structuring error handling in
scripts:
```
try {
    do_a
    do_b
    do_c
} catch {
    do_x
    do_y
    do_z
}
```
This is equivalent to:
```
(do_a && do_b && do_c) || (do_x; do_y; do_z)
```

Catch blocks can also accept an argument of type `Data` which corresponds to the value returned by
the failing command.

```
try {
    may_fail -args
} catch failure_data {
    say (
        `Command {failure_data.command} failed with message:\n`
        `\t{failure_data.err.read()}`
    )
}
```

In Egg, we can also directly check a command's exit code by getting the `exit_code` property of the
resulting `Data` object.

`>  say (my_executable -args).exit_code`

## Control Flow

#### Repeat



# For Each Loops
# for i in {1..5} do echo "Welcome $i times" done;
[1..5].map(say)
[1..5].ea( i => say "Welcome {i}")
for i in [1..5] {say "Welcome {i}"}

# While Loops
while i < 10 {
    say `Welcome {i}`;
}

# export a = hello
a := "hello"

# Asychronous
# long_runner &
~(long_runner)

~(long_runner).then(|result| { 
    say result;
    result ++ result
}).then(|result2| {
    say result
}).success(|result| { 
    say result
}).error(|result| { 
    say result
})

promise.await()

# [[ $b = 5 ]] && a="$c" || a="$d"
a := c ? b == 5 : d

# source foo.sh
import foo.ips

# Functions
fn do_thing(x) {say x}
do_thing := |x| {say x}

# Types
# data, file, function, list, json, list, number, string, bool, custom_classes

# Type Morphisms
some_data.split(" ") # delimiter is optional, default is " "
some_data.split_set(" ") # delimiter is optional, default is " "
some_list.to_set()
some_set.to_list()
~
# Lists
my_list := [1, 2, 3]
my_list.push(4)
my_list.push_front(0)
my_list.pop()
my_list.pop_front()
my_list.peek()
my_list.peek_front()

# Typed arguments
|x: Data, y: File, z: Fn| {z(y x)}

# Return Types
# any type or None
|x: Data, y: File, z: Fn| : Data {
    z(y x)
}

# Type Classes
type MyType() 

# Default parameters
fn do_thing(x, thing: function = say) {thing(x)}

# Methods
# All typed unary functions may be used as methods
some_data.re::fs()

# Math
# + - * / ** %
@a + @b

# Bitwise Math
xor(@a, @b)
a.xor(b)

# Logical
op.and(@a, @b)

# String Operations
c := a ++ b # Concatenation
c := `{a}{b}` # Concatenation
string_data.is_numeric()
string_data.is_alpha()

# Namespaces
module my_module { a := 1 }
my_module::a := 1

# Special namespaces
::xor(a, b) # Looks inside builtins and anything not given an explicit namespace
std::xor # Looks inside builtins
path::some_binary # Look inside the path for executables
cwd::some_binary # Look inside the current working directory

# Navigating the filetree
cd .././s

# Split string
mv base/[child1, child2]

# Variable Existence
if isset(FEATURE) ...

# Variable is not null
if FEATURE = NULL;

# Variable Exists and is Not Null
if FEATURE? ...

# Todo...
* More higher order functions (map, fold, reduce, filter, compose)
* Generators
* JSON and hashmaps
* Manipulating PATH
* history
* functions that take an unknown amount of arguments
* generators
* Function return types
* switch case
* ternat
* timing a call
* decorators
