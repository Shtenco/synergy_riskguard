from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from .core import AccountState,OrderIntent,Limits,decide
app=FastAPI(title="SYNERGY RiskGuard",version="2.0.0")
class State(BaseModel):
    equity:float; start_day_equity:float; high_watermark:float; gross_exposure:float; returns:list[float]=[]; kill_switch:bool=False
class Order(BaseModel): symbol:str; notional:float; side:str
class Request(BaseModel): state:State; order:Order
@app.get('/health')
def health():return {'ok':True,'service':'riskguard'}
@app.post('/v1/check')
def check(req:Request):
    s=AccountState(**{**req.state.model_dump(),'returns':tuple(req.state.returns)})
    return decide(s,OrderIntent(**req.order.model_dump()),Limits()).to_dict()

# Enterprise v2 control/data plane
from .enterprise.service import EnterpriseRuntime, build_enterprise_router, install_observability
from .enterprise.product import build_product_router
enterprise_runtime=EnterpriseRuntime.from_env(service_name='synergy-riskguard')
install_observability(app,enterprise_runtime)
app.include_router(build_enterprise_router(enterprise_runtime))
app.include_router(build_product_router(enterprise_runtime))

if __name__=='__main__': uvicorn.run(app,host='0.0.0.0',port=8000)
