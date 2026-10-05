def get_target_pair(stripe_index, mirror_pairs):
    pair_index = stripe_index % len(mirror_pairs)
    return mirror_pairs[pair_index]