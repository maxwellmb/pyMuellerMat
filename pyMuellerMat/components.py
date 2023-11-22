from collections import OrderedDict
from dataclasses import dataclass
from typing import Any, Optional, Callable
from numpy.typing import NDArray
import numpy as np
import timeit
from pydantic import BaseModel, Field
import tomli
import tomli_w
import datetime

from pyMuellerMat.mm_functions import lp_mm, wp_mm


class System(BaseModel):
    name: str = ""
    filter: str = ""
    date: datetime.date = datetime.date.today()
    components: OrderedDict[str, Callable]

    def __call__(self) -> NDArray:
        mms = [comp() for comp in reversed(self.components.values())]
        return np.linalg.multi_dot(mms)
    
    def to_dict(self) -> dict:
        # get model as nested dictionary
        # round-trip ensures sys can be recreated from output,
        # and JSON makes sure all types are safe for serialization
        return self.model_dump(mode="json", round_trip=True)


class LinearPolarizer(BaseModel):
    theta: float = 0

    def __call__(self) -> NDArray:
        return lp_mm(self.theta)

class GenericWaveplate(BaseModel):
    theta: float = 0
    delta: float = 0

    def __call__(self) -> NDArray:
        return wp_mm(self.theta, self.delta)


if __name__ == "__main__":
    # demo
    # generate circular polarized light
    lp = LinearPolarizer(theta=0)
    qwp = GenericWaveplate(theta=np.pi/4, delta=np.pi/2)
    sys = System(
        name="test",
        filter="Open",
        components=OrderedDict(lp=lp, qwp=qwp)
    )
    
    M = sys()
    np.set_printoptions(suppress=True)
    print(M)
    S = np.array((1, 0, 0, 0))
    print(S)
    print(M @ S)

    res = timeit.timeit(sys, number=10000)
    print(f"Average time to evaluate MM (n=1e4): {res*1e3:.02e} ms")


    model_dict = sys.to_dict()

    import pprint
    print("Model as dictionary")
    print("-------------------")
    pprint.pprint(model_dict)

    print("\nModel as TOML")
    print("-------------------")
    print(tomli_w.dumps(model_dict))