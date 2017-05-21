# nodepy/werkzeug-reloader-patch

A monkey-patch for the Werkzeug reloader for use with [Node.Py].

    $ nodepy-pm install --save-ext @nodepy/werkzeug-reloader-patch

Alternatively, use the `install()` function before starting a
Werkzeug application.

```python
require('werkzeug-reloader-patch').install()
```

  [Node.Py]: https://github.com/nodepy/nodepy

> Note: Uses undocumented Werkzeug API.
