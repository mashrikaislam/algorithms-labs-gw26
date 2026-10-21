"""Part 3: implement Open Addressing with Linear Probing insert and lookup.

OpenAddressingHashTable container and probe_index helper are provided.
"""


class OpenAddressingHashTable:
  """Open Addressing hash table storing [key, value] pairs directly in slots."""

  def __init__(self, capacity=7):
    self.capacity = capacity
    self.size = 0
    self.slots = [None] * capacity

  def __repr__(self):
    return (
      "OpenAddressingHashTable(capacity=" + str(self.capacity)
      + ", size=" + str(self.size) + ")"
    )


def probe_index(key, i, m):
  """Provided: return the slot index for probe step i using Linear Probing.

  Formula: ((key mod m) + i) mod m
  """
  return ((key % m) + i) % m


def linear_probe_insert(table, key, value):
    for i in range(table.capacity):
        slot = probe_index(key, i, table.capacity)
        probes = i + 1

        if table.slots[slot] is None:
            table.slots[slot] = [key, value]
            table.size += 1
            return (slot, probes)

        if table.slots[slot][0] == key:
            table.slots[slot][1] = value
            return (slot, probes)

    raise OverflowError("Hash table is full")


def linear_probe_lookup(table, key):
    for i in range(table.capacity):
        slot = probe_index(key, i, table.capacity)
        probes = i + 1

        if table.slots[slot] is None:
            return (None, probes)

        if table.slots[slot][0] == key:
            return (table.slots[slot][1], probes)

    return (None, table.capacity)


if __name__ == "__main__":
  from lab_checks import check_probing
  raise SystemExit(
    check_probing(
      probe_index,
      linear_probe_insert,
      linear_probe_lookup,
    )
  )
