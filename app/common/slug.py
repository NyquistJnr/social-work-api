import re

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.base_entity import BaseEntity

_NON_ALNUM_RE = re.compile(r"[^a-z0-9]+")


def slugify(text: str) -> str:
    slug = _NON_ALNUM_RE.sub("-", text.lower()).strip("-")
    return slug or "untitled"


async def ensure_unique_slug(
    session: AsyncSession, model: type[BaseEntity], base_slug: str, slug_column: str = "slug"
) -> str:
    """Appends `-2`, `-3`, ... to `base_slug` until it doesn't collide with an
    existing row (including soft-deleted ones, since slugs must stay unique
    at the DB level regardless of deletion state)."""
    column = getattr(model, slug_column)
    candidate = base_slug
    suffix = 1
    while True:
        existing = await session.execute(select(model.id).where(column == candidate))
        if existing.scalar_one_or_none() is None:
            return candidate
        suffix += 1
        candidate = f"{base_slug}-{suffix}"
