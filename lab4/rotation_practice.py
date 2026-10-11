"""Parts 3-4: implement AVL balance factor, rotations, and iterative and recursive AVL insertion.

Node structure, tree container, and height maintenance helpers are provided.
"""


class Node:
  """Binary Search Tree node with parent pointer and height attribute."""

  def __init__(self, key, parent=None):
    self.key = key
    self.parent = parent
    self.left = None
    self.right = None
    self.height = 0

  def __repr__(self):
    return "Node(" + str(self.key) + ")"


class BinarySearchTree:
  """Container holding the root pointer of a Binary Search Tree."""

  def __init__(self):
    self.root = None

  def print_tree(self):
    """Print the full tree with child labels, heights, balance factors, and parents."""
    if self.root is None:
      print("(empty tree)")
      return

    seen = set()

    def node_summary(node):
      left_height = -1 if node.left is None else node.left.height
      right_height = -1 if node.right is None else node.right.height
      bf = left_height - right_height
      parent_key = "None" if node.parent is None else str(node.parent.key)
      return (
        str(node.key)
        + " [height=" + str(node.height)
        + ", bf=" + str(bf)
        + ", parent=" + parent_key + "]"
      )

    def print_children(node, prefix):
      if node.left is None and node.right is None:
        return

      children = [("L", node.left), ("R", node.right)]
      for index, (direction, child) in enumerate(children):
        is_last = index == len(children) - 1
        connector = "└── " if is_last else "├── "
        child_prefix = prefix + ("    " if is_last else "│   ")

        if child is None:
          print(prefix + connector + direction + ": None")
        elif id(child) in seen:
          print(
            prefix + connector + direction + ": "
            + node_summary(child) + " [cycle or repeated reference]"
          )
        else:
          seen.add(id(child))
          print(prefix + connector + direction + ": " + node_summary(child))
          print_children(child, child_prefix)

    seen.add(id(self.root))
    print(node_summary(self.root))
    print_children(self.root, "")


def get_height(node):
  """Provided: return height of node (-1 for None, 0 for leaf)."""
  if node is None:
    return -1
  return node.height


def update_height(node):
  """Provided: recalculate node's height based on its left and right children."""
  if node is not None:
    node.height = 1 + max(get_height(node.left), get_height(node.right))


def balance_factor(node):
  if node is None:
    return 0
  return get_height(node.left) - get_height(node.right)

def rotate_left(tree, x):
  y = x.right
  x.right = y.left

  if y.left is not None:
    y.left.parent = x

  y.parent = x.parent

  if x.parent is None:
    tree.root = y
  elif x == x.parent.left:
    x.parent.left = y
  else:
    x.parent.right = y

  y.left = x
  x.parent = y

  update_height(x)
  update_height(y)

  return y

def rotate_right(tree, y):
  x = y.left
  y.left = x.right

  if x.right is not None:
    x.right.parent = y

  x.parent = y.parent

  if y.parent is None:
    tree.root = x
  elif y == y.parent.left:
    y.parent.left = x
  else:
    y.parent.right = x

  x.right = y
  y.parent = x

  update_height(y)
  update_height(x)

  return x


def rotate_left_right(tree, z):
  rotate_left(tree, z.left)
  return rotate_right(tree, z)


def rotate_right_left(tree, z):
  rotate_right(tree, z.right)
  return rotate_left(tree, z)


def avl_insert_iterative(tree, key):
  parent = None
  current = tree.root

  while current is not None:
    parent = current
    if key < current.key:
      current = current.left
    else:
      current = current.right

  new_node = Node(key, parent)

  if parent is None:
    tree.root = new_node
  elif key < parent.key:
    parent.left = new_node
  else:
    parent.right = new_node

  current = parent

  while current is not None:
    update_height(current)
    bf = balance_factor(current)

    if bf > 1:
      if balance_factor(current.left) < 0:
        rotate_left(tree, current.left)
      new_root = rotate_right(tree, current)
      current = new_root.parent

    elif bf < -1:
      if balance_factor(current.right) > 0:
        rotate_right(tree, current.right)
      new_root = rotate_left(tree, current)
      current = new_root.parent

    else:
      current = current.parent

  return new_node


def avl_insert_recursive(tree, key):
  def insert(node, key, parent):
    if node is None:
      return Node(key, parent)

    if key < node.key:
      node.left = insert(node.left, key, node)
    else:
      node.right = insert(node.right, key, node)

    update_height(node)
    bf = balance_factor(node)

    if bf > 1:
      if balance_factor(node.left) < 0:
        rotate_left(tree, node.left)
      return rotate_right(tree, node)

    if bf < -1:
      if balance_factor(node.right) > 0:
        rotate_right(tree, node.right)
      return rotate_left(tree, node)

    return node

  tree.root = insert(tree.root, key, None)
  tree.root.parent = None

  return bst_search(tree.root, key)


if __name__ == "__main__":
  from lab_checks import check_rotations
  raise SystemExit(
    check_rotations(
      balance_factor,
      rotate_left,
      rotate_right,
      rotate_left_right,
      rotate_right_left,
      avl_insert_iterative,
      avl_insert_recursive
    )
  )
