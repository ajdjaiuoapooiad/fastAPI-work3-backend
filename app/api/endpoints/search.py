from fastapi import APIRouter, Depends, Query
from typing import Optional

from app.api.models.search import SearchRequest, SearchResponse, GitHubRepository
from app.core.github_client import search_repositories

router = APIRouter()

@router.get("/search", response_model=SearchResponse)
async def search(search_request: SearchRequest = Depends()):
    """
    指定されたキーワードとユーザー名で GitHub リポジトリを検索します。
    """
    repositories: List[GitHubRepository] = await search_repositories(
        keyword=search_request.keyword,
        username=search_request.username,
        sort=search_request.sort,
        order=search_request.order,
        page=search_request.page,
    )
    return SearchResponse(items=repositories)