# Welcome to Egg.

Egg is a shell programming that tries to have some cake and eat some too.

It tries to be terse and productive for use in a shell:
```
# Sum the second column of a csv
$ total := cat my_file.csv | _.split.ea $ _.split(',')[1].int | _.map.sum
```

While being sane and extendable for use in scripts:

```
class Item {
    name: Str
    price: Float
    quantity: Int

    fn total (): Float {
        ret price * quantity
    }
}

fn get_items_from(file: Path) : Status[[Item]] {
    if !(file.exists) {
        ret Status::Error("Provided file does not exist")
    }

    lines : [str] = `read @file` | _.split

    items : [Item] = []
    for (i, line) in lines.with_indices {
        cols := line.split(',')
        if cols.len != 3 {
            ret Status::Err("Line {i} is invalid")
        }
        items.add(Item{cols[0], cols[1].float, cols[2].int})
    }
    ret Status::Ok(items)
}

fn main (args) {
    for item in get_items_from(args[0]).expect() {
        say "Item: {item.name} Cost: {item.cost}"
    }
}
```

Note: Egg is in the early design stage and syntax is highly prone to change.

## Goals

Egg has goals:
* be a highly productive shell language
* make scripting a maintainable endeavor
* be simple and predictable to non-experts
* be easy to learn

