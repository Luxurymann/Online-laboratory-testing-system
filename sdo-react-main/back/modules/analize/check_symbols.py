import re
from typing import List, Dict, Union

from models.db_class import CodeLength


def check_symbols(filename: str, length: CodeLength, unique_id: str) -> Dict[str, Union[int, bool, None]]:
    with open(f'./trash/{unique_id}/{filename}', 'r') as file:
        lines: List[str] = file.readlines()
    symbols: int = 0
    lines_count: int = 0
    for line in lines:
        symbols += len(re.sub(r'\s', '', line))
        lines_count += 1
    result: Dict[str, Union[int, bool, None]] = dict.fromkeys(["TaskSymbols", "TaskRows", "UserSymbols", "UserRows",
                                                               "Symbols", "Rows"])
    result["TaskSymbols"] = length.symbols
    result["TaskRows"] = length.rows
    result["UserSymbols"] = symbols
    result["UserRows"] = lines_count
    result["Symbols"] = length.symbols > symbols
    result["Rows"] = length.rows > lines_count
    return result


__all__ = ["check_symbols"]
