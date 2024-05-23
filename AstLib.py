class AstContentGetter:
    def __init__(self, data: str):
        self._lines = data.splitlines()

    def get(self, v) -> str:
        # linenos are 1-based

        first_line = self._lines[v.lineno - 1]

        if v.end_lineno == v.lineno:
            # one line only
            return first_line[v.col_offset:v.end_col_offset]

        # multiline
        ret = []
        ret.append(first_line[v.col_offset:])
        # intermediary lines
        if v.end_lineno != v.lineno:
            for li in range(v.lineno, v.end_lineno - 1):
                ret.append(self._lines[li])
        # last line
        ret.append(self._lines[v.end_lineno - 1][:v.end_col_offset])
        return '\n'.join(ret)
