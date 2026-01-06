from collections import OrderedDict

def dedupe_articles(articles):
    seen = OrderedDict()

    for a in articles:
        key = (a["title"] + a["source"]["name"]).lower()
        if key not in seen:
            seen[key] = a

    return list(seen.values())

def rank_articles(articles, limit=10):
    # Prefer articles with images & descriptions
    scored = sorted(
        articles,
        key=lambda x: (
            bool(x.get("image")),
            len(x.get("description") or "")
        ),
        reverse=True
    )
    return scored[:limit]
