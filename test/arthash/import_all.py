import importlib, os

# From https://github.com/ManiacalLabs/BiblioPixel/blob/master/test/bibliopixel/import_all.py


def _split_all(path):
    result = []
    old_path = None
    while path != old_path:
        (path, tail), old_path = os.path.split(path), path
        tail and result.insert(0, tail)
    return result


def _all_imports(root, project_name):
    python_root = os.path.join(root, project_name)
    for directory, sub_folders, files in os.walk(python_root):
        if '__' in directory:
            continue

        relative = os.path.relpath(directory, root)
        root_import = '.'.join(_split_all(relative))

        yield root_import

        for f in files:
            if f.endswith('.py') and '__' not in f:
                yield '%s.%s' % (root_import, f[:-3])


def import_all(root, project_name, blacklist):
    """Import all files and directories """
    successes, failures = [], []
    for name in _all_imports(root, project_name):
        if name not in blacklist:
            try:
                importlib.import_module(name)
            except Exception as e:
                failures.append((name, e))
            else:
                successes.append(name)

    return successes, failures
