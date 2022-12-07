import pytest
import monitoring


class TestAddRow:

    @pytest.mark.parametrize(['element', 'column_info', 'wrap', 'col_max', 'expected'], [
        ({'first': "this", 'second': "is a row"}, [("heading", "first"), ("heading2", "second")], 50, {'first': 7, 'second': 8}, "this    | is a row | \n"),
        ({'first': "this", 'second': "is a row that will wrap"}, [("heading", "first"), ("heading2", "second")], 13, {'first': 7, 'second': 23}, "this    | is a row that | \n        | will wrap     | \n")
    ])
    def test_expected(self, element, column_info, wrap, col_max, expected):
        assert monitoring.add_row(element, column_info, wrap, col_max) == expected
