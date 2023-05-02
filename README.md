# holiday-dates-combine
A script to combine the outputs from my School Holiday web scraper, Public Holiday scraper and a manually made list of other special dates.

## How to update

1. Get the public and school holiday date using:
   2. https://github.com/Kyle-Ross/au-public-holiday-data-downloader
   3. https://github.com/Kyle-Ross/au-school-holiday-scraper
4. Check that you have the desired values for every state
5. Manually update the special days csv
6. Update the date range in the script to cover any new years
7. Run the script and do count checks over the output

## Notes

- School holidays are only available a year in advance
- Different formats in the school scraper sources can cause issues, but you could always just add the date ranges manually in the backup source file