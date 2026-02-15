def normalize(path: str) -> str:
    path_stack: list[str] = []
    path_list = path.split("/")
    for p in path_list:
        if p == "..":
            if path_stack:
                path_stack.pop()
        elif p == "." or p == "":
            continue
        else:
            path_stack.append(p.strip())
    return "/" + "/".join(path_stack)
