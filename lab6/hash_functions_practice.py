"""Part 1: implement the Division Method and Multiplication Method hash functions.

Golden Ratio conjugate constant A is provided.
"""

import math

GOLDEN_RATIO_A = (math.sqrt(5) - 1.0) / 2.0


def division_hash(key, m):
  return key % m


def multiplication_hash(key, m, A=GOLDEN_RATIO_A):
  return math.floor(m * ((key * A) % 1.0))


if __name__ == "__main__":
  from lab_checks import check_hash_functions
  raise SystemExit(
    check_hash_functions(
      division_hash,
      multiplication_hash,
    )
  )
