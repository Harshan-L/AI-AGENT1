import requests
from ddgs import DDGS


# ==========================================
# WIKIPEDIA SEARCH
# ==========================================

def wikipedia_search(query):

    try:

        url = "https://en.wikipedia.org/w/rest.php/v1/search/page"

        params = {
            "q": query,
            "limit": 3
        }

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        if response.status_code != 200:

            return "Wikipedia search failed."

        data = response.json()

        results = []

        for page in data.get("pages", []):

            title = page.get("title", "")
            description = page.get("description", "")
            excerpt = page.get("excerpt", "")

            results.append(
                f"Title: {title}\n"
                f"Description: {description}\n"
                f"Excerpt: {excerpt}\n"
            )

        if not results:

            return "No Wikipedia results found."

        return "\n".join(results)

    except Exception as e:

        return f"Wikipedia search failed: {str(e)}"


# ==========================================
# DUCKDUCKGO SEARCH
# ==========================================

def duckduckgo_search(query):

    try:

        results = DDGS().text(
            query,
            max_results=5
        )

        if not results:

            return "No DuckDuckGo results found."

        output = []

        for result in results:

            title = result.get("title", "")
            body = result.get("body", "")
            href = result.get("href", "")

            output.append(
                f"Title: {title}\n"
                f"Description: {body}\n"
                f"URL: {href}\n"
            )

        return "\n".join(output)

    except Exception as e:

        return f"DuckDuckGo search failed: {str(e)}"