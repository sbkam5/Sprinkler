from cimis import *


def main():
    appKey = 'acac78e2-860f-4194-b27c-ebc296745833'  # cimis unique appKey
    sites = [80]  #query single site or multiple
    xls_path = 'CIMIS_query.xlsx' # TODO: make this dep on stations/query date

    interval ='hourly' #options are:    default, daily, hourly
    start = '03-01-2017' #self-explanatory
    end = '03-02-2017' #self-explanatory

    site_names, cimis_data = run_query(appKey, sites, interval,
                                       start=start, end=end)

    print(site_names, cimis_data)


if __name__ == "__main__":
    main()
