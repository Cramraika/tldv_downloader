# vulture whitelist — symbols vulture flags as unused but are actually used
# (framework callbacks, dynamically-referenced attrs, API surface, etc.).
# Auto-scanned by `vulture .` from repo root (OW-503). Seed empty; append as needed.
#
# Usage: each line names a symbol to treat as USED, e.g.:
#   _.my_unused_looking_attr   # accessed via getattr / serialization
#   handle_event               # registered as a framework callback
#
# Generate candidates with:  vulture . --make-whitelist > .vulture-whitelist.candidates.py
# then review + move real false-positives here (NEVER blanket-import the candidates file).
