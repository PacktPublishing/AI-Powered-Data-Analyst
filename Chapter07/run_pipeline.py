def run_weekly_pricing_pipeline(pages, your_car, model_name):
    batch_requests, custom_id_map = build_page_extraction_batch(pages)
    batch_results = submit_and_parse_batch(batch_requests)
    all_listings = apply_page_extraction_results(batch_results, custom_id_map)

    df = listings_to_dataframe(all_listings)
    append_to_csv(df)

    analysis = analyze_model(df, model_name)
    if analysis is None:
        print(f"No listings found for {model_name} this week")
        return

    report_text = generate_market_report(your_car, analysis)
    log_weekly_report(analysis, report_text)

    print(report_text)


pages = [
    ("https://competitor-a.com/listings/civic", "Competitor A"),
    ("https://competitor-b.com/inventory?model=civic", "Competitor B"),
]

run_weekly_pricing_pipeline(
    pages=pages,
    your_car="2021 Honda Civic EX, 32,000 miles",
    model_name="Civic"
