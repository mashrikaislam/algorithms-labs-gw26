"""Part 2: implement Separate Chaining insert and lookup.

ChainingHashTable container, load_factor, chaining_rehash, and chaining_delete are provided.
"""


class ChainingHashTable:
  """Separate Chaining hash table storing [key, value] pairs in bucket lists."""

  def __init__(self, capacity=7, max_load=0.75):
    self.capacity = capacity
    self.max_load = max_load
    self.size = 0
    self.buckets = [[] for _ in range(capacity)]

  def __repr__(self):
    return (
      "ChainingHashTable(capacity=" + str(self.capacity)
      + ", size=" + str(self.size) + ")"
    )


def load_factor(table):
  """Provided: return current table load factor alpha = N / M."""
  return table.size / table.capacity


def chaining_rehash(table, new_capacity):
  """Provided: resize table to new_capacity and rehash all [key, value] pairs."""
  old_buckets = table.buckets
  table.capacity = new_capacity
  table.buckets = [[] for _ in range(new_capacity)]

  for bucket in old_buckets:
    for key, value in bucket:
      new_index = key % table.capacity
      table.buckets[new_index].append([key, value])


def chaining_delete(table, key):
  """Provided: remove key from table and return its value, or None if missing."""
  index = key % table.capacity
  bucket = table.buckets[index]

  for i, (entry_key, entry_val) in enumerate(bucket):
    if entry_key == key:
      bucket.pop(i)
      table.size -= 1
      return entry_val
  return None


def chaining_insert(table, key, value):
    index = key % table.capacity
    bucket = table.buckets[index]

    for entry in bucket:
        if entry[0] == key:
            entry[1] = value
            return

    bucket.append([key, value])
    table.size += 1

    if load_factor(table) > table.max_load:
        chaining_rehash(table, 2 * table.capacity)


def chaining_lookup(table, key):
    index = key % table.capacity
    bucket = table.buckets[index]

    for entry in bucket:
        if entry[0] == key:
            return entry[1]

    return None


if __name__ == "__main__":
  from lab_checks import check_chaining
  raise SystemExit(
    check_chaining(
      chaining_insert,
      chaining_lookup,
      chaining_delete,
      chaining_rehash,
    )
  )
