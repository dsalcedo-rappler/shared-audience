Process Flow:
1. Run `Monthly Query` query in BigQuery and save in a google drive
2. Download query result with `download.py` and move to `data` folder as `sharktank-db-{yyyymm}.csv`
3. Run `gen_top1000.py`
4. Get `top1000_channels_apr2021.csv` in `results` folder and upload to BigQuery
5. Run the `Shared Audience - Channels` job in BigQuery
6. Download query result and save to `data/channels_{yyyymm}.csv`
7. Run `create.py`
    OPTIONAL: use the result from `create.py` into `sorter.py` to increase shared audience threshold
8. Upload `top1000_channels_apr2021.csv` and `top1000_links_apr2021.csv` to Flourish