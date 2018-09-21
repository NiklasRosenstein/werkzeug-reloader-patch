"""
Monkey-patch for the Werkzeug application reloader.
"""

import nodepy
import functools
import sys
import warnings
import werkzeug._reloader as _reloader

_installed = False


def monkey_patch(obj, member):
  """
  Monkey-patch a function called *member* in *obj* with the decorated function.
  The original member value will be passed as the first argument.
  """

  _old = getattr(obj, member)
  def decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
      return func(_old, *args, **kwargs)
    setattr(obj, member, wrapper)
    return wrapper
  return decorator


def install():
  """
  Installs the patch for the `werkzeug._reloader` module.
  """

  global _installed
  if _installed: return

  if _reloader.reloader_loops['auto'] != _reloader.reloader_loops['stat']:
    name = module.package.name
    kind = dict((v, k) for k, v in _reloader.reloader_loops.items() if k != 'auto').get(_reloader.reloader_loops['auto'], '???')
    message = '{}: Reloader "{}" is not supported. Using "stat" reloader instead.'
    warnings.warn(message.format(name, kind), UserWarning)
    _reloader.reloader_loops['auto'] = _reloader.reloader_loops['stat']

  @monkey_patch(_reloader, '_iter_module_files')
  def _iter_module_files(__old):
    yield from __old()
    for module in require.context.modules.values():
      yield str(module.filename)

  @monkey_patch(_reloader, '_get_args_for_reloading')
  def _get_args_for_reloading(__old):
    if nodepy.runtime.script and 'args' in nodepy.runtime.script:
      return nodepy.runtime.script['args']
    else:
      args = __old()
      if not nodepy.runtime.script:
        args[0:1] = nodepy.runtime.exec_args
      return args

  _installed = True

def init_extension(*args):
  install()
