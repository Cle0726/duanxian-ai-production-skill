#!/usr/bin/env python3
"""Compatibility entry point. Current smoke suite is V4.4."""
from run_v44_smoke_tests import main
if __name__ == '__main__':
    raise SystemExit(main())
