import contextlib
from datetime import datetime, timezone
import json
import numpy as np
import os
from pandas import DataFrame
import warnings
import _pickle as cPickle

# I/O

def save(obj: object, prefixe: str = "output", format: str = "pickle") -> int:

    assert (
        format == "json" or format == "pickle"
    ), "File format is not supported"

    if format in ["json", "pickle"]:

        if isinstance(obj,DataFrame):
            obj = obj.to_dict(orient='list')

        FILES = {
            "json": {"ext": "json", "mode": "w", "func": json.dump},
            "pickle": {"ext": "pkl", "mode": "wb", "func": cPickle.dump},
        }

        with open(
            file=f"{prefixe}.{FILES[format]['ext']}",
            mode=FILES[format]["mode"],
        ) as f:
            FILES[format]["func"](obj, f)

        assert os.path.isfile(
            f"{prefixe}.{FILES[format]['ext']}"
        ), "File was not created"

        return 1
    else:
        raise ValueError(f"Error: The file format {format} is not supported.")


def is_file(path: str) -> bool:
    return os.path.isfile(path)


def is_empty(path: str) -> bool:
    return os.path.getsize(path) == 0


def is_indexed(path: str) -> bool:
    return verify_file(path)


def verify_file(file: str):

    assert isinstance(file, str), "Values must be of string instance"

    if not is_file(file):

        raise FileNotFoundError(f"Error: The file '{file}' does not exist.")

    if is_empty(file):

        raise ValueError(f"Error: The file '{file}' is empty.")
    
def file_stats(path: str) -> dict:
    
    statinfo = os.stat(path)

    return {"basename": os.path.basename(path),
            "path": os.path.dirname(path),
            "size": round(statinfo.st_size / pow(1024,2),2),
            "mtime": datetime.fromtimestamp(statinfo.st_mtime, tz=timezone.utc)}

@contextlib.contextmanager
def suppress_warnings():
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="no intervals found for*")
        warnings.filterwarnings("ignore", message="Mean of empty slice.")
        yield

# SETS


def intersect(a: set[str], b: set[str]) -> set:
    return a & b


def difference(a: set[str], b: set[str]) -> set:
    return a - b

def jaccard_index(shared: int, total: dict) -> float:
    try:
        return shared / total
    except ZeroDivisionError:
        return None

# Variables

def convert(a: object) -> object:

    try:
        return a if any(list(map(lambda x: x in a,('/','|')))) else eval(a)
    except Exception:
        return a


# Variants

def hamming_distance(a: np.ndarray, b: np.ndarray) -> float:
    try:
        return 1 - ((np.sum(np.not_equal(a, b))) / (a.size + b.size))
    except ZeroDivisionError:
        return None

def is_homozygous(GT: str):
    if '/' in GT:
        alleles = GT.split('/')
    elif '|' in GT:
        alleles = GT.split('|')
    
    return alleles[0] == alleles[1]

def is_heterozygous(GT: str):
    if '/' in GT:
        alleles = GT.split('/')
    elif '|' in GT:
        alleles = GT.split('|')
    
    return alleles[0] != alleles[1]

def exclude(v: object, filters: dict = None) -> bool:

    return (
            v.is_indel and filters["exclude"]["exclude_indels"]
        ) or (
            v.is_snp and filters["exclude"]["exclude_snps"]
        ) or (
            v.is_mnp and filters["exclude"]["exclude_mnps"]
        ) or (
            v.is_sv and filters["exclude"]["exclude_svs"]
        ) or (
            v.is_transition and filters["exclude"]["exclude_transitions"]
        ) or (
            (v.FILTER != None) and filters["exclude"]["pass_only"]
        ) if filters else False

def format_to_values(format: str, values: str|list[str]) -> dict:

    format = format.split(":")

    if isinstance(values,list):

        values = list(map(lambda x: x.split(":"), values))

        return {f"sample{s}": {f: convert(v)} for s in range(len(values)) for f, v in zip(format,values[s])}

    else:

        values = values.split(":")

        return {f: convert(v) for f, v in zip(format,values)}