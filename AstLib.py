class AstContentGetter:
    '''
    A class to get the code of an AST node parsed from the given file.
    This is the same in function as ast.get_source_segment, but avoids
    repeatedly splitting the lines.
    '''
    def __init__(self, data: str):
        '''
        Initialise this class with the contents of the source file that was
        passed to the ast.parse().
        '''
        self._lines = data.splitlines()

    def get(self, v) -> str:
        '''
        Returns the snippet of the source code that represents the given
        ast.parse() node.
        '''
        # lineno is 1-based, but col_offset is 0-based
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
