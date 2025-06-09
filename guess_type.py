from visidata import BaseSheet, anytype, options, vd
import itertools

@BaseSheet.api
def guessType(self, *args):
    cols = self.visibleCols
    rows = self.rows

    for col in cols:
        if col.type is not anytype:
            continue

        max_to_check = 20
        current_type = None

        for val in itertools.islice((col.getValue(r) for r in rows), max_to_check):
            if not str(val):
                continue
            try:
                fv = float(val)
                is_int = float(int(fv)) == fv
                if is_int and current_type is None:
                    current_type = int
                else:
                    current_type = float
                    break
            except Exception:
                pass

        col.type = anytype if current_type is None else current_type

BaseSheet.addCommand(
    'gr', 
    'guess-types', 
    'guessType()',
    'Guess column types based on values.'
)
