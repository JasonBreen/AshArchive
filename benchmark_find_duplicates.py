import time
import random
import string
from collections import defaultdict

def generate_mods(num_mods, duplicate_ratio):
    mods = []
    # Base words
    words = [''.join(random.choices(string.ascii_lowercase, k=8)) for _ in range(num_mods // 2)]

    for i in range(num_mods):
        if random.random() < duplicate_ratio:
            base = random.choice(words)
            mod_id = f"mod_{base}"
            mod_name = f"Mod {base.capitalize()}"
        else:
            base = ''.join(random.choices(string.ascii_lowercase, k=8))
            mod_id = f"mod_{base}_{i}"
            mod_name = f"Mod {base.capitalize()} {i}"

        mods.append({"id": mod_id, "name": mod_name})

    # Add same name different id
    for i in range(int(num_mods * duplicate_ratio)):
        base = random.choice(words)
        mod_name = f"Mod {base.capitalize()}"
        mod_id = f"mod_{base}_{random.randint(1000, 9999)}"
        mods.append({"id": mod_id, "name": mod_name})

    return mods

def original_find_duplicates(mods):
    id_counts = defaultdict(int)
    name_to_ids = defaultdict(set)
    for mod in mods:
        mod_id = mod.get("id")
        mod_name = mod.get("name")
        if isinstance(mod_id, str) and mod_id:
            id_counts[mod_id] += 1
        if isinstance(mod_name, str) and mod_name and isinstance(mod_id, str) and mod_id:
            name_to_ids[mod_name].add(mod_id)

    dup_ids = sorted(mod_id for mod_id, count in id_counts.items() if count > 1)
    dup_names = sorted(name for name, ids in name_to_ids.items() if len(ids) > 1)
    return dup_ids, dup_names

def new_find_duplicates(mods):
    seen_ids = set()
    dup_ids_set = set()
    name_to_ids = defaultdict(set)
    dup_names_set = set()

    for mod in mods:
        mod_id = mod.get("id")
        mod_name = mod.get("name")

        has_id = isinstance(mod_id, str) and mod_id
        if has_id:
            if mod_id in seen_ids:
                dup_ids_set.add(mod_id)
            else:
                seen_ids.add(mod_id)

        if isinstance(mod_name, str) and mod_name and has_id:
            ids = name_to_ids[mod_name]
            ids.add(mod_id)
            if len(ids) > 1:
                dup_names_set.add(mod_name)

    dup_ids = sorted(dup_ids_set)
    dup_names = sorted(dup_names_set)
    return dup_ids, dup_names

mods = generate_mods(100000, 0.1)

# verify correctness
assert original_find_duplicates(mods) == new_find_duplicates(mods)

# Benchmark
import timeit

print("Original:", timeit.timeit(lambda: original_find_duplicates(mods), number=10))
print("New:", timeit.timeit(lambda: new_find_duplicates(mods), number=10))
