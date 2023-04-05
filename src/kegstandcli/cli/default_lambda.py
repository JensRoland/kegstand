import kegstand

# Create and export the Kegstand API as a single
# Lambda-compatible handler function
handler = kegstand.Api(__file__).export()
