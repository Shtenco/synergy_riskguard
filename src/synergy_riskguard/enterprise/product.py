from __future__ import annotations
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from ..core import AccountState, Action, Limits, OrderIntent, decide
from .models import Principal, Role
from .service import EnterpriseRuntime, principal_dependency, request_id_header

class StateModel(BaseModel):
    equity:float; start_day_equity:float; high_watermark:float; gross_exposure:float
    returns:list[float]=Field(default_factory=list); kill_switch:bool=False
class OrderModel(BaseModel): symbol:str; notional:float; side:str
class LimitsModel(BaseModel):
    max_daily_loss:float=.03; max_drawdown:float=.10; max_gross_exposure:float=2.0; max_single_position:float=.25; var_limit:float=.05; confidence:float=.99
class RiskRequest(BaseModel): state:StateModel; order:OrderModel; limits:LimitsModel=Field(default_factory=LimitsModel)

def build_product_router(runtime:EnterpriseRuntime)->APIRouter:
    router=APIRouter(prefix="/enterprise/v1/risk",tags=["enterprise-riskguard"])
    @router.post("/check")
    async def check(req:RiskRequest, principal:Principal=Depends(principal_dependency(runtime,{Role.TRADER,Role.RISK})), request_id:str=Depends(request_id_header)):
        state=AccountState(**{**req.state.model_dump(),"returns":tuple(req.state.returns)})
        order=OrderIntent(**req.order.model_dump()); limits=Limits(**req.limits.model_dump())
        result=decide(state,order,limits).to_dict();result["request_id"]=request_id
        runtime.record(principal,action="riskguard.pretrade.check",request_id=request_id,payload={"symbol":order.symbol,"decision":result["action"],"approved_notional":result["approved_notional"],"reasons":result["reasons"]})
        runtime.metrics.inc("product_requests_total",labels={"action":"risk_check","decision":result["action"]})
        return result
    return router
