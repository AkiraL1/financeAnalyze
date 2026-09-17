from fastapi import APIRouter, Query

from catalog.registry import load_catalog
from desk.board import build_board, build_overview
from desk.intel import build_intel
from desk.review import build_review
from oracle.intel import intel_gateway

router = APIRouter()


@router.get("/api/overview")
def overview() -> dict:
    return build_overview()


@router.get("/api/board")
def board() -> dict:
    return build_board()


@router.get("/api/intel")
def intel(live: bool = Query(default=False)) -> dict:
    catalog = load_catalog()
    snapshot = intel_gateway().snapshot(None) if live else None
    return build_intel(catalog, snapshot)


@router.get("/api/review")
def review(oracle: bool = Query(default=False)) -> dict:
    return build_review(include_oracle=oracle)
