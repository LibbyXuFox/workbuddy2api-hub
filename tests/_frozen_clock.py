"""A frozen clock defined by local wall time, not by an absolute epoch.

Every usage/bucket suite pins `time.time()` so that windows, day buckets and
`started` are comparable across runs. That clock used to be the literal
`1791445200.0` — a fixed instant that reads as 15:40 in UTC+8 (where it was
written) but as **00:40** in UTC-7. The fixtures are built from *local
midnight* (rows around `TODAY0 ± 1h`, "today's series", "an empty window two
hours back"), so in a zone where the frozen instant lands just after midnight
the rows fall into yesterday and the assertions flip: `_test_usage_cache_kinds`
sees an empty series, `_test_usage_series_minutes` sees a "empty" window full
of rows. Same code, same data, different machine time zone.

Defining the clock as local 2026-10-08 15:40 keeps every suite on the same
instant while staying far from midnight in *any* zone, so the fixtures mean the
same thing everywhere. CI (UTC) and the author's UTC+8 both used to pass by
luck; UTC-7 did not.
"""

import time

#: 2026-10-08 15:40 local. `tm_isdst=-1` lets mktime pick the zone's own DST
#: rule, so the instant is a real wall-clock time rather than a fixed epoch.
FROZEN = time.mktime((2026, 10, 8, 15, 40, 0, 0, 0, -1))
