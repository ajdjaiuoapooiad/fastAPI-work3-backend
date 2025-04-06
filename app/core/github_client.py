from typing import List, Optional

import httpx

from app.api.models.search import GitHubRepository

# GitHub API のベース URL
BASE_URL = "https://api.github.com"

async def search_repositories(
    keyword: str,
    username: str,
    sort: Optional[str] = None,
    order: Optional[str] = "desc",
    page: int = 1,
    per_page: int = 50,
) -> List[GitHubRepository]:
    """
    GitHub API を使用してリポジトリを検索し、GitHubRepository モデルのリストを返す非同期関数。

    Args:
        keyword: 検索キーワード。
        username: 検索するユーザー名。
        sort: ソートの基準 (例: "stars", "forks", "updated")。デフォルトは None。
        order: ソートの順序 ("asc" または "desc")。デフォルトは "desc"。
        page: ページ番号。デフォルトは 1。
        per_page: 1ページあたりの件数。デフォルトは 50。

    Returns:
        GitHubRepository モデルのリスト。
    """
    headers = {"Accept": "application/vnd.github.v3+json"}
    params = {
        "q": f"{keyword} user:{username}",
        "sort": sort,
        "order": order,
        "page": page,
        "per_page": per_page,
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/search/repositories", headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            repositories_data = data.get("items", [])
            total_count = data.get("total_count")  # ページネーション実装時に使用

            repositories: List[GitHubRepository] = []
            for repo_data in repositories_data:
                repository = GitHubRepository(
                    name=repo_data["name"],
                    description=repo_data.get("description"),
                    html_url=repo_data["html_url"],
                    # 他に必要なフィールドがあればここに追加
                )
                repositories.append(repository)

            return repositories
        except httpx.HTTPStatusError as e:
            print(f"GitHub API error: {e}")
            raise
        except httpx.RequestError as e:
            print(f"Request error: {e}")
            raise

if __name__ == "__main__":
    async def main():
        results = await search_repositories(keyword="fastapi", username="tiangolo")
        for repo in results[:5]:
            print(f"Name: {repo.name}")
            print(f"Description: {repo.description}")
            print(f"URL: {repo.html_url}")
            print("-" * 20)

    import asyncio
    asyncio.run(main())