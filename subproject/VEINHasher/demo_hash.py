# demo_hash.py  – minimal example
# from vein import VEIN


demo_pass_phrase = "This is not the passphrase we will use in the production system"
MAIN_KEY = VEIN.passphrase_to_hex64(demo_pass_phrase)
MAIN_MODULUS = 9973                     # any integer ≥ 2
DUMMY_EIN    = "12-3456789"

hashed = VEIN.VTIN_identifier(
    ein=DUMMY_EIN,
    main_key=MAIN_KEY,
    modulus=MAIN_MODULUS,
)

print(f"dummy_ein: {DUMMY_EIN}  →  hash:{hashed}")