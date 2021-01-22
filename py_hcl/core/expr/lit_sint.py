from py_hcl.core.expr import HclExpr
from py_hcl.core.stmt.connect import VariableType
from py_hcl.core.type.sint import SIntT
from py_hcl.utils import signed_num_bin_width


class SLiteral(HclExpr):
    def __init__(self, value: int):
        self.value = value

        w = signed_num_bin_width(value)
        self.hcl_type = SIntT(w)
        self.variable_type = VariableType.ReadOnly
