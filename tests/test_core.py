from synergy_riskguard.core import *

def test_drawdown_rejects():
    s=AccountState(90,100,110,0,tuple([-.01]*20))
    d=decide(s,OrderIntent('EURUSD',10,'BUY'))
    assert d.action==Action.REJECT

def test_position_cap_resizes():
    s=AccountState(100,100,100,0,tuple([0.001]*20))
    d=decide(s,OrderIntent('BTCUSD',80,'BUY'))
    assert d.action==Action.RESIZE and d.approved_notional==25

def test_kill_switch():
    s=AccountState(100,100,100,0,(),True)
    assert decide(s,OrderIntent('X',1,'BUY')).action==Action.KILL_SWITCH
