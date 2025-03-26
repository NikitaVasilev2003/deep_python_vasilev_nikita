def filter_file(file, search_words, stop_words):
    search_lower = {word.lower() for word in search_words}
    stop_lower = {word.lower() for word in stop_words}

    if isinstance(file, str):
        with open(file, "r", encoding="utf-8") as file_obj:
            yield from _process_lines(file_obj, search_lower, stop_lower)
    else:
        yield from _process_lines(file, search_lower, stop_lower)


def _process_lines(file_obj, search_lower, stop_lower):
    for line in file_obj:
        stripped_line = line.strip()
        words = stripped_line.split()
        words_lower = [word.lower() for word in words]

        if any(word in stop_lower for word in words_lower):
            continue

        if any(word in search_lower for word in words_lower):
            yield stripped_line
