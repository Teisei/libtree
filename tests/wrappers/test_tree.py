# Copyright (c) 2015 Fabian Kochem


from libtree.wrappers import Transaction, Tree
from mock import Mock
import pytest


def test_it_takes_a_connection(dsn):
    conn = Mock()
    assert Tree(connection=conn).connection is conn


def test_it_takes_a_connection_pool(dsn):
    pool = Mock()
    assert Tree(pool=pool).pool is pool


def test_it_takes_a_table_prefix():
    prefix = '_vortec'
    assert Tree(pool=Mock(), prefix=prefix).prefix == prefix


def test_it_requires_either_connection_or_pool():
    with pytest.raises(TypeError):
        Tree()


def test_it_cant_deal_with_both_connection_and_pool():
    with pytest.raises(TypeError):
        Tree(connection=Mock(), pool=Mock())


def test_cm_returns_a_transaction_object():
    conn = Mock()
    tree = Tree(connection=conn)
    with tree() as transaction:
        assert transaction.__class__ == Transaction


def test_cm_uses_assigned_transaction_object():
    conn = Mock()
    tree = Tree(connection=conn)
    with tree() as transaction:
        assert transaction.connection is conn


def test_cm_uses_connection_from_pool():
    pool, conn = Mock(), Mock()
    pool.getconn.return_value = conn
    tree = Tree(pool=pool)
    with tree() as transaction:
        assert transaction.connection is conn


def test_cm_puts_connection_back_into_pool():
    pool, conn = Mock(), Mock()
    pool.getconn.return_value = conn
    tree = Tree(pool=pool)
    with tree() as transaction:  # noqa
        pass
    assert pool.putconn.called
    pool.putconn.assert_called_with(conn)


def test_cm_commits_transaction():
    conn = Mock()
    tree = Tree(connection=conn)
    with tree() as transaction:  # noqa
        pass
    assert conn.commit.called


def test_cm_rolls_back_transaction():
    conn = Mock()
    tree = Tree(connection=conn)
    with pytest.raises(ValueError):
        with tree() as transaction:  # noqa
            raise ValueError()
    assert conn.rollback.called


def test_close():
    pool = Mock()
    Tree(pool=pool).close()
    assert pool.closeall.called


def xtest_check_postgres_version():
    raise NotImplementedError


def xtest_install():
    raise NotImplementedError


def xtest_drop_tables():
    raise NotImplementedError


def xtest_flush_tables():
    raise NotImplementedError
