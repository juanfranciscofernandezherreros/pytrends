"""
Search Google Trends for the most searched topics related to a keyword and geo.

Usage:
    python scripts/mallorca_trends.py --keyword "Mallorca" --geo "ES" --timeframe "today 12-m"
"""

import argparse

from pytrends.request import TrendReq


def parse_args():
    parser = argparse.ArgumentParser(
        description="Fetch Google Trends data for a keyword in a given location."
    )
    parser.add_argument(
        "--keyword",
        default="Mallorca",
        help="Keyword to search on Google Trends (default: 'Mallorca')",
    )
    parser.add_argument(
        "--geo",
        default="ES",
        help="Geographic region code (e.g. 'ES' for Spain, '' for worldwide). Default: 'ES'",
    )
    parser.add_argument(
        "--timeframe",
        default="today 12-m",
        help="Timeframe for the query (e.g. 'today 12-m', 'today 3-m'). Default: 'today 12-m'",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    print(f"=== Google Trends search ===")
    print(f"  Keyword  : {args.keyword}")
    print(f"  Geo      : {args.geo if args.geo else 'Worldwide'}")
    print(f"  Timeframe: {args.timeframe}")
    print()

    pytrend = TrendReq(hl="es-ES", tz=60)
    pytrend.build_payload(
        kw_list=[args.keyword],
        geo=args.geo,
        timeframe=args.timeframe,
    )

    # --- Interest over time ---
    interest_over_time_df = pytrend.interest_over_time()
    print("=== Interest Over Time ===")
    if interest_over_time_df.empty:
        print("No data available.")
    else:
        print(interest_over_time_df.to_string())

    # --- Related queries (top searched) ---
    related_queries_dict = pytrend.related_queries()
    keyword_data = related_queries_dict.get(args.keyword, {})

    top_queries = keyword_data.get("top")
    print(f"\n=== Related Queries – Top (most searched) for '{args.keyword}' ===")
    if top_queries is None or top_queries.empty:
        print("No data available.")
    else:
        print(top_queries.to_string(index=False))

    rising_queries = keyword_data.get("rising")
    print(f"\n=== Related Queries – Rising for '{args.keyword}' ===")
    if rising_queries is None or rising_queries.empty:
        print("No data available.")
    else:
        print(rising_queries.to_string(index=False))

    # --- Related topics ---
    related_topics_dict = pytrend.related_topics()
    topic_data = related_topics_dict.get(args.keyword, {})

    top_topics = topic_data.get("top")
    print(f"\n=== Related Topics – Top for '{args.keyword}' ===")
    if top_topics is None or top_topics.empty:
        print("No data available.")
    else:
        print(top_topics[["topic_title", "topic_type", "value"]].to_string(index=False))

    rising_topics = topic_data.get("rising")
    print(f"\n=== Related Topics – Rising for '{args.keyword}' ===")
    if rising_topics is None or rising_topics.empty:
        print("No data available.")
    else:
        print(rising_topics[["topic_title", "topic_type", "value"]].to_string(index=False))


if __name__ == "__main__":
    main()
