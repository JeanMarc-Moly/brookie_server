class NoLibrary(Exception):
    def __init__(self) -> str:
        super().__init__("No library plugin available")
