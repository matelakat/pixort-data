import contextlib
import tempfile
import os


@contextlib.contextmanager
def tempdb():
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        tf.close()
        try:
            yield "sqlite:///" + os.path.abspath(tf.name)
        finally:
            os.unlink(tf.name)


@contextlib.contextmanager
def tempfname():
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        tf.close()
        try:
            yield os.path.abspath(tf.name)
        finally:
            os.unlink(tf.name)
