"""Shared pytest settings: sets the order in which test groups run."""

# Groups run in this order. A test with two markers (for example smoke + ecp)
# is placed by the first group in this list that it belongs to.
GROUP_ORDER = ["smoke", "ecp", "boundary", "negative", "datadriven", "module"]


def _group_rank(item):
    for rank, name in enumerate(GROUP_ORDER):
        if item.get_closest_marker(name):
            return rank
    return len(GROUP_ORDER)  # tests without a group marker run last


def pytest_collection_modifyitems(items):
    # sort() is stable, so tests keep their file order inside one group
    items.sort(key=_group_rank)