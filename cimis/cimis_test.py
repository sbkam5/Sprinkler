from cimis import *
import numpy


def main():
    appKey = 'acac78e2-860f-4194-b27c-ebc296745833'  # cimis unique appKey
    sites = [75]  #query single site or multiple
    xls_path = 'CIMIS_query.csv' # TODO: make this dep on stations/query date

    interval ='hourly' #options are:    default, daily, hourly
    start = '06-09-2019' #self-explanatory
    end = '06-10-2019' #self-explanatory

    site_names, cimis_data = run_query(appKey, sites, interval,
                                       start=start, end=end)

    # write_output_file(xls_path, cimis_data, site_names)
    # print(type(cimis_data[0]))
    csv = cimis_data[0].to_csv(index=False)
    f = open(xls_path, "w+")
    f.write(csv)
    f.close()
    
    # print(cimis_data)


if __name__ == "__main__":
    main()
