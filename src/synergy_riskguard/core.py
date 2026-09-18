from __future__ import annotations
from dataclasses import dataclass, asdict
from enum import Enum
from statistics import NormalDist
import numpy as np

class Action(str,Enum):
    ALLOW="ALLOW"; RESIZE="RESIZE"; REJECT="REJECT"; KILL_SWITCH="KILL_SWITCH"

@dataclass(frozen=True)
class Limits:
    max_daily_loss: float=.03
    max_drawdown: float=.10
    max_gross_exposure: float=2.0
    max_single_position: float=.25
    var_limit: float=.05
    confidence: float=.99

@dataclass(frozen=True)
class AccountState:
    equity: float
    start_day_equity: float
    high_watermark: float
    gross_exposure: float
    returns: tuple[float,...]=()
    kill_switch: bool=False

@dataclass(frozen=True)
class OrderIntent:
    symbol:str; notional:float; side:str

@dataclass(frozen=True)
class Decision:
    action:Action; approved_notional:float; reasons:tuple[str,...]; metrics:dict
    def to_dict(self):
        d=asdict(self); d['action']=self.action.value; return d

def historical_var(returns, confidence=.99):
    r=np.asarray(returns,dtype=float)
    if r.size < 5:return 0.0
    return float(max(0.0,-np.quantile(r,1-confidence)))

def cvar(returns, confidence=.99):
    r=np.asarray(returns,dtype=float)
    if r.size < 5:return 0.0
    q=np.quantile(r,1-confidence); tail=r[r<=q]
    return float(max(0.0,-tail.mean())) if tail.size else 0.0

def decide(state:AccountState, order:OrderIntent, limits:Limits=Limits())->Decision:
    reasons=[]
    if state.kill_switch:return Decision(Action.KILL_SWITCH,0.0,("manual_or_system_kill_switch",),{})
    daily_loss=max(0.0,(state.start_day_equity-state.equity)/max(state.start_day_equity,1e-12))
    dd=max(0.0,(state.high_watermark-state.equity)/max(state.high_watermark,1e-12))
    var=historical_var(state.returns,limits.confidence); es=cvar(state.returns,limits.confidence)
    metrics={"daily_loss":daily_loss,"drawdown":dd,"historical_var":var,"cvar":es,"gross_exposure":state.gross_exposure}
    if daily_loss>=limits.max_daily_loss: reasons.append("daily_loss_limit")
    if dd>=limits.max_drawdown: reasons.append("drawdown_limit")
    if var>=limits.var_limit: reasons.append("var_limit")
    if reasons:return Decision(Action.REJECT,0.0,tuple(reasons),metrics)
    cap=max(0.0, state.equity*limits.max_single_position)
    remaining=max(0.0,state.equity*limits.max_gross_exposure-state.gross_exposure)
    approved=min(abs(order.notional),cap,remaining)
    action=Action.ALLOW if approved>=abs(order.notional)-1e-9 else Action.RESIZE
    if approved<=0:return Decision(Action.REJECT,0.0,("exposure_limit",),metrics)
    return Decision(action,approved,tuple(reasons),metrics)
