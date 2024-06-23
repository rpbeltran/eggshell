from . import types
from .memory import *

# Garbage Collection todolist:
# todo: Automatically call the garbage collector once a certain amount of
#  memory has been allocated instead of waiting for the scope to be popped
# todo: Support creating instances which are not garbage collected
#  (we can free them by inserting frees w/ escape analysis)


def test_garbage_collection_basic():
    memory = Memory()
    assert len(memory.instances) == 0
    assert len(memory.scopes) == 1

    # var a
    memory.new(types.Integer(100), name="a")
    assert memory.get_id("a") == 0
    a = memory.get_id("a")
    assert (
            memory.get_object(a).val()
            == memory.get_object_by_name("a").val()
            == 100
    )

    # push scope
    memory.push_scope()
    assert len(memory.scopes) == 2

    # var b
    memory.new(types.Integer(101), name="b")
    assert memory.get_id("b") == 1
    b = memory.get_id("b")
    assert memory.get_object(b).val() == 101
    assert len(memory.instances) == 2

    # pop scope
    memory.pop_scope()
    assert len(memory.scopes) == 1
    assert len(memory.instances) == 1

    # pop scope
    memory.pop_scope()
    assert len(memory.scopes) == 0
    assert len(memory.instances) == 0


def test_garbage_collection_nonblocking_depends():
    memory = Memory()
    assert len(memory.instances) == 0
    assert len(memory.scopes) == 1

    # var a
    memory.new(types.Integer(100), name="a")
    assert memory.get_id("a") == 0
    a = memory.get_id("a")
    assert memory.get_object(a).val() == 100

    # push scope
    memory.push_scope()
    assert len(memory.scopes) == 2

    # var b = [&a]
    memory.new(types.Integer(101), deps={a}, name="b")
    assert memory.get_id("b") == 1
    b = memory.get_id("b")
    assert memory.get_object(b).val() == 101
    assert len(memory.instances) == 2

    # var c = [&b]
    memory.new(types.Integer(102), deps={b}, name="c")
    assert memory.get_id("c") == 2
    c = memory.get_id("c")
    assert memory.get_object(c).val() == 102
    assert len(memory.instances) == 3

    # pop scope
    memory.pop_scope()
    assert len(memory.scopes) == 1
    assert len(memory.instances) == 1

    # pop scope
    memory.pop_scope()
    assert len(memory.scopes) == 0
    assert len(memory.instances) == 0


def test_garbage_collection_depends():
    memory = Memory()
    assert len(memory.instances) == 0
    assert len(memory.scopes) == 1

    # var a
    memory.new(types.Integer(100), name="a")
    assert memory.get_id("a") == 0
    a = memory.get_id("a")
    assert memory.get_object(a).val() == 100

    # push scope
    memory.push_scope()
    assert len(memory.scopes) == 2

    # var b
    memory.new(types.Integer(101), name="b")
    assert memory.get_id("b") == 1
    b = memory.get_id("b")
    assert memory.get_object(b).val() == 101
    assert len(memory.instances) == 2

    # a.push(b)
    memory.add_dependency(a, b)

    # pop scope
    memory.pop_scope()
    assert len(memory.scopes) == 1
    assert len(memory.instances) == 2

    # pop scope
    memory.pop_scope()
    assert len(memory.scopes) == 0
    assert len(memory.instances) == 0


def test_garbage_collection_circular():
    memory = Memory()
    assert len(memory.instances) == 0
    assert len(memory.scopes) == 1

    # var a
    memory.new(types.Integer(100), name="a")
    assert memory.get_id("a") == 0
    a = memory.get_id("a")
    assert memory.get_object(a).val() == 100

    # push scope
    memory.push_scope()
    assert len(memory.scopes) == 2

    # var b
    memory.new(types.Integer(101), deps={a}, name="b")
    assert memory.get_id("b") == 1
    b = memory.get_id("b")
    assert memory.get_object(b).val() == 101
    assert len(memory.instances) == 2

    # a.push(b)
    memory.add_dependency(a, b)

    # pop scope
    memory.pop_scope()
    assert len(memory.scopes) == 1
    assert len(memory.instances) == 2

    # pop scope
    memory.pop_scope()
    assert len(memory.scopes) == 0
    assert len(memory.instances) == 0