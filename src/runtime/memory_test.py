from .memory import Memory
from .types.numeric import Integer

# Garbage Collection todolist:
# todo: Automatically call the garbage collector once a certain amount of
#  memory has been allocated instead of waiting for the scope to be popped
# todo: Support creating instances which are not garbage collected
#  (we can free them by inserting frees w/ escape analysis)


def test_garbage_collection_basic() -> None:
    memory = Memory()
    assert len(memory.instances) == 0
    assert len(memory.scopes) == 1

    # var a
    memory.new(Integer(100), name="a")
    assert memory.get_id("a") == 0
    a = memory.get_id("a")
    assert a is not None
    a_obj = memory.get_object(a)
    assert isinstance(a_obj, Integer)
    assert a_obj.val() == 100
    a_obj_by_name = memory.get_object_by_name("a")
    assert isinstance(a_obj_by_name, Integer)
    assert a_obj_by_name.val() == 100

    # push scope
    memory.push_scope()
    assert len(memory.scopes) == 2

    # var b
    memory.new(Integer(101), name="b")
    assert memory.get_id("b") == 1
    b = memory.get_id("b")
    assert b is not None
    b_obj = memory.get_object(b)
    assert isinstance(b_obj, Integer)
    assert b_obj.val() == 101
    assert len(memory.instances) == 2

    # pop scope
    memory.pop_scope()
    assert len(memory.scopes) == 1
    assert len(memory.instances) == 1

    # pop scope
    memory.pop_scope()
    assert len(memory.scopes) == 0
    assert len(memory.instances) == 0


def test_garbage_collection_nonblocking_depends() -> None:
    memory = Memory()
    assert len(memory.instances) == 0
    assert len(memory.scopes) == 1

    # var a
    memory.new(Integer(100), name="a")
    assert memory.get_id("a") == 0
    a = memory.get_id("a")
    assert a is not None
    a_obj = memory.get_object(a)
    assert isinstance(a_obj, Integer)
    assert a_obj.val() == 100

    # push scope
    memory.push_scope()
    assert len(memory.scopes) == 2

    # var b = [&a]
    memory.new(Integer(101), deps={a}, name="b")
    assert memory.get_id("b") == 1
    b = memory.get_id("b")
    assert b is not None
    b_obj = memory.get_object(b)
    assert isinstance(b_obj, Integer)
    assert b_obj.val() == 101
    assert len(memory.instances) == 2

    # var c = [&b]
    memory.new(Integer(102), deps={b}, name="c")
    assert memory.get_id("c") == 2
    c = memory.get_id("c")
    assert c is not None
    c_obj = memory.get_object(c)
    assert isinstance(c_obj, Integer)
    assert c_obj.val() == 102
    assert len(memory.instances) == 3

    # pop scope
    memory.pop_scope()
    assert len(memory.scopes) == 1
    assert len(memory.instances) == 1

    # pop scope
    memory.pop_scope()
    assert len(memory.scopes) == 0
    assert len(memory.instances) == 0


def test_garbage_collection_depends() -> None:
    memory = Memory()
    assert len(memory.instances) == 0
    assert len(memory.scopes) == 1

    # var a
    memory.new(Integer(100), name="a")
    assert memory.get_id("a") == 0
    a = memory.get_id("a")
    assert a is not None
    a_obj = memory.get_object(a)
    assert isinstance(a_obj, Integer)
    assert a_obj.val() == 100

    # push scope
    memory.push_scope()
    assert len(memory.scopes) == 2

    # var b
    memory.new(Integer(101), name="b")
    assert memory.get_id("b") == 1
    b = memory.get_id("b")
    assert b is not None
    b_obj = memory.get_object(b)
    assert isinstance(b_obj, Integer)
    assert b_obj.val() == 101
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


def test_garbage_collection_circular() -> None:
    memory = Memory()
    assert len(memory.instances) == 0
    assert len(memory.scopes) == 1

    # var a
    memory.new(Integer(100), name="a")
    assert memory.get_id("a") == 0
    a = memory.get_id("a")
    assert a is not None
    a_obj = memory.get_object(a)
    assert isinstance(a_obj, Integer)
    assert a_obj.val() == 100

    # push scope
    memory.push_scope()
    assert len(memory.scopes) == 2

    # var b
    memory.new(Integer(101), deps={a}, name="b")
    assert memory.get_id("b") == 1
    b = memory.get_id("b")
    assert b is not None
    b_obj = memory.get_object(b)
    assert isinstance(b_obj, Integer)
    assert b_obj.val() == 101
    assert len(memory.instances) == 2

    assert memory.get_id("foo") is None

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