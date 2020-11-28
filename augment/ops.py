import six
import collections
import copy
import re
import sys
import threading

import numpy as np
import six
from six.moves import xrange  # pylint: disable=redefined-builtin
from tensorflow.core.framework import attr_value_pb2
from tensorflow.core.framework import function_pb2
from tensorflow.core.framework import graph_pb2
from tensorflow.core.framework import node_def_pb2
from tensorflow.core.framework import op_def_pb2
from tensorflow.core.framework import versions_pb2
from tensorflow.core.protobuf import config_pb2
from tensorflow.python import pywrap_tensorflow as c_api
from tensorflow.python import tf2
from tensorflow.python.eager import context
from tensorflow.python.eager import core
from tensorflow.python.eager import tape
from tensorflow.python.framework import c_api_util
from tensorflow.python.framework import composite_tensor
from tensorflow.python.framework import device as pydev
from tensorflow.python.framework import dtypes
from tensorflow.python.framework import errors
from tensorflow.python.framework import op_def_registry
from tensorflow.python.framework import registry
from tensorflow.python.framework import tensor_shape
from tensorflow.python.framework import traceable_stack
from tensorflow.python.framework import versions
from tensorflow.python.ops import control_flow_util
from tensorflow.python.platform import app
from tensorflow.python.platform import tf_logging as logging
from tensorflow.python.util import compat
from tensorflow.python.util import decorator_utils
from tensorflow.python.util import deprecation
from tensorflow.python.util import function_utils
from tensorflow.python.util import lock_util
from tensorflow.python.util import memory
from tensorflow.python.util import tf_contextlib
from tensorflow.python.util import tf_stack
from tensorflow.python.util.deprecation import deprecated_args
from tensorflow.python.util.lazy_loader import LazyLoader
from tensorflow.python.util.tf_export import tf_export



_call_cpp_shape_fn = None
_call_cpp_shape_fn_and_require_op = None

_shape_registry = registry.Registry("shape functions")
_default_shape_function_registry = registry.Registry("default shape functions")
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
