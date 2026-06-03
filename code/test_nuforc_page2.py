"""
Test NUFORC scraping to see what's actually happening
"""
from nuforc_real_scraper import NUFORCRealScraper

scraper = NUFORCRealScraper()

print("Testing page 2 (should have NEW reports)...")
reports = scraper.parse_table_page(2)

print(f"\nFound {len(reports)} reports on page 2")
print("\nFirst 3 reports:")
for i, report in enumerate(reports[:3], 1):
    print(f"\n{i}. {report['occurred']} | {report['city']}, {report['state']}")
    print(f"   URL: {report['report_url']}")
    print(f"   Summary: {report['summary'][:100]}...")

    # Check what case_number would be generated
    case_number = None
    if report['report_url']:
        case_number = report['report_url'].split('/')[-1].replace('.html', '')

    print(f"   Case from URL: {case_number}")

    # Hash-based
    import hashlib
    location_parts = [p for p in [report['city'], report['state'], report['country']] if p]
    location = ', '.join(location_parts)
    if not case_number or case_number.startswith('?id=') or len(case_number) < 5:
        unique_str = f"{report['occurred']}|{location}|{report['summary'][:100]}"
        case_hash = hashlib.md5(unique_str.encode()).hexdigest()[:12]
        case_number = f"NUFORC-{case_hash}"

    print(f"   Final case_number: {case_number}")
