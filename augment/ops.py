class RegisterShape(object):
  """No longer used.

  Was: A decorator for registering a shape function.

  Shape functions must now be registered via the SetShapeFn on the
  original Op specification in C++.

  """

  def __init__(self, op_type):
    """Saves the `op_type` as the `Operation` type."""
    if not isinstance(op_type, six.string_types):
      raise TypeError("op_type must be a string")
    self._op_type = op_type

  def __call__(self, f):
    """Registers "f" as the shape function for "op_type"."""
    if f is None:
      assert _call_cpp_shape_fn

      # None is a special "weak" value that provides a default shape function,
      # and can be overridden by a non-None registration.
      try:
        _default_shape_function_registry.register(_call_cpp_shape_fn,
                                                  self._op_type)
      except KeyError:
        # Ignore duplicate registrations of the weak value. This can
        # occur if the op library input to wrapper generation
        # inadvertently links in one or more of the standard op
        # libraries.
        pass
    else:
      _shape_registry.register(f, self._op_type)
    return f
