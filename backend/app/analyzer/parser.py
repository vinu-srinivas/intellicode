import ast


def parse_code(code: str):
    """
    Parse Python source code into an Abstract Syntax Tree.

    Returns:
        AST object if parsing succeeds.
        Error information if parsing fails.
    """

    try:
        tree = ast.parse(code)

        return {
            "syntax_valid": True,
            "tree": tree,
            "error": None
        }

    except SyntaxError as error:
        return {
            "syntax_valid": False,
            "tree": None,
            "error": {
                "message": error.msg,
                "line": error.lineno,
                "column": error.offset
            }
        }