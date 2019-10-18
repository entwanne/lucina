from lucina.utils import open_files


def test_open_files(mocker):
    def mock_open(filename, *args, **kwargs):
        f = mocker.MagicMock()
        f.filename = filename
        f.args = args
        f.kwargs = kwargs
        f.__enter__.return_value = f
        return f
    mocker.patch('builtins.open', side_effect=mock_open)

    with open_files(['a', 'b']) as files:
        assert len(files) == 2
        assert files[0].filename == 'a'
        assert files[1].filename == 'b'

    with open_files(['foo'], 'r', encoding='utf-8') as files:
        assert len(files) == 1
        assert files[0].filename == 'foo'
        assert files[0].args == ('r',)
        assert files[0].kwargs == {'encoding': 'utf-8'}
