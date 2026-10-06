"""Strategy parameters are fixed by spec and must not be tuned."""


def test_strategy_params_locked(cfg):
    p = cfg.strategy
    assert (p.ema_fast, p.ema_slow, p.ema_trend, p.rsi_period) == (20, 50, 200, 14)
    assert (p.rsi_min, p.rsi_max) == (45, 70)
    assert p.swing_lookback == 10 and p.sl_buffer_pct == 0.005
    assert p.max_sl_distance_pct == 0.04 and p.reward_risk == 2
    assert p.warmup_candles >= 200


def test_risk_and_costs_locked(cfg):
    assert cfg.mode == "paper"
    assert cfg.risk.risk_per_trade_pct == 0.01 and cfg.risk.max_open_positions == 1
    assert cfg.costs.fee_pct == 0.001 and cfg.costs.slippage_pct == 0.0005
