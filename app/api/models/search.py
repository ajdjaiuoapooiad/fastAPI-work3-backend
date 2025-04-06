from typing import List, Optional

from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    keyword: str = Field(..., description="検索キーワード")
    username: str = Field(..., description="ユーザー名")
    sort: Optional[str] = Field(None, description="ソート基準 (stars, forks, updated)")
    order: Optional[str] = Field("desc", description="ソート順序 (asc, desc)")
    page: int = Field(1, gt=0, description="ページ番号")


class GitHubRepository(BaseModel):
    name: str = Field(..., description="リポジトリ名")
    description: Optional[str] = Field(None, description="リポジトリの説明")
    html_url: str = Field(..., description="リポジトリの GitHub URL")


class SearchResponse(BaseModel):
    items: List[GitHubRepository] = Field(..., description="検索結果のリポジトリリスト")
    total_count: Optional[int] = Field(None, description="総検索結果数")