With these goals comes more concrete corollaries:
* egg should be extensible with custom types, modules, and encapsulation
* egg should attempt to minimize footguns
* egg should be gradually typed (since type checker in scripts == good, 
but type annotation in shell == tedious)
* egg should support standard data structures
* egg should avoid undefined behaviour (so I guess we'll need some docs)

Notably, some other things are non-goals too:
* Compatibility with Bash syntax is a non-goal, though generally, where Egg 
differs from Bash there is a preference that the Bash syntax should error in Egg
as opposed to doing something subtly different.
* Blazing fast performance as a general-purpose programming language is a non-goal, as shell
  scripts normally spend most of their computation time inside other executables

And to top it off, there are some future goals that are currently nowhere near
the top of the list of priorities. We'll call these "nice to haves" for now:
* Support for unit testing functions with guarantees of no system side-effects.
* A fully featured argparse toolkit for standardizing cli design of egg scripts
* A standard library of useful modules

## Status

Early design and prototyping stage

## An Inclomplete Assortment of Planned Language Features

**Executing Commands**

These parts look a lot like Bash

```
cd ~/very/nice/path
foo bar | grep "spam" >> output_file.txt     
```

If we type in an arbitrary word (which is not a reserved keyword), eggshell will
attempt to find an executable the path that matches and will execute it. We will
refer to this as "implicit execution".

We can
also disambiguate our intention to execute some string by surrounding it in
backticks as in `foo bar`. If by chance your executable includes certain
charecters such as spaces, you will need to surround it in quotes
(even if you are using backticks) such as in the following cases.

```
"hello world.py" a b c
`"hello world.py" a b c`
```

Unlike in Bash however, implicit execution is not permitted:
1. within code blocks surrounded by `{ ... }`
2. between square brackets `[ ... ]`
3. within parenthetical expressions `( ... )`
4. following a numerical-arithmetic operator `+`, `-`, `*`, `/`, `//`, `**`, or `%`

So within a function for example, we must use backticks.
In these cases, `a := b` will  assume b is the name of another variable, not a
target to execute.

```
fn a() {
  hello := `echo hello`
  say $ hello
}
```

When implicit execution is allowed at the top level, variable names must be
prefixed with a `@` symbol, as in: `a := @b`.


**User defined functions and lambdas**

```
fn get_rows_for_user(username: str): [str] {
    ret `cat data.csv` | `grep "{username}@company.com"`.split()
}

rows := get_rows_for_user("user")
```

Lambdas are supported too with the syntax: `\a -> b` for a single arg or
`\(a,b) -> c` for lambdas with multiple arguments.

This function has a lambda in its body:
```
fn factorial(n: int): int {
    answer := 1
    (1..n).ea $ \i -> answer *= i
    ret answer
}

factorial_of_10 := factorial(10)
```

Functions that take a single argument can also have that argument piped to it
like so:

```
factorial_of_10 := 10 | @factorial
```

Functions can also take two special types of arguments: `*args` which accepts
multiple arguments and provides them as a list, and `**kwargs` which accepts
arbitrary named arguments and returns them as a Map with string keywords. These
arguments should be familiar to Python users.

```
fn sum(*args) {
  total := 0;
  args.ea(total += _)
}
```

```
fn run_with_env(executable: str, **extra_env: map[str,str] ) {
  env.push
  for item in extra_env {
    env.set(item[0], item[1])
  }
  `{executable}`
  env.pop
}
```

Functions can also receive arguments via "currying" syntax:

```
add3 : Fn = \(a, b, c) -> @a + b + c

plus_15 := add3 $ 10 $ 5

sum_1_2_3 : int = f $ 1 $ 2 $ 3
```

Implicit lambdas can also be created with the `_` token for lambdas that only
take one argument.

```
lines := cat my_file.csv | _.split()
```

The scope of an implicit lambda is bounded by pipe `|` and curry `$` operators.
This means that `a | foo(_.bar)` is equivalent to `a | \x -> foo(x.bar)`. If you
need a lambda to be defined more narrowly you will need to define the lambda
explicitly or restructure your expression. For example, if in the previous
example you wanted the `_.a` to be a lambda argument to foo, you could rewrite
the expression as `a | foo $ _.bar`.

There is also a shorthand for just these sorts of lambdas which are used to
access fields of an object as `...field_name`. Take for example the expression:
`items.sort(key=\x -> x.date)`. We could also write this
`items.sort(key=...date)`.

Lambda functions can also have multiple lines using curly braces as below:

```
add3 := \(a,b,c) {
    d:= a + b
    return d + c 
}
```

Default arguments can be asserted, and type hints on arguments are optional.
When we are calling a function with zero args, or using only default values for
args, we can omit the parenthesis. See how implicit lambdas and function calls
make get_rows_for_user faster to type.

```
lines := cat my_file.csv | _.split.rev.rev # why reverse twice? Because we can!
```

To refer to the function directly when the function is not being called or
curried (functions in egg are first class!) we can add `...` to subvert this
behavior.

```
fn do_with_1_2_3 ( f: Fn ) {
    f(1)
    f(2)
    f(3)
}

do_with_1_2_3(say...)
```


**Error Handling**

This works the same as in Bash:
```
(do_a && do_b && do_c) || do_x
```

But we also support another:
```
try {
    do_a
    do_b
    do_c
} catch {
    do_x
}
```

These are exactly equivalent, but try-catch blocks have an additional ability to
catch the exact error thrown inside the try and store it:


```
try {
    do_a
    do_b
    do_c
} catch e: Error {
    say("Handling error: {e}")
    do_x
    do_y
    do_z
}
```

**Do Blocks**

Consider the bash code `(a && b && c) || (x; y; z)` and
notice how semicolons within a parenthesis allow bash to express a sequence of
actions in a sort of code block without creating a function. In Egg, we can
construct a similar "atomic sequence" using "do blocks".

The equivalent code in Egg would be:
```
(`a` && `b` && `c`) || do {`x`; `y`; `z`}
```

**Loops**

Egg supports three basic types of loops, all of which will likely feel familiar:

Infinite loops:
```
loop {
  if input("Enter guess: ") == correct_answer {
    break
  }
  say $ "Guess again"   
}
```

While loops:
```
a := 1
while (a < 10) {
    say $ a
    a += 1
}
```

For loops:
```
for i in (0..10) {
    say i
}
```

Additionally, most collections types have a `.ea` "for each" method:
```
# Print 0 through 9
(0..10).ea $ say _ 
```

Loops can also have labels for breaking or continuing outer loops using the `as`
keyword:
```
loop as outer_loop {
  ...
  while(...) as inner_loop {
    ...
    if (...) {
      continue outer_loop
    }
  }
}
```

Labeled loops are supported for `loop`, `for` and `while` loops.

**Asynchronous Programming**

Promises in bash are similar to their counterparts in Javascript.

```
promise := ~(`long_running_executable a b c`)
say "I get printed almost immediately!"
promise.await()
say "I get printed after the long task finishes..."
```

We can chain them together like so:

```
~(`foo`).then( \foo_out -> { 
    say(foo_out)
    `do_something_else`
}).success(say _).error(say _).then(say _)
```


**Importing other egg files**

Consider `my_egg.egg` with the following contents:

```
import "my_library.egg"

fn foo() {
  say "hello world"
}

foo()
```

There are two different ways we might want to incorporate this script into
another.

The first thing we may want to do is simply call the script from another script.
This is done with:
```
egg my_egg.egg
```
That will call the script in a new process but will not make `foo()` available
to use by the calling script.

The second thing we may want to do is fetch the user defined functions and types
for use in our own script. This is done with:

```
import "my_egg.egg"
```

That will make foo available to the calling script under the namespace "my_egg",
so we can say:

```
import "my_egg.egg"

my_egg::foo()
```

Note that in the above snippet, "hello world" will be displayed twice as
my_egg.egg must be run in order to import it. The namespace of a module is
decided by its parsing its filename. But we can change it like so:

```
import "my_egg.egg" as foo_lib

foo_lib::foo()
```

**Classes**

todo: write more here

```
class Item {
  name: Str
  price: Float
  quantity: Int = 1

  fn total(): Float {
    ret price * quantity
  }
}

item : Item = Item{"thingy", 1.99} 
```

Egg supports polymorphism. 

```
class Cow : Animal {
    fn make_sound() {
      say("moo")
    }
} 
```

**Lists**

Lists in egg behave similarly to lists in other languages like Python. Like many
dynamic programming languages, the elements in lists need not be the same type,
unless of course type constraints have been added. Lists are 0-indexed as all
things should be.

```
l := [1,2,"three",Four(),5.0]

four := l[3]
_3_4_5_ := l[2:5]
_1_3_5_ := l[0:5:2] 

l_last := l[-1]

l_reversed := l[::-1]

l.add(6)

l.insert(1,1.5)

[9,0,5,1].sort()

nearest_to_7 := [9,0,5,1].sort_rev(abs(_ - 7 ))

size := l.len()
```

Lists is egg can also be used as sets.

```
l := [1,4,6,7,8, 4]
s := l.uniq()
s.add_uniq(3)
s.add_uniq(4) # does nothing!
```


**Maps**

Maps in egg behave similarly to dictionaries in Python.  

```
a : Map = { "apple": Apple, "orange": Orange }

a := { }
```

They are in essence heterogeneous hashmaps (the keys need not all be the same
type, nor the values). Though type constraints may be added as desired!

```
valid_map : Map[str, int] = { "apple": 1, "orange": 2 }
try {
  invalid_map : Map[str, int] = { "apple": 1, "orange": false }
} catch {
  say "non-int value 'false' throws an error";
}
```

**Working with Environment Variables**

Unlike with bash, environment variables do not enter the global scope. This is 
to help avoid collisions with user defined variables and functions as well as
executables in path.

To access an environment variable with a default value, use `env.get` as in:
`env.get("FOO", "default_value")`

To set an environment variable for the duration of the script, use:
`@env.set("FOO", "hello")` or `@env["FOO"] = "Hello"`

To check if an environment variable is set, use:
`@env.has("FOO")`

If you know that an environment variable is set, you can access it like a
dictionary which will throw an error if it is not defined:
`@env["FOO"]`

To temporarily set an environment variable, then return it to prior state,
you can employ the `push` and `pop` methods:

```
env.push("FOO", "hello")
./do_something_that_uses_foo
env.pop("FOO")
```

You can also call `env.push` and `env.pop` without any arguments and it will
reset all environment variables to their previous state.

```
env["foo"] = "Hello"
env["bar"] = "World"

env.push()
env["foo"] = "Alice"
env["bar"] = "Bob"
say "hello {env['foo']} and {env['bar']}" 
env.pop()

say "{env['foo']} {env['bar']}"
```

Calling `env.pop()` if no states have been pushed with `env.push()` (or if all
pushed states have been popped before), env will be reset to it's value when the
script or shell was created. This can also be forced with `env.reset()`.

Will display "hello Alice and Bob" on the first `say` and "hello world" on the
second.

One more way of setting the environment temporarily is with a context. Contexts
work similar to their equivalents in Python.

```
with env.ctx(foo="hello", bar="world") {
  say $ "{env['foo']} {env['bar']}"
}
```

This will set `foo` and `bar` environment variables for the duration of the with
block only. 


## Builtin Types and Data Structures

**Basic Types**

1. Str
2. Int
3. Float
4. Bool
5. Fn

**Provided Data Structures**

1. Lists
2. Hashmaps


## Random Details

These things should probably go somewhere other than the README at some point.

### Operator Precedence Chart

From highest to lowest priority (higher priorities evaluate first):

1. selection: `my_list[i]`, `...field_name`, `func_name...`
2. negation: `not`, `!`, `-` (unary)
3. exponentiation: `**`
4. multiplication/division: `*`, `/`, `//`, `%`
5. comparison: `!=`, `==`, `>`, `>=`, `<`, `<=`
6. conjunction: `and` 
7. disjunction: `or`, `xor`
8. implicit lambda: `_`
9. currying: `$`
10. pipelining: `|`
11. assignment: `:=`
12. semicolon: `;`

### Chaining Comparisons

Comparison operators can be chained like such:

```
a < b > 3 == 4 != 5
```

The result will be true iff all adjacent values uphold their connecting
comparison.
