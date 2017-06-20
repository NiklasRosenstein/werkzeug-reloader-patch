# Copyright (c) 2017 Niklas Rosenstein
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
This Node.Py module installs a monkey-patch to get the Werkzeug reloader
to work with the Node.Py runtime. Note that this currently only works with
the `stat` based Werkzeug reloader.
"""

import nodepy
import functools
import sys
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

  if _reloader.reloader_loops['auto'] == _reloader.reloader_loops['watchdog']:
    print("[werkzeug-reloader - WARNING]: default reloader is 'watchdog', "
          "werkzeug-reloader only supports 'stat'.", file=sys.stderr)

  @monkey_patch(_reloader, '_iter_module_files')
  def _iter_module_files(__old):
    yield from __old()
    for filename in require.context._module_cache.keys():
      yield filename

  @monkey_patch(_reloader, '_get_args_for_reloading')
  def _get_args_for_reloading(__old):
    args = __old()
    args[0:1] = nodepy.proc_args
    return args

  _installed = True

def init_extension(package, module):
  install()
