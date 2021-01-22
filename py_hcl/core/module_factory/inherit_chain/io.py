from typing import Dict, Union, Optional, Tuple

from py_hcl.core.expr.error import ExprError
from py_hcl.core.expr.io import Input, Output, IO
from py_hcl.core.type.bundle import BundleT, BundleDirection
from py_hcl.core.utils import module_inherit_mro
from py_hcl.utils.serialization import json_serialize


@json_serialize
class IOHolder(object):
    def __init__(self,
                 named_ports: Dict[str, Union[Input, Output]],
                 module_name: Optional[str] = None):
        self.named_ports = named_ports
        self.module_name = module_name


def io_extend(modules: Tuple[type]):
    modules = module_inherit_mro(modules)

    current_ports = {}
    io_chain = []
    for m in modules[::-1]:
        h = m.io.io_chain[0]
        current_ports.update(h.named_ports)
        io_chain.insert(0, h)

    def _(named_ports: Dict[str, Union[Input, Output]]):
        current_ports.update(named_ports)
        io_chain.insert(0, IOHolder(named_ports))
        return IO(__build_bundle_type_from_ports(current_ports), io_chain)

    return _


def __build_bundle_type_from_ports(
        named_ports: Dict[str, Union[Input, Output]]) -> BundleT:
    fields = {}
    for k, v in named_ports.items():
        if isinstance(v, Input):
            fields[k] = {"dir": BundleDirection.SOURCE, "hcl_type": v.hcl_type}
            continue

        if isinstance(v, Output):
            fields[k] = {"dir": BundleDirection.SINK, "hcl_type": v.hcl_type}
            continue

        raise ExprError.io_value_err(
            "type of '{}' is {}, not Input or Output".format(k, type(v)))

    return BundleT(fields)
