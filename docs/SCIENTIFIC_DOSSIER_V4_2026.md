# RISKGUARD / INDEPENDENT CAPITAL VETO

## Научная задача и собственный исследовательский вклад

Risk officer / account state / order capacity. core.decide checks kill switch, daily loss, drawdown, historical 99% VaR, single-order notional and gross exposure. cvar is reported in metrics but not independently vetoed.

## Фактический вычислительный механизм

Historical VaR = max(0, -quantile(returns,1-alpha)); CVaR = max(0,-mean(returns below that quantile)); approved notional = min(request, equity*single_cap, max(0,equity*gross_cap-current_exposure)).

## Почему этот компонент важен для единой федерации

Это отдельный специализированный компонент — источник ограниченного, объяснимого исследования или решения. Его выводы можно передавать по типизированному контракту, не делая саму модель хозяином клиентских средств или бухгалтерского результата.

## Программа воспроизводимого эксперимента

Stress missing histories (the core returns VaR=0 for fewer than five observations), gaps, stale state, CVaR-only breaches, large orders, and risk policy revision. Require signed decision linkage, account state hashes and broker-side final capacity.

## Экспериментальный протокол и измеримые результаты

Зафиксировать исходный commit, датированные входы и их SHA-256, строгий baseline, независимую валидационную и тестовую выборки, граничные случаи, стоимость вычисления и неблагоприятные сценарии. Сравнивать на одном времени и идентичном объёме ресурсов. Публиковать не только mean score, но и распределение ошибок, устойчивость, отказные сценарии и экономические издержки. Наличие исполняемых тестов и enterprise API не доказывает реальную финансовую эффективность или production deployment.

## Подтверждающие исходники

- [`src/synergy_riskguard/core.py`](../src/synergy_riskguard/core.py)
- [`src/synergy_riskguard/synergy_contracts.py`](../src/synergy_riskguard/synergy_contracts.py)
- [`tests/`](../tests/)

## Критерий следующей версии

Перейти от предметного реализованного ядра к эксперименту с отдельным воспроизводимым manifest, автоматической CI-проверкой и фактическими доказательствами из конечной интеграции. Прежняя корневая документация сохранена полностью.
