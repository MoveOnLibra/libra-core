#!/bin/bash
flake8 libra --exclude=libra/proto --count --select=E9,F --show-source --statistics
