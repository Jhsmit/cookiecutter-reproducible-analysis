import shutil
from pathlib import Path
from io import StringIO, BytesIO
import re
import json
import pandas as pd
import yaml


def longpath(pth: Path) -> Path:
    """Converts input `pth` to long path compatible format"""
    return Path(r"//?/" + str(pth))


def read_header(file_obj, comment="#"):
    header = []

    while True:
        line = file_obj.readline()
        line = line.decode() if isinstance(line, bytes) else line
        if line.startswith(comment):
            header.append(line)
        else:
            break
    return header


def parse_header(filepath_or_buffer, comment="#"):
    if isinstance(filepath_or_buffer, (StringIO, BytesIO)):
        header = read_header(filepath_or_buffer, comment=comment)
        filepath_or_buffer.seek(0)
    else:
        with open(filepath_or_buffer, "r") as file_obj:
            header = read_header(file_obj, comment=comment)

    header = [h.strip("#\n ") for h in header]
    pattern = r"<[^>]+>"
    header_dict = {}
    for line in header:
        tags = re.findall(r"<[^>]+>", line)
        if len(tags) == 2 and tags[0] == tags[1].replace("/", ""):
            name = tags[0].strip("<>")
            content = json.loads(re.sub(pattern, "", line))
            header_dict[name] = content

    return header_dict


def csv_to_dataframe(filepath_or_buffer, comment="#", **kwargs):
    """
    Reads a .csv file or buffer into a :pandas:`DataFrame` object.
    Comment lines are parsed where json dictionaries marked by tags are read.
    The <pandas_kwargs> marked json dict is used as kwargs for `pd.read_csv`
    The <metadata> marked json dict is stored in the returned dataframe object as `df.attrs['metadata'].

    Parameters
    ----------
    filepath_or_buffer : :obj:`str`, pathlib.Path or io.StringIO
        Filepath or StringIO buffer to read.
    comment : :obj:`str`
        Indicates which lines are comments.
    kwargs
        Optional additional keyword arguments passed to `pd.read_csv`
    Returns
    -------
    df: pd.DataFrame
    """

    if comment is not None:
        header_dict = parse_header(filepath_or_buffer, comment=comment)
    else:
        header_dict = {}

    pd_kwargs = header_dict.get("pandas_kwargs", {})
    pd_kwargs.update(kwargs)
    df = pd.read_csv(filepath_or_buffer, **pd_kwargs)
    if "metadata" in header_dict:
        df.attrs["metadata"] = header_dict["metadata"]
    return df


def dataframe_to_stringio(
    df, sio=None, fmt="csv", include_metadata=True, include_version=True, **kwargs
):
    """
    Save a pd.DataFrame to an io.StringIO object. Kwargs to read the resulting .csv object with pd.read_csv to
    get the original pd.DataFrame back are included in the comments.
    Optionally additional metadata or the version of PyHDX used can be included in the comments.

    Parameters
    ----------
    df: pd.DataFrame
        The pandas dataframe to write to the io.StringIO object.
    sio: `io.StringIO`, optional
        The `io.StringIO` object to write to. If `None`, a new `io.StringIO` object is created.
    fmt: :obj:`str`
        Specify the formatting of the output. Options are 'csv' (machine readable) or 'pprint' (human readable)
    include_metadata: :obj:`bool` or :obj:`dict`
        If `True`, the metadata in df.attrs['metadata'] is included. If :obj:`dict`, this dictionary is used as the
        metadata. If `False`, no metadata is included.
    include_version : :obj:`bool`
        `True` to include PyHDX version information.
    **kwargs : :obj:`dict`, optional
            Optional additional keyword arguments passed to `df.to_csv`


    Returns
    -------
    sio: io.StringIO
        Resulting io.StringIO object.

    """
    sio = sio or StringIO()

    json_header = {}
    if include_metadata and "metadata" in df.attrs:
        json_header["metadata"] = df.attrs["metadata"]
    elif isinstance(include_metadata, dict):
        json_header["metadata"] = include_metadata

    if fmt == "csv":
        json_header["pandas_kwargs"] = {
            "comment": "#",
            "header": list(range(df.columns.nlevels)),
            "index_col": 0,
        }
        for k, v in json_header.items():
            if v:
                sio.write(f"# <{k}>{json.dumps(v)}</{k}>\n")
        df.to_csv(sio, line_terminator="\n", **kwargs)
    elif fmt == "pprint":
        if include_version:
            sio.write("\n")
        for k, v in json_header.items():
            if v:
                sio.write(f'{k.capitalize().replace("_", " ")}\n')
                sep = len(k) * "-"
                sio.write(f"{sep}\n")
                sio.write(yaml.dump(v, sort_keys=False))
                sio.write("\n")
        # use df.to_string()?
        with pd.option_context(
            "display.max_rows",
            None,
            "display.max_columns",
            None,
            "display.expand_frame_repr",
            False,
        ):
            sio.write(df.__str__())
    else:
        raise ValueError(
            f"Invalid specification for fmt: '{fmt}', must be 'csv' or 'pprint'"
        )

    sio.seek(0)
    return sio


def dataframe_to_file(
    file_path, df: pd.DataFrame, fmt: str = "csv", include_metadata:bool = True, include_version:bool=False, **kwargs
):
    """
    Save a pd.DataFrame to an io.StringIO object. Kwargs to read the resulting .csv object with pd.read_csv to
    get the original pd.DataFrame back are included in the comments.
    Optionally additional metadata or the version of PyHDX used can be included in the comments.

    Parameters
    ----------
    file_path: :obj:`str` or `pathlib.Path`
        File path of the target file to write.
    df: pd.DataFrame
        The pandas dataframe to write to the file.
    fmt: :obj:`str`
        Specify the formatting of the output. Options are '.csv' (machine readable) or 'pprint' (human readable)
    include_metadata: :obj:`bool` or :obj:`dict`
        If `True`, the metadata in df.attrs['metadata'] is included. If :obj:`dict`, this dictionary is used as the
        metadata. If `False`, no metadata is included.
    include_version : :obj:`bool`
        `True` to include PyHDX version information.
    **kwargs : :obj:`dict`, optional
            Optional additional keyword arguments passed to `df.to_csv`


    Returns
    -------
    sio: io.StringIO
        Resulting io.StringIO object.

    """
    sio = dataframe_to_stringio(
        df,
        fmt=fmt,
        include_metadata=include_metadata,
        include_version=include_version,
        **kwargs,
    )
    with open(file_path, "w") as f:
        sio.seek(0)
        shutil.copyfileobj(sio, f)
