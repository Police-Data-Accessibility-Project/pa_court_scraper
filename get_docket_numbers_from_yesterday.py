import asyncio
import datetime
import re

from playwright.async_api import async_playwright

COURT_URL = "https://ujsportal.pacourts.us/CaseSearch"

async def perform_action_and_scrape(date: datetime.datetime):

    # Get date in the format `yyyy-mm-dd`
    formatted_date = date.strftime("%Y-%m-%d")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        page = await browser.new_page()

        # Navigate to the page
        await page.goto(COURT_URL)

        # Click option with value 'DateFiled' in select element with title 'Search By'
        await page.select_option("select[title='Search By']", "DateFiled")

        await page.fill("input[name='FiledStartDate']", value=formatted_date)

        await page.fill("input[name='FiledEndDate']", value=formatted_date)

        # Clcik button with id 'btnSearch'
        await page.click("#btnSearch")

        # Wait for network idle
        await page.wait_for_load_state('networkidle')

        # Scrape the resultant data from table with id 'caseSearchResultGrid
        result = await page.inner_html("#caseSearchResultGrid")

        # Close the browser
        await browser.close()

        return result


# Example usage
async def main():

    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)

    scraped_data = await perform_action_and_scrape(date=yesterday)

    # Get all data which matches regex '<td>(MJ[^<]*)<\/td>'
    matches = [match.group(1) for match in re.finditer(r'<td>(MJ[^<]*)<\/td>', scraped_data)]

    # Write, separated by lines, to a text file
    with open("docket_numbers_from_yesterday.txt", "w") as f:
        f.write("\n".join(matches))


# Run the script
asyncio.run(main())
