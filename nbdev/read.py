# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_read.ipynb.

#nbdev_cell auto 0
__all__ = ['NbCell', 'dict2nb', 'read_nb', 'nbdev_create_config', 'update_version', 'add_init', 'cell_header', 'export_cells', 'create_all_cell']


#nbdev_cell ../nbs/00_read.ipynb 2
#export
from fastcore.imports import *
from fastcore.foundation import *
from fastcore.utils import *
from fastcore.test import *
from fastcore.script import *

import json,ast


#nbdev_cell ../nbs/00_read.ipynb 13
#export
class NbCell(AttrDict):
    def __init__(self, idx, cell):
        for k,v in cell.items(): self[k] = v
        self.idx = idx
        if 'source' in self: self.set_source(self.source)

    def __repr__(self): return self.source
    
    def set_source(self, source):
        self.source = ''.join(source)
        if self.cell_type=='code' and self.source[:1]!='%':self.parsed = ast.parse(self.source).body


#nbdev_cell ../nbs/00_read.ipynb 15
#export
def dict2nb(js):
    "Convert a dict to an `AttrDict`, "
    nb = dict2obj(js)
    nb.cells = nb.cells.enumerate().starmap(NbCell)
    return nb


#nbdev_cell ../nbs/00_read.ipynb 23
#export
def read_nb(path):
    "Return notebook at `path`"
    with open(path) as f: return dict2nb(json.loads(f.read()))


#nbdev_cell ../nbs/00_read.ipynb 26
#export
@call_parse
def nbdev_create_config(
    user:Param("Repo username", str),
    host:Param("Repo hostname", str)='github',
    lib_name:Param("Name of library", str)=None,
    path:Param("Path to create config file", str)='.',
    cfg_name:Param("Name of config file to create", str)='settings.ini',
    branch:Param("Repo branch", str)='master',
    git_url:Param("Repo URL", str)="https://github.com/%(user)s/%(lib_name)s/tree/%(branch)s/",
    custom_sidebar:Param("Create custom sidebar?", bool_arg)=False,
    nbs_path:Param("Name of folder containing notebooks", str)='.',
    lib_path:Param("Folder name of root module", str)='%(lib_name)s',
    doc_path:Param("Folder name containing docs", str)='docs',
    tst_flags:Param("Test flags", str)='',
    version:Param("Version number", str)='0.0.1',
    **kwargs
):
    "Creates a new config file for `lib_name` and `user` and saves it."
    if lib_name is None:
        parent = Path.cwd().parent
        lib_name = parent.parent.name if parent.name=='nbs' else parent.name
    g = locals()
    config = {o:g[o] for o in 'host lib_name user branch git_url lib_path nbs_path doc_path \
        tst_flags version custom_sidebar'.split()}
    config = {**config, **kwargs}
    save_config_file(Path(path)/cfg_name, config)


#nbdev_cell ../nbs/00_read.ipynb 29
#export
_init,_version = '__init__.py','version.py'
def update_version(path:Path):
    "Add or update `__version__` in `version.py`"
    path = Path(path)
    (path/_version).write_text(f"__version__='{Config().version}'\n")


#nbdev_cell ../nbs/00_read.ipynb 30
#export
def _has_py(fs): return any(1 for f in fs if f.endswith('.py'))

def add_init(path):
    "Add `__init__.py` in all subdirs of `path` containing python files if it's not there already"
    # we add the lowest-level `__init__.py` files first, which ensures _has_py succeeds for parent modules
    path = Path(path)
    if not (path/_version).exists(): update_version(path)
    if not (path/_init).exists(): (path/_init).write_text("from .version import __version__\n")
    for r,ds,fs in os.walk(path, topdown=False):
        r = Path(r)
        subds = (os.listdir(r/d) for d in ds)
        if _has_py(fs) or any(filter(_has_py, subds)) and not (r/_init).exists(): (r/_init).touch()


#nbdev_cell ../nbs/00_read.ipynb 32
#export
@with_cast
def cell_header(nb_path:Path, lib_path:Path):
    "Create `#nbdev_cell {source file}` header"
    return f"#nbdev_cell {os.path.relpath(nb_path.resolve(), lib_path)}"


#nbdev_cell ../nbs/00_read.ipynb 33
#export
def export_cells(cells, hdr, file, offset=0):
    "Export `cells` to `file`"
    for cell in cells: file.write(f'{hdr} {cell.idx}\n{cell}\n\n\n')


#nbdev_cell ../nbs/00_read.ipynb 34
#export
def create_all_cell(vs):
    "Create string that defines `__all__` with `vs`"
    return f"#nbdev_cell auto 0\n__all__ = {list(vs)}\n\n\n"


