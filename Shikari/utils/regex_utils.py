from regex import search

async def regex_searcher(regex_string: str, string: str) -> str:
    try:
        re_search = search(regex_string, string, timeout=6)
    except TimeoutError:
        return False
    except Exception:
        return False

    return re_search


async def infinite_loop_check(regex_string: str) -> bool:
    loop_matches = (
        r"\((.{1,}[\+\*]){1,}\)[\+\*]."
        r"[\(\[].{1,}\{\d(,)?\}[\)\]]\{\d(,)?\}"
        r"\(.{1,}\)\{.{1,}(,)?\}\(.*\)(\+|\* |\{.*\})"
    )

    for match in loop_matches:
        match_1 = search(match, regex_string)

    return bool(match_1)
