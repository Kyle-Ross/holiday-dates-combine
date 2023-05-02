# holiday-dates-combine
A script to combine the outputs from my School Holiday web scraper, Public Holiday scraper and a manually made list of other special dates.

Outputs a date by date reference file ready for load into a database with references for Public Holidays, School Holidays and Special Days.

## How to use

1. Get the public and school holiday date using the scripts here:
   2. https://github.com/Kyle-Ross/au-public-holiday-data-downloader
   3. https://github.com/Kyle-Ross/au-school-holiday-scraper
4. Check that you have the desired values for every state
5. Manually update the special days csv
6. Update the date range in the script to cover any new years, by adjusting the 'start_date' and 'end_date' variables.
7. Run the script and do checks over the output

## Notes

- School holidays are only available a year in advance
- Different formats in the school scraper sources can cause issues, but you could always just add the date ranges manually in the backup source file in the public holidays scraper.