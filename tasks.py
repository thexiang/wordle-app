from invoke import Collection

from pyinvoke_tasks import local

namespace = Collection(local)
namespace.configure({'run': {'echo': True}})